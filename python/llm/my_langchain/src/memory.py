import os

import openai

from pathlib import Path
from dotenv import load_dotenv, find_dotenv

from langchain import OpenAI, ConversationChain


def init():
    env_path = Path.home().joinpath('.config/py.env')
    _ = load_dotenv(find_dotenv(env_path.as_posix()))

    openai.api_key = os.environ['OPENAI_API_KEY']


def chat():
    llm = OpenAI(temperature=0)
    conversation = ConversationChain(llm=llm, verbose=True)
    output = conversation.predict(input="你好")
    print(output)


if __name__ == '__main__':
    init()
    chat()
