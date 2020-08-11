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
    #file_path = './test.avi'
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





