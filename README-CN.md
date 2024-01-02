# DJIConcat 中文文档
这个项目提供了一个高效的解决方案，用于自动合并DJI相机自动切分的视频片段。当DJI相机因文件大小限制（每4GB）而将长视频切分成多个小片段时，本工具能够自动识别并将它们无缝合并回一个完整的视频文件，特别适用于长时间的录影场景。

## ⚠️写在前面

**数据是无价的, 在运行此工具前, 请确保已做好相应的备份工作, 如若出现数据丢失问题, 概不负责**

## 主要特性
- 自动合并: 自动识别并合并分散的DJI视频片段。
- 干运行模式: 提供一个干运行选项，允许用户预览将要执行的操作，而不进行实际合并。
- 详细输出: 可以启用详细输出模式，以获取更多关于处理过程的信息。
- 灵活的源和目标路径: 允许用户指定视频片段的源目录和合并后视频的目标目录。
- 手动选择合并: 为用户提供手动选择特定视频文件进行合并的选项。
- 一键操作: 提供一个选项，以自动查找并合并视频，无需额外的用户输入。
- 自定义合并列表: 允许用户指定一个包含要合并视频文件列表的文件，为合并过程提供更多的灵活性和控制。

这个工具对于需要处理大量DJI视频文件的用户来说是非常有价值的，无论是专业摄影师还是航拍爱好者都会发现它在视频编辑过程中大大节省了时间和精力。

## 安装

`git clone https://github.com/chann1n9/DJIConcat.git`

此工具依赖ffmpeg, 请确保运行前已安装ffmpeg
### macOS
`brew install ffmpeg`
### Windows
[ffmpeg Download Page](https://ffmpeg.org/download.html)
### Linux
自行使用apt/dnf/pacman安装

## 快速开始

`python3 merge.py -s /path/to/videos -t merge-videos -y`

自动寻找/path/to/videos路径下被切片的视频, 并自动合并

## 更多使用方法

`python3 merge.py -s /path/to/videos -d`

只寻找符合合并条件的视频但不执行合并

### 交互式运行
`python3 merge.py -s /path/to/videos`

你将会看到类似下列输出

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

此时你可以通过每行前的index选择合并哪一条队列
例如:

- 全部合并: `*`
- 合并1, 3, 5, 7: `1,3,5,7`
- 合并1到3: `1-3`
- 甚至组合选择: `1,3,5-7`
- 反选: `!1,3,5,7`最终会选择2, 4, 6
- 组合反选: `!1,3,5-7`最终会选择2, 4

### 关于 --target-path

--target-path有三种用法

1. 默认: 当--target-path没有收到参数, 会将--source-path的值作为自己的值, 但非常不建议这种方式, 因为当合并过程被打断且已经生成了合并视频后, 会影响再次操作, 除非在交互式运行中排除已经合并的视频队列, 如果某条队列没有合并完毕, 请自行删除未完成的视频
2. 以 “./” 或 “/”开头: --target-path会被赋值此相对路径或绝对路径
3. 以--source-path的值作为相对路径起点: 例如对--target-path赋值为 “merge-videos” 或 “merge-videos/journey2west,” 当--source-path接收到的值为 “/path/to/videos” 时, 会最终将合并的视频放到 “/path/to/videos/merge-videos” 或 “/path/to/videos/merge-videos/journey2west”

### 手动合并视频

```
python3 merge.py -s /path/to/videos \
--manual video1.mp4 video2.mp4 video3.mp4 -t merge-videos
```

手动将video1.mp4 video2.mp4 video3.mp4三个视频合并为一条视频

**注意: 此时不会对提供的视频是否符合合并条件做判断, 会强行进行合并, 建议在手动合并视频前, 先利用dry run模式查看哪些视频是符合合并条件的**

`python3 merge.py -s /path/to/videos --dry-run`

### 关于merge file

--merge-file参数是用来确定merge file存放位置的, merge file是ffmpeg合并视频时的依据, 可以看作是一个缓存文件, 默认为运行目录
