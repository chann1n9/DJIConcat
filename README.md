# DJIConcat

This project offers a streamlined solution for automatically merging video segments created by DJI cameras. Designed to address the issue of long videos being split into multiple clips due to the 4GB file size limitation of DJI cameras, this tool seamlessly stitches these segments back into a single video file. It's particularly beneficial for extended recording sessions.

[点击这里查看中文版说明](README-CN.md)

## ⚠️Preface

**Data is priceless. Before running this tool, please ensure that you have made appropriate backups. We are not responsible for any data loss that may occur.**

## Key Features

- Automatic Merging: Automatically identifies and combines scattered DJI video segments.
- Dry Run Mode: Includes a dry run option that allows users to preview the actions to be performed without actual merging.
- Verbose Output: Users can enable a verbose output mode for additional information about the processing.
- Flexible Source and Target Paths: Users can specify the directories for the source video segments and the merged output.
- Manual Selection for Merging: Provides an option for manually selecting specific video files to merge.
- One-click Operation: Offers an option for automatically locating and merging videos without additional user input.
- Custom Merge List: Users can specify a file containing a list of video files to be merged, offering more flexibility and control in the merging process.

This tool is highly valuable for users who need to handle a large volume of DJI video files, from professional photographers to aerial photography enthusiasts, saving considerable time and effort in the video editing process.

## Installation

`git clone https://github.com/chann1n9/DJIConcat.git`

This tool relies on ffmpeg, please ensure ffmpeg is installed before running.

### macOS

`brew install ffmpeg`

### Windows

[ffmpeg Download Page](https://ffmpeg.org/download.html)

### Linux

Install using apt/dnf/pacman as appropriate.

## Quick Start

`python3 merge.py -s /path/to/videos -t merge-videos -y`

Automatically searches for segmented videos in the /path/to/videos path and merges them automatically.

## More Usage Methods

`python3 merge.py -s /path/to/videos -d`

Only searches for videos that meet the merging criteria but does not perform the merge.

### Interactive Mode

`python3 merge.py -s /path/to/videos`

You will see an output similar to the following:

```
...
*********************
*   Merge Summary   *
*********************
1. DJI_0024.MP4 DJI_0025.MP4 DJI_0026.MP4
2. DJI_0030.MP4 DJI_0031.MP4
3. DJI_0037.MP4 DJI_0038.MP4
4. DJI_0062.MP4 DJI_0063.MP4
5. DJI_0099.MP4 DJI_0100.MP4 DJI_0101.MP4 DJI_0102.MP4 DJI_0103.MP4 DJI_0104.MP4
6. DJI_0106.MP4 DJI_0107.MP4 DJI_0108.MP4
7. DJI_0113.MP4 DJI_0114.MP4 DJI_0115.MP4 DJI_0116.MP4
Input index of merge list. Such as 1,2,3 or 1-7,10-14,16,17
        OR * for ALL
        OR ! for NOT. Such as !1,2 or !3-6,9-12:
```

At this point, you can choose which queue to merge by the index at the start of each line. For example:

- Merge all: `*`
- Merge 1, 3, 5, 7: `1,3,5,7`
- Merge 1 to 3: `1-3`
- Even combine choices: `1,3,5-7`
- Invert selection: `!1,3,5,7` ultimately selects 2, 4, 6
- Combine invert selection: `!1,3,5-7` ultimately selects 2, 4

### About --target-path

There are three ways to use --target-path:

1. Default: When --target-path does not receive an argument, it takes the value of --source-path. However, this is not recommended because if the merging process is interrupted and a merged video has already been created, it will affect subsequent operations unless the already merged video queue is excluded in interactive mode. If a queue is not fully merged, please delete the incomplete video yourself.
2. Starting with "./" or "/": --target-path will be assigned this relative or absolute path.
3. Using the value of --source-path as a starting point for the relative path: For example, assigning "merge-videos" or "merge-videos/journey2west" to --target-path, when --source-path receives the value "/path/to/videos", the merged videos will eventually be placed in "/path/to/videos/merge-videos" or "/path/to/videos/merge-videos/journey2west".

### Manual Video Merging

```
python3 merge.py -s /path/to/videos \
--manual video1.mp4 video2.mp4 video3.mp4 -t merge-videos
```

Manually merges video1.mp4, video2.mp4, and video3.mp4 into a single video. Note: At this point, it does not check if the provided videos meet the merging criteria and will forcefully merge. It is advisable to use dry run mode first to see which videos meet the merging criteria.

`python3 merge.py -s /path/to/videos --dry-run`

### About merge file

The --merge-file parameter is used to determine the location of the merge file. The merge file is a basis for ffmpeg to merge videos and can be considered a cache file. It is set to the directory where the command is run by default.
