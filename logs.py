#!/usr/bin/env python
#auth Yong.jianzhuang
#version 0.1
#date 20181211
#mail: Yong.jianzhuang@dr-elephant.com

import logging

def log(info):
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='/data/Python/Release/logs/release.log',
                    filemode='a')
    logging.info(info)

if __name__ == "__main__":
    log('This is a write test line')

