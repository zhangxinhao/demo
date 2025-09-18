import os
from pathlib import Path
from openai import OpenAI


def load_env_file(file_path):
    """从.env文件加载环境变量"""
    env_vars = {}
    if Path(file_path).exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    return env_vars


if __name__ == '__main__':
    # 使用相对路径加载.env文件
    script_dir = Path(__file__).parent
    env_file = script_dir / '.env'
    env_vars = load_env_file(env_file)

    api_key = env_vars.get('OPENROUTER_API_KEY')
    if not api_key:
        raise ValueError("在.env文件中未找到OPENROUTER_API_KEY")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    completion = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": "1+1=?"
            }
        ]
    )

    print(completion.choices[0].message.content)
