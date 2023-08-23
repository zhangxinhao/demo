import os
import time

import openai
from pathlib import Path
from dotenv import load_dotenv, find_dotenv


def init():
    env_path = Path.home().joinpath('.config/py.env')
    _ = load_dotenv(find_dotenv(env_path.as_posix()))

    openai.api_key = os.environ['OPENAI_API_KEY']


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]


def test():
    res = get_completion("111+222=？")
    print(res)


if __name__ == '__main__':
    init()
    # 统计test函数的执行时间
    start_time = time.time()
    test()
    end_time = time.time()
    print('time cost: ', end_time - start_time, 's')
