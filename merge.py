#!/usr/bin/python3

import os
import sys
import math
import argparse
import subprocess
from datetime import datetime
import logging


SOURCE_PATH = None
TARGET_PATH = None
MERGE_LIST_PATH = None


def run(cmd):
    if isinstance(cmd, str):
        cmd = cmd.split()
    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True)
        stdout = result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

    return stdout


def ffmpeg_info(file_path):
    cmd_base = "ffprobe -v error -select_streams v:0"
    cmd_entries = "-show_entries stream_tags=creation_time:format=duration"
    cmd_format = "-of default=noprint_wrappers=1:nokey=1"
    cmd = f"{cmd_base} {cmd_entries} {cmd_format} {file_path}"
    logging.debug(f"Command : {cmd}")
    stdout = run(cmd)
    creation, duration = stdout.split()
    logging.debug(f"{file_path} : ffmpeg get creation : {creation}")
    logging.debug(f"{file_path} : ffmpeg get duration : {duration}")
    return creation, duration


def get_creation_ts(creation):
    creation_ts = datetime.fromisoformat(creation.rstrip("Z")).timestamp()
    return creation_ts


def get_end_ts(creation, duration):
    c_ts = get_creation_ts(creation)
    end_ts = math.ceil(c_ts + float(duration))
    return end_ts


def generate_merge_list():
    logging.info(f"SOURCE PATH : {SOURCE_PATH}")
    files_name = sorted(
        [_ for _ in os.listdir(SOURCE_PATH) if _.endswith('.MP4')])

    files_gt_4090M = []
    for file in files_name:
        file_path = f"{SOURCE_PATH}/{file}"
        size = os.path.getsize(file_path)
        logging.debug(f"{file_path} : Get file size : {size}")
        if size >= 4090000000:
            logging.debug(f"{file_path} : Size of : greater than 4090MB")
            files_gt_4090M.append(file)

    logging.info(f"Files greater than 4090M : Number: {len(files_gt_4090M)}")
    logging.info(f"Files greater than 4090M : {files_gt_4090M}")

    check_items = set()
    for head in files_gt_4090M:
        if head not in check_items:

            merge_list = [head,]
            i_head = files_name.index(head)
            logging.info(f"Checking start on (head FILE) : {head}")
            logging.debug(f"Index of head files : {i_head}")

            creation, duration = ffmpeg_info(f"{SOURCE_PATH}/{head}")
            end_ts = get_end_ts(creation, duration)
            logging.debug(f"{SOURCE_PATH}/{head} : Ended on {end_ts}")

            for f in files_name[i_head + 1:]:
                f_c, f_d = ffmpeg_info(f"{SOURCE_PATH}/{f}")
                f_c_ts = get_creation_ts(f_c)
                logging.debug(f"{SOURCE_PATH}/{f} : Created on {f_c_ts}")

                if f_c_ts == end_ts or abs(f_c_ts - end_ts) <= 1:
                    logging.info(
                        f"{SOURCE_PATH}/{f} is being appended in merge list")
                    merge_list.append(f)

                    if f in files_gt_4090M:
                        check_items.add(f)

                else:
                    break

                end_ts = get_end_ts(f_c, f_d)

            logging.info(f"Merge list : {merge_list}")
            yield merge_list


def ffmpeg_merge(merge_list):
    with open(f"{MERGE_LIST_PATH}", 'w', encoding='utf-8') as f:
        f.writelines([f"file '{SOURCE_PATH}/{_}'\n" for _ in merge_list])
    logging.debug(f"Merge list {merge_list} is writed in {MERGE_LIST_PATH}")

    head_file_name = merge_list[0]
    tail_file_name = merge_list[-1]
    suffix = {_.split('.')[-1] for _ in merge_list}
    assert len(suffix) == 1, f"Videos format is not same: {merge_list}"
    out_file_name = f"{os.path.splitext(head_file_name)[0]}-{tail_file_name}"
    logging.debug(
        f"Start merging : From {head_file_name} : To {tail_file_name}.{suffix}")
    logging.info(f"Start merging into {out_file_name}")
    run(f"ffmpeg -f concat -safe 0 -i {MERGE_LIST_PATH} -c copy {TARGET_PATH}/{out_file_name}")
    logging.info(f"{out_file_name}.{suffix} : Merge finished")


