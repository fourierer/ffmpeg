# ffmpeg
Just for learning ffmpeg





#### 一、ffmpeg的安装

ffmpeg是一个用来处理视频的命令行系统开源工具，python中也有相应的ffmpeg库。

python库安装指令：

```shell
pip install ffmpeg-python
```

安装结果(注意安装的版本，其余指令安装的ffmpeg版本差距较大)：

```
Installing collected packages: ffmpeg-python
Successfully installed ffmpeg-python-0.2.0
```

以下指令安装都不成功(原因未知)：

```shell
pip install ffmpeg
conda install ffmpeg-python
conda install ffmpeg
```





#### 二、ffmpeg的使用

以下很多指令参考了链接( https://blog.csdn.net/wenmingzheng/article/details/88373192?utm_medium=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.edu_weight&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.edu_weight )

1.获取视频的相关信息get_infomation.py

```python
import ffmpeg
import numpy
import sys
import random
import os
import cv2

def read_frame_as_jpeg(in_file, frame_num):
    """
    指定帧数读取任意帧
    """
    out, err = (
        ffmpeg.input(in_file)
              .filter('select', 'gte(n,{})'.format(frame_num))
              .output('pipe:', vframes=1, format='image2', vcodec='mjpeg')
              .run(capture_stdout=True)
    )
    return out


def read_frame_by_time(in_file, time):
    """
    指定时间节点读取任意帧
    """
    out, err = (
        ffmpeg.input(in_file, ss=time)
              .output('pipe:', vframes=1, format='image2', vcodec='mjpeg')
              .run(capture_stdout=True)
    )
    return out

def get_video_info(in_file):
    """
    获取视频基本信息
    """
    try:
        probe = ffmpeg.probe(in_file)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        if video_stream is None:
            print('No video stream found', file=sys.stderr)
            sys.exit(1)
        return video_stream
    except ffmpeg.Error as err:
        print(str(err.stderr, encoding='utf8'))
        sys.exit(1)
def main():
    file_path = './test.mp4'
    #file_path = './monkey_video/test.MTS'
    video_info = get_video_info(file_path) # 视频信息字典
    print(video_info)
    width = video_info['width'] # 宽度
    height = video_info['height'] # 高度
    total_frames = video_info['nb_frames'] # 帧数
    total_duration = video_info['duration'] # 时长
    frame_rate = video_info['r_frame_rate'] # 帧率
    bitrate = video_info['bit_rate'] # 码率
    print('宽度：{}'.format(width))
    print('高度：{}'.format(height))
    print('帧数：{}'.format(total_frames))
    print('时长：{}s'.format(total_duration))
    print('帧率：{}'.format(frame_rate))
    print('比特率(码率)：{}bps'.format(bitrate))
    '''
    #指定帧数读取任意帧
    random_frame = random.randint(1,total_frames)
    print('随机帧索引：{}'.format(random_frame))
    out = read_frame_as_jpeg(file_path, random_frame)
    image_array = numpy.asarray(bytearray(out), dtype="uint8")
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    cv2.imshow('frame', image)
    cv2.waitKey()

    #指定时间读取任意帧
    random_time = random.randint(1, int(float(total_duration)) - 1) + random.random()
    print('随机时间：{}s'.format(random_time))
    out = read_frame_by_time(file_path, random_time)
    image_array = numpy.asarray(bytearray(out), dtype="uint8")
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    cv2.imshow('frame', image)
    cv2.waitKey()
    '''

if __name__ == '__main__':
    main()
```

运行结果：

```
{'index': 0, 'codec_name': 'h264', 'codec_long_name': 'H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10', 'profile': 'High', 'codec_type': 'video', 'codec_time_base': '1/60', 'codec_tag_string': 'avc1', 'codec_tag': '0x31637661', 'width': 960, 'height': 544, 'coded_width': 960, 'coded_height': 544, 'has_b_frames': 1, 'pix_fmt': 'yuv420p', 'level': 31, 'color_range': 'tv', 'color_space': 'bt709', 'color_transfer': 'bt709', 'color_primaries': 'bt709', 'chroma_location': 'left', 'refs': 1, 'is_avc': 'true', 'nal_length_size': '4', 'r_frame_rate': '30/1', 'avg_frame_rate': '30/1', 'time_base': '1/600', 'start_pts': 0, 'start_time': '0.000000', 'duration_ts': 64980, 'duration': '108.300000', 'bit_rate': '1153599', 'bits_per_raw_sample': '8', 'nb_frames': '3249', 'disposition': {'default': 1, 'dub': 0, 'original': 0, 'comment': 0, 'lyrics': 0, 'karaoke': 0, 'forced': 0, 'hearing_impaired': 0, 'visual_impaired': 0, 'clean_effects': 0, 'attached_pic': 0, 'timed_thumbnails': 0}, 'tags': {'creation_time': '2020-05-06T13:23:13.000000Z', 'language': 'und', 'handler_name': 'Core Media Video'}}
宽度：960
高度：544
帧数：3249
时长：108.300000s
帧率：30/1
比特率(码率)：1153599bps
```

（1）比特率(bit_rate，也叫码率、数据率)是一个确定整体视频/音频质量的参数，秒为单位处理的字节数，码率和视频质量成正比，在视频文件中比特率用bps来表达；

（2）帧率(frame_rate)表示视频每秒的帧数，和平均帧率(avg_frame_rate)之间的区别？

或者直接通过命令行的ffmpeg获取：

```shell
ffmpeg -i test.mp4
```

运行结果：

```
ffmpeg version 4.2.2 Copyright (c) 2000-2019 the FFmpeg developers
  built with clang version 4.0.1 (tags/RELEASE_401/final)
  configuration: --prefix=/Users/momo/opt/anaconda3 --cc=x86_64-apple-darwin13.4.0-clang --disable-doc --enable-avresample --enable-gmp --enable-hardcoded-tables --enable-libfreetype --enable-libvpx --enable-pthreads --enable-libopus --enable-postproc --enable-pic --enable-pthreads --enable-shared --enable-static --enable-version3 --enable-zlib --enable-libmp3lame --disable-nonfree --enable-gpl --enable-gnutls --disable-openssl --enable-libopenh264 --enable-libx264
  libavutil      56. 31.100 / 56. 31.100
  libavcodec     58. 54.100 / 58. 54.100
  libavformat    58. 29.100 / 58. 29.100
  libavdevice    58.  8.100 / 58.  8.100
  libavfilter     7. 57.100 /  7. 57.100
  libavresample   4.  0.  0 /  4.  0.  0
  libswscale      5.  5.100 /  5.  5.100
  libswresample   3.  5.100 /  3.  5.100
  libpostproc    55.  5.100 / 55.  5.100
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from 'test.mp4':
  Metadata:
    major_brand     : mp42
    minor_version   : 1
    compatible_brands: mp41mp42isom
    creation_time   : 2020-05-06T13:23:13.000000Z
  Duration: 00:01:48.30, start: 0.000000, bitrate: 1206 kb/s
    Stream #0:0(und): Video: h264 (High) (avc1 / 0x31637661), yuv420p(tv, bt709), 960x544, 1153 kb/s, 30 fps, 30 tbr, 600 tbn, 1200 tbc (default)
    Metadata:
      creation_time   : 2020-05-06T13:23:13.000000Z
      handler_name    : Core Media Video
    Stream #0:1(und): Audio: aac (LC) (mp4a / 0x6134706D), 44100 Hz, mono, fltp, 48 kb/s (default)
    Metadata:
      creation_time   : 2020-05-06T13:23:13.000000Z
      handler_name    : Core Media Audio
```

ffmpeg命令行方法只适用于查看视频信息，却无法利用这些信息来处理视频，如 https://github.com/fourierer/Video_Classification_ResNet3D_Pytorch/blob/master/generate_video_jpgs_dj.py 中利用视频的信息抽帧，就没有用ffmpeg来获取视频信息，而是用了ffprobe(也可以用python自带的库来获取相关信息)。



2.分离视频和音频流

（1）从视频文件中去除音频

```shell
ffmpeg -i input.mp4 -an output.mp4 # 去除mp4视频中的音频
ffmpeg -i input.avi -vcodec copy -an output.avi # 去除avi视频中的音频
```

（2）从视频文件中去除视频，即取出音频

```shell
ffmpeg -i test.avi -acodec copy -vn bgm.mp3 # 取出avi视频中的音频，存为mp3格式
```

这个指令在.mp4格式的视频上尝试时没有成功，原因未知？（可以先将mp4格式的视频转为avi格式，再进行音频的抽取）



3.视频转码相关

```shell
ffmpeg -i test.ts -acodec copy -vcodec copy -f mp4 output.mp4 # ts视频流转mp4
ffmpeg -y -i test.ts -c:v libx264 -c:a copy -bsf:a aac_adtstoasc output.mp4 # ts视频转mp4
ffmpeg -i test.h264 -vcodec copy -f mpegts output.ts # h264视频转ts视频流 
ffmpeg -i test.h264 -vcodec copy -f mp4 output.mp4 # h264视频转mp4
ffmpeg -i test.mp4 -b:v 640k output.flv # mp4转flv
ffmpeg -i test.mp4 -acodec copy -vcodec copy -f flv output.flv # mp4转flv
ffmpeg -i test.flv -b:v 640k output.mp4 # flv转mp4
ffmpeg -i test.mp4 -s 176x144 -vcodec h263 -r 25 -b 12200 -ab 12200 -ac 1 -ar 8000 output.3gp # mp4转3gp
ffmpeg -i test.avi -s aqif -vcodec -acodec mp3 -ac 1 -ar 8000 -r 25 -ab 32 -y output.3gp # avi转3gp
ffmpeg -i test.3gp -f avi -vcodec xvid -acodec mp3 -ar 22050 output.avi # 3gp转flv
ffmpeg -i test.flv -s 176x144 -vcodec h263 -r 25 -b 200 -ab 64 -acodec mp3 -ac 1 -ar 8000 output.3gp # flv转3gp
ffmpeg -i test.mp4 output.avi # mp4转avi
ffmpeg -i test.flv -vcodec h264 -r 25 -b 200 -ab 128 -acodec mp3 -ac 2 -ar 44100 output.mp4 # flv转mp4
ffmpeg -i test.mp4 -c:v libx264 -ar 22050 -crf 28 output.flv # mp4转flv
ffmpeg -i test.avi -c copy -map 0 output.mp4 # avi转mp4
ffmpeg -i  http://vfile1.grtn.cn/2018/1542/0254/3368/154202543368.ssm/154202543368.m3u8 -c copy -bsf:a aac_adtstoasc -movflags +faststart test.mp4 # m3u8转mp4
ffmpeg -i test.mkv -y -vcodec copy -acodec copy output.mp4 # mkv转mp4
ffmpeg -i test.mkv -vcodec copy -acodec copy output.avi  # mkv转avi
```



这里添加一个windows下使用优酷自己的ffmpeg来转码kux的方法：

下载优酷客户端，找到ffmpeg.exe的位置(如F:\Program Files (x86)\YouKu\YoukuClient\nplayer\ffmpeg.exe),在nplayer目录下打开powershell，输入以下指令：

```
.\ffmpeg.exe -y -i "F:\xjj.kux" -c:a copy -c:v copy -threads 2 "F:\xjj.mp4"
```

参照指令修改路径即可。



4.视频处理相关

```shell
ffmpeg -i test.mp4 -metadata:s:v rotate="90" -codec copy output.mp4 # 旋转90°
ffmpeg -i test.mp4 -vf "transpose=1" output.mp4 # 顺时针旋转90°
ffmpeg -i test.mp4 -vf "transpose=2" output.mp4 # 逆时针旋转90°
ffmpeg -i test.mp4 -vf "transpose=3" output.mp4 # 顺时针旋转90°后再水平翻转
ffmpeg -i test.mp4 -vf "transpose=0" output.mp4 # 逆时针旋转90°后再水平翻转
ffmpeg -i test.mp4 -vf hflip output.mp4 # 水平翻转视频画面
ffmpeg -i test.mp4 -vf vflip output.mp4 # 垂直翻转视频画面
```



5.使用ffmpeg对视频进行抽帧

抽帧有很多种，包括正常均匀抽帧，抽取指定时间帧，抽取关键帧(IPB帧)，抽取场景转换帧等。以正常均匀抽帧为例，简单介绍指令以及给出一些链接供参考：( https://zhuanlan.zhihu.com/p/85895180 ),( https://www.jianshu.com/p/ddafe46827b7 ),( https://www.jianshu.com/p/3c8c4a892f3c ), ( http://www.ffmpeg.org/ffmpeg.html ).

正常均匀抽帧指令：

```shell
ffmpeg -i test.mp4 -r 1 -q:v 2 -f image2 ./jpg/%06d.jpg
```

-r 1表示每秒抽1帧；-q:v 2表示抽取的帧质量，2表示高质量，0表示低质量；-f image2表示指定的输出格式；./jpg/%06d.jpg是命名规则，表示可以保存6位数的帧数量，如000001.jpg，000002.jpg，.......。当不指定帧率-r时，默认使用视频本身帧率进行抽帧，如：

```shell
ffmpeg -i test.TS -q:v 2 ./jpg/image_%05d.jpg # 实例
```

6.使用ffmpeg加速视频和裁剪视频

ffmpeg加速视频的值从0.25到4，即最多放慢4倍和加速4倍。
如加速4倍：（不加速音频）

```shell
ffmpeg -i fast_4x.mp4 -vf  "setpts=0.25*PTS" fast_16.mp4 # 0.25表示加速4倍
```

裁剪视频：

```shell
ffmpeg -ss 00:00:03 -i fast_16.mp4 -vcodec copy -acodec copy -t 00:09:55 fast_4x.mp4 # 表示从00:00:03开始，裁剪时长为9分15秒的片段
```



