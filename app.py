import argparse
import requests
import json
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from downloader import download
from error import *

def saveHtml(name, data):
    with open('html/'+name+'.html', 'w', encoding='utf-8') as f:
        f.write(data)
        f.close()

def Download(url, status, DEBUG=True)->dict:
    headers = {
        'authority': 'www.tiktok.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    session = requests.Session()
    response = session.get(url, headers=headers)
    if response.status_code >= 400:
        raise NotFound(response.status_code)
    soup = BeautifulSoup(response.content, 'html.parser')

    if DEBUG:
        saveHtml('res1',soup.prettify())

    script = soup.select_one('script#__UNIVERSAL_DATA_FOR_REHYDRATION__')
    jsonData = json.loads(script.string)["__DEFAULT_SCOPE__"]["webapp.video-detail"]["itemInfo"]["itemStruct"]
    author = jsonData["author"]["uniqueId"]
    video = jsonData['video']
    createTime =  jsonData['createTime']

    videoUrl = video['playAddr']
    cover = video['cover']
    dynamicCover = video['dynamicCover']
    videoFormat = video['format']

    headers = {
        'authority': 'v16-webapp-prime.tiktok.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'origin': 'https://www.tiktok.com',
        'pragma': 'no-cache',
        'range': 'bytes=0-',
        'referer': 'https://www.tiktok.com/',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'video',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        }
    if status == 1:
        download(videoUrl, './video/'+author+'-'+createTime+'.'+videoFormat, videoFormat, headers, session)
    return {"cover":cover, "dynamic cover":dynamicCover, "url":videoUrl}

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='app.py' , description="TikTik Downloader is a python app for downloading TikToks")
    parser.add_argument('-d', '--download', action='store_true', help="Download option")
    parser.add_argument('--url', '-u', help="URL of the TikTok video",)
    parser.add_argument('--info', action='store_true', help="For showing video info")
    args = parser.parse_args()
    return args

def url_validator(url):
    url_p = urlparse(url)
    query = url_p.query
    if url_p.query != "is_from_webapp=1&sender_device=pc":
        query = "is_from_webapp=1&sender_device=pc"
    return f"{url_p.scheme}://{url_p.netloc}{url_p.path}?{query}"

if __name__ == '__main__':
    args = parse_arguments()
    if args.url:
        if args.download:
            Download(args.url, status=1)
        elif args.info:
            print(Download(status=0))
        else:
            print('[-] invalid args. please check app.py -h for help')
    else:
        print("Specify Url with -u or  --url")