def main():
    parser = argparse.ArgumentParser(
        description="Find DJI's auto-sliced videos and merge them into one video.")
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Enable dry-run mode, which will not perform actual operations.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable verbose output mode.")
    parser.add_argument(
        "-s",
        "--source-path",
        required=True,
        help="Directory of videos you want to merge. Such as ./videos or /path/to/videos")
    parser.add_argument(
        "-t", "--target-path", help="Directory of output files. \
                                Such as ./output or /path/to/output \
                                Defaults to the same as source-path. If the path entered does not start with '/' or './' \
                                (e.g., 'output' or 'output/somewhere'), the file will be saved in 'source-path/output' \
                                or 'source-path/output/somewhere', respectively.")
    parser.add_argument(
        "-m",
        "--manual",
        nargs='+',
        metavar='MEDIA',
        help="The list you want to merge. Such as --manual /path/to/videos1 /path/to/videos2")
    parser.add_argument("-y", "--yes-to-all", action="store_true",
                        help="Automatically find and merge videos.")
    parser.add_argument(
        "--merge-file",
        default="./merge.list",
        help="Specifies the location of the 'merge.list' file, defaulting to './merge.list'.")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    global SOURCE_PATH
    global TARGET_PATH
    global MERGE_LIST_PATH
    SOURCE_PATH = os.path.abspath(args.source_path)
    if args.target_path:
        TARGET_PATH = args.target_path if args.target_path.startswith(
            ('/', './')) else f"{SOURCE_PATH}/{args.target_path}"
    else:
        TARGET_PATH = SOURCE_PATH
    MERGE_LIST_PATH = os.path.abspath(args.merge_file)
    logging.info(f"SOURCE_PATH : {SOURCE_PATH}")
    logging.info(f"TARGET_PATH : {TARGET_PATH}")
    logging.info(f"MERGE_LIST_PATH : {MERGE_LIST_PATH}")

    if args.manual:
        merge_list = args.manual
        if len(merge_list) > 1:
            logging.info(f"Video list : {merge_list}")
            ffmpeg_merge(merge_list)
        else:
            logging.error(f"Video list : {merge_list}")
            logging.error("Length of video list must greater than 1")

    if not args.manual:
        merge_summary = list(generate_merge_list())

        if args.yes_to_all:

            for merge_list in merge_summary:
                ffmpeg_merge(merge_list)

            sys.exit()
        else:
            pass

        print("*********************")
        print("*   Merge Summary   *")
        print("*********************")
        merge_summary_dict = dict(enumerate(merge_summary, start=1))

        for i, merge_list in merge_summary_dict.items():
            print(f"{i}. {' '.join(merge_list)}")

        if not args.dry_run:
            _msg = """Input index of merge list. Such as 1,2,3 or 1-7,10-14,16,17
            OR * for ALL
            OR ! for NOT. Such as !1,2 or !3-6,9-12:"""
            print(_msg)
            ipt = input()

            keys = []

            if '*' in ipt:
                assert '*' == ipt, "DO NOT USE * with other statement!"
            else:
                for clip in ipt.lstrip('!').split(','):

                    if '-' not in clip:
                        keys.append(int(clip))
                    else:
                        _range = clip.split('-')
                        for i in range(int(_range[0]), int(_range[-1]) + 1):
                            keys.append(i)

                print("These videos will be merged:")
                if ipt.startswith('!'):
                    keys = [
                        _ for _ in list(merge_summary_dict) if _ not in keys]
                for i in keys:
                    print(f"{i}. {merge_summary_dict[i]}")

                merge_summary = [merge_summary_dict[i] for i in keys]

            switch = input("Are you sure to continue? [Y/n]: ").lower()
            if 'y' == switch:
                for merge_list in merge_summary:
                    ffmpeg_merge(merge_list)


if __name__ == "__main__":
    main()
