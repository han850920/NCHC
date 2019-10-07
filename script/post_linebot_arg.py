"""
    just a glue code for temporal using that send out the line-bot command.
    2019-08-24 20:28:12
    @J4J
"""
"""
    Usage:
    $ time python -m scripts.post_linebot_arg 'thbCCTV-11-0020-033-01' '台 2(淡金公路/阿里荖 坑路到淡金公路/跳水路)' '2019-08-24:20:14:49' 'thbCCTV-11-0020-033-01_20190824-2014.jpg' '/tmp/20190824-2014/thbCCTV-11-0020-033-01_20190824-2014.jpg'
"""


#import argparse
import requests
import sys
from .util import Reporter

def post_Linebot(tvid, road, realtime, im_name, im_full_name):
    # upload image to temp
    files = {'file': (im_name, open(im_full_name, 'rb'))}
    response = requests.post('https://mlab.nchc.org.tw/linebot/upload/', files=files)
    print(response.content)
    
    # send message to line
    content = 'imageUrl=https://mlab.nchc.org.tw/linebot/upload/' + im_name + '&thumbnailUrl=https://mlab.nchc.org.tw/linebot/upload/' + im_name + '&textContent=' + '[觀測時間] '+ realtime + '\n[觀測站] '+ tvid + '\n[位置] '+ road + '&groupId=C548424a26e1ca19af55daaad605aa9f6'
    response = requests.post('https://mlab.nchc.org.tw/linebot/message/', headers={'Content-type': 'application/x-www-form-urlencoded'}, data=content.encode('utf-8'))


if __name__ == "__main__":

#    parser = argparse.ArgumentParser()
#    parser.add_argument("--image", help="image to be processed")
#    sys.argv[1]
#    print(sys.argv[1])
    post_Linebot(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    print('Done..', sys.argv)
