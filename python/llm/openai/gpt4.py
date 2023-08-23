import time
import requests
import json
import openai
import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

api_key = ''
url = 'https://api.aiguoguo199.com/v1/chat/completions'
headers = ''
payload = ''


def init():
    env_path = Path.home().joinpath('.config/py.env')
    _ = load_dotenv(find_dotenv(env_path.as_posix()))
    openai.api_key = os.environ['OPENAI_API_KEY']
    global api_key
    api_key = os.environ['OPENAI_API_KEY_4']


def set_headers():
    global headers
    headers = {
        'Authorization': 'Bearer ' + api_key,
        'Content-Type': 'application/json'
    }


def set_payload(content):
    global payload
    payload = {
        "model": "gpt-4",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": content
            }
        ]
    }


def test():
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    data = response.json()

    # 提取助手的回复
    if 'choices' in data:
        reply = data['choices'][0]['message']['content']
        print(reply)
    else:
        print('意外的响应格式')


if __name__ == '__main__':
    init()
    set_headers()
    start_time = time.time()
    set_payload("python如何在函数内部修改全局变量")
    test()
    end_time = time.time()
    print("time:", (end_time - start_time), "s")
