#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://aweme.snssdk.com/aweme/v1/play/?video_id={video_id}
import os
from contextlib import closing

import sys

import certifi
import urllib3

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())


def vedio_download(video_name, video_url):
    if os.path.exists(video_name):
        print("downloaded! {video_name} by {video_url}".format(video_name=video_name, video_url=video_url))
        return
    size = 0
    with closing(http.request('GET', video_url, preload_content=False)) as response:
        chunk_size = 1024
        content_size = int(response.headers['content-length'])
        if response.status == 200:
            print('[文件大小]：%0.2f MB' % (content_size / chunk_size / 1024.0))
            with open(video_name, 'wb') as file:
                for data in response.stream(chunk_size):
                    file.write(data)
                    size += len(data)
                    file.flush()

                sys.stdout.flush()
            response.release_conn()


if __name__ == '__main__':
    video_id = "cd06570a459c43eebb6e11cf93d86332"
    video_name = "mp4/{video_id}.mp4".format(video_id=video_id)
    video_url = "https://aweme.snssdk.com/aweme/v1/play/?video_id={video_id}".format(video_id=video_id)
    vedio_download(video_name, video_url)
