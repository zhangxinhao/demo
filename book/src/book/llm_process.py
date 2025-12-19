"""
大模型处理模块
读取配置文件，遍历书籍的txt文件，调用大模型进行处理
"""

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import yaml
from dotenv import load_dotenv
from openai import OpenAI


def get_project_root() -> Path:
    """获取项目根目录"""
    # 从src/book/llm_process.py往上两级
    return Path(__file__).parent.parent.parent


def get_src_dir() -> Path:
    """获取src目录"""
    return Path(__file__).parent.parent


def load_env():
    """加载环境变量配置"""
    env_path = get_src_dir() / ".env"
    load_dotenv(env_path)

    api_key = os.getenv("OPENROUTER_API_KEY")
    model_name = os.getenv("MODEL_NAME")

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in .env file")
    if not model_name:
        raise ValueError("MODEL_NAME not found in .env file")

    return api_key, model_name


def load_config(config_path: Path) -> dict:
    """加载配置文件"""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_config(config_path: Path, config: dict) -> None:
    """保存配置文件"""
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)


def get_books_to_process(books_config: dict) -> list[str]:
    """
    获取需要处理的书籍列表
    筛选条件：completed=true 且 llm_process=false
    """
    books_to_process = []
    for book_name, book_info in books_config.items():
        completed = book_info.get("completed", False)
        llm_processed = book_info.get("llm_process", False)

        if completed and not llm_processed:
            books_to_process.append(book_name)

    return books_to_process


def read_txt_file(file_path: Path) -> str:
    """读取txt文件内容"""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def save_result_file(file_path: Path, content: str) -> None:
    """保存处理结果到文件"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def call_llm(client: OpenAI, model_name: str, prompt: str) -> str:
    """
    调用大模型API
    
    Args:
        client: OpenAI客户端
        model_name: 模型名称
        prompt: 提示词内容
    
    Returns:
        模型响应内容
    """
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            extra_body={"reasoning": {"enabled": True}}
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling LLM: {e}")
        raise


def process_single_file(
        client: OpenAI,
        model_name: str,
        txt_file: Path,
        output_dir: Path
) -> tuple[str, bool]:
    """
    处理单个txt文件
    
    Args:
        client: OpenAI客户端
        model_name: 模型名称
        txt_file: txt文件路径
        output_dir: 输出目录
    
    Returns:
        (文件名, 是否成功)
    """
    file_name = txt_file.name
    try:
        # 读取文件内容作为提示词
        prompt = read_txt_file(txt_file)

        print(f"Processing file: {file_name}")

        # 调用大模型
        result = call_llm(client, model_name, prompt)

        # 保存结果到md文件
        output_file = output_dir / f"{txt_file.stem}.md"
        save_result_file(output_file, result)

        print(f"Completed: {file_name} -> {output_file.name}")
        return file_name, True

    except Exception as e:
        print(f"Failed to process {file_name}: {e}")
        return file_name, False


def process_book(
        client: OpenAI,
        model_name: str,
        book_name: str,
        txt_dir: Path,
        output_base_dir: Path,
        num_threads: int
) -> bool:
    """
    处理单本书籍的所有txt文件
    
    Args:
        client: OpenAI客户端
        model_name: 模型名称
        book_name: 书籍名称
        txt_dir: txt文件目录
        output_base_dir: 输出基础目录
        num_threads: 并发线程数
    
    Returns:
        是否全部处理成功
    """
    book_txt_dir = txt_dir / book_name

    if not book_txt_dir.exists():
        print(f"Warning: Directory not found for book '{book_name}': {book_txt_dir}")
        return False

    # 获取所有txt文件
    txt_files = list(book_txt_dir.glob("*.txt"))
    if not txt_files:
        print(f"Warning: No txt files found in {book_txt_dir}")
        return False

    # 创建输出目录
    output_dir = output_base_dir / book_name
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Processing book: {book_name}")
    print(f"Found {len(txt_files)} txt files")
    print(f"Using {num_threads} threads")

    # 使用线程池并发处理
    success_count = 0
    fail_count = 0

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # 提交所有任务
        futures = {
            executor.submit(
                process_single_file,
                client,
                model_name,
                txt_file,
                output_dir
            ): txt_file
            for txt_file in txt_files
        }

        # 收集结果
        for future in as_completed(futures):
            txt_file = futures[future]
            try:
                file_name, success = future.result()
                if success:
                    success_count += 1
                else:
                    fail_count += 1
            except Exception as e:
                print(f"Exception processing {txt_file.name}: {e}")
                fail_count += 1

    print(f"Book '{book_name}' processing complete: {success_count} success, {fail_count} failed")

    return fail_count == 0


def main():
    """主函数"""
    root = get_project_root()

    # 路径配置
    config_path = root / "data" / "yaml" / "config.yaml"
    txt_dir = root / "data" / "txt"
    output_dir = root / "data" / "md"

    # 加载环境变量
    print("Loading environment variables...")
    api_key, model_name = load_env()
    print(f"Using model: {model_name}")

    # 创建OpenAI客户端
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    # 加载配置
    print("Loading config...")
    config = load_config(config_path)
    num_threads = config.get("num_threads", 2)
    books_config = config.get("books", {})

    # 获取需要处理的书籍
    books_to_process = get_books_to_process(books_config)

    if not books_to_process:
        print("No books to process (requires completed=true and llm_process=false)")
        return

    print(f"Found {len(books_to_process)} books to process: {books_to_process}")

    # 处理每本书
    processed_books = []
    for book_name in books_to_process:
        success = process_book(
            client=client,
            model_name=model_name,
            book_name=book_name,
            txt_dir=txt_dir,
            output_base_dir=output_dir,
            num_threads=num_threads
        )

        if success:
            processed_books.append(book_name)

    # 更新配置，标记已处理的书籍
    for book_name in processed_books:
        if book_name in config["books"]:
            config["books"][book_name]["llm_process"] = True

    # 保存配置
    save_config(config_path, config)
    print(f"Config updated. Marked {len(processed_books)} books as llm_process=true")


if __name__ == "__main__":
    main()
