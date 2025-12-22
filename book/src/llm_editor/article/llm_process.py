"""
大模型处理模块（文章版）
遍历 data/article/prompt_txt 目录下的 txt 文件，调用大模型进行处理
输出 md 文件到 data/article/md 目录
"""

import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from llm_editor.utils import (
    get_src_dir,
    get_data_dir,
    read_file,
    write_file,
    ensure_dir,
    get_logger,
)

# 初始化 logger
logger = get_logger("article_llm_process")


def get_article_prompt_txt_dir() -> Path:
    """获取文章 prompt_txt 目录"""
    return get_data_dir() / "article" / "prompt_txt"


def get_article_md_dir() -> Path:
    """获取文章 md 输出目录"""
    return get_data_dir() / "article" / "md"


def load_env() -> tuple[str, str, int]:
    """
    加载环境变量配置
    
    Returns:
        (api_key, model_name, num_threads) 元组
    """
    env_path = get_src_dir() / ".env"
    load_dotenv(env_path)

    api_key = os.getenv("OPENROUTER_API_KEY")
    model_name = os.getenv("MODEL_NAME")
    num_threads_str = os.getenv("NUM_THREADS", "2")

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in .env file")
    if not model_name:
        raise ValueError("MODEL_NAME not found in .env file")

    try:
        num_threads = int(num_threads_str)
    except ValueError:
        logger.warning(f"Invalid NUM_THREADS value '{num_threads_str}', using default 2")
        num_threads = 2

    return api_key, model_name, num_threads


def call_llm(client: OpenAI, model_name: str, prompt: str, file_name: str) -> tuple[str, float, int, int]:
    """
    调用大模型API
    
    Args:
        client: OpenAI客户端
        model_name: 模型名称
        prompt: 提示词内容
        file_name: 文件名（用于日志标识）
    
    Returns:
        (模型响应内容, 耗时秒数, prompt_tokens, completion_tokens) 元组
    """
    try:
        # 打印请求的字符数
        prompt_chars = len(prompt)
        logger.info(f"[{file_name}] Request prompt chars: {prompt_chars}")

        start_time = time.time()
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
        elapsed_time = time.time() - start_time

        # 获取 token 使用情况
        prompt_tokens = response.usage.prompt_tokens if response.usage else 0
        completion_tokens = response.usage.completion_tokens if response.usage else 0

        logger.info(
            f"[{file_name}] LLM call completed in {elapsed_time:.2f}s, prompt_tokens: {prompt_tokens}, completion_tokens: {completion_tokens}")
        return response.choices[0].message.content, elapsed_time, prompt_tokens, completion_tokens
    except Exception as e:
        logger.error(f"[{file_name}] Error calling LLM: {e}")
        raise


def process_single_file(
        client: OpenAI,
        model_name: str,
        txt_file: Path,
        output_dir: Path
) -> tuple[str, bool, float, int, int]:
    """
    处理单个txt文件
    
    Args:
        client: OpenAI客户端
        model_name: 模型名称
        txt_file: txt文件路径
        output_dir: 输出目录
    
    Returns:
        (文件名, 是否成功, 耗时秒数, prompt_tokens, completion_tokens)
    """
    file_name = txt_file.name
    try:
        # 读取文件内容作为提示词
        prompt = read_file(txt_file)

        logger.info(f"Processing file: {file_name}")

        # 调用大模型
        result, elapsed_time, prompt_tokens, completion_tokens = call_llm(client, model_name, prompt, file_name)

        # 保存结果到md文件
        output_file = output_dir / f"{txt_file.stem}.md"
        write_file(output_file, result)

        logger.info(f"Completed: {file_name} -> {output_file.name} (took {elapsed_time:.2f}s)")
        return file_name, True, elapsed_time, prompt_tokens, completion_tokens

    except Exception as e:
        logger.error(f"Failed to process {file_name}: {e}")
        return file_name, False, 0.0, 0, 0


def process_articles(
        client: OpenAI,
        model_name: str,
        input_dir: Path,
        output_dir: Path,
        num_threads: int
) -> bool:
    """
    处理所有文章txt文件
    
    Args:
        client: OpenAI客户端
        model_name: 模型名称
        input_dir: 输入目录
        output_dir: 输出目录
        num_threads: 并发线程数
    
    Returns:
        是否全部处理成功
    """
    if not input_dir.exists():
        logger.warning(f"Input directory not found: {input_dir}")
        return False

    # 获取所有txt文件
    txt_files = list(input_dir.glob("*.txt"))
    if not txt_files:
        logger.warning(f"No txt files found in {input_dir}")
        return False

    # 创建输出目录
    ensure_dir(output_dir)

    logger.info(f"Found {len(txt_files)} txt files")
    logger.info(f"Using {num_threads} threads")

    # 使用线程池并发处理
    success_count = 0
    fail_count = 0
    total_elapsed_time = 0.0
    total_prompt_tokens = 0
    total_completion_tokens = 0

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
                file_name, success, elapsed_time, prompt_tokens, completion_tokens = future.result()
                if success:
                    success_count += 1
                    total_elapsed_time += elapsed_time
                    total_prompt_tokens += prompt_tokens
                    total_completion_tokens += completion_tokens
                else:
                    fail_count += 1
            except Exception as e:
                logger.error(f"Exception processing {txt_file.name}: {e}")
                fail_count += 1

    # 计算平均耗时
    avg_time = total_elapsed_time / success_count if success_count > 0 else 0.0
    logger.info(f"Processing complete: {success_count} success, {fail_count} failed")
    logger.info(f"Total LLM time: {total_elapsed_time:.2f}s, Average per file: {avg_time:.2f}s")
    logger.info(
        f"Total tokens - prompt: {total_prompt_tokens}, completion: {total_completion_tokens}, total: {total_prompt_tokens + total_completion_tokens}")

    return fail_count == 0


def main() -> None:
    """主函数"""
    # 路径配置
    input_dir = get_article_prompt_txt_dir()
    output_dir = get_article_md_dir()

    # 加载环境变量
    logger.info("Loading environment variables...")
    api_key, model_name, num_threads = load_env()
    logger.info(f"Using model: {model_name}")
    logger.info(f"Using {num_threads} threads")

    # 创建OpenAI客户端
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    # 处理所有文章
    logger.info(f"Input directory: {input_dir}")
    logger.info(f"Output directory: {output_dir}")

    success = process_articles(
        client=client,
        model_name=model_name,
        input_dir=input_dir,
        output_dir=output_dir,
        num_threads=num_threads
    )

    if success:
        logger.info("All articles processed successfully!")
    else:
        logger.warning("Some articles failed to process")


if __name__ == "__main__":
    main()
