import json
import os

from agent_heaven.jinja_utils.utils.jinja_utils import load_jinja_env
from agent_heaven.jinja_utils.utils.llm_utils import MockLLM


def get_db_info():
    """字符串拼接DB表当中的所有表的名字"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, "db_info.json")

    with open(json_file_path, "r", encoding="utf-8") as f:
        db_data = json.load(f)

    db_name = db_data.get("name", db_data.get("id", "unknown"))
    tables = db_data.get("tables", {})
    table_names = list(tables.keys())

    db_info = f"Database Name: {db_name}\nTables: {', '.join(table_names)}"
    return db_info


def get_table_info(table_name, table_meta):
    """处理表的元数据信息，转换为英文格式"""
    n_records = table_meta.get("n_records", "Unknown")
    table_description = table_meta.get("description", "")

    table_info = f"Table Name: {table_name}\nNumber of Records: {n_records}"
    if table_description:
        table_info += f"\nDescription: {table_description}"

    return table_info


def get_column_info(col_name, col_meta):
    """处理列的元数据信息，转换为英文格式"""
    col_type = col_meta.get("type", "text")
    col_description = col_meta.get("description", "")

    column_info = f"Column Name: {col_name}\nData Type: {col_type}"
    if col_description:
        column_info += f"\nDescription: {col_description}"

    return column_info


def db_desc(sql):
    """
    生成数据库、表和列的描述信息
    
    Args:
        sql (str): SQL查询语句（当前版本暂未使用，预留参数）
        
    Returns:
        tuple: (数据库描述, 表描述, 列描述)
    """
    # 加载数据库信息
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, "db_info.json")

    with open(json_file_path, "r", encoding="utf-8") as f:
        db_data = json.load(f)

    # 获取数据库信息
    db_info = get_db_info()

    # 获取第一个表和第一个列作为示例
    tables = db_data.get("tables", {})
    if not tables:
        return "No tables found", "No tables found", "No columns found"

    table_name = list(tables.keys())[0]
    table_meta = tables[table_name]
    table_info = get_table_info(table_name, table_meta)

    columns = table_meta.get("columns", {})
    if not columns:
        return db_info, table_info, "No columns found"

    column_name = list(columns.keys())[0]
    column_meta = columns[column_name]
    column_info = get_column_info(column_name, column_meta)

    # 加载Jinja2模板环境
    env = load_jinja_env()
    db_template = env.get_template("db/db/default.jinja")
    table_template = env.get_template("db/table/default.jinja")
    column_template = env.get_template("db/column/default.jinja")

    # 渲染模板
    db_prompt = db_template.render(db_info=db_info)
    table_prompt = table_template.render(
        db_info=db_info,
        table_name=table_name,
        table_info=table_info
    )
    column_prompt = column_template.render(
        db_name=db_data.get("name", db_data.get("id", "unknown")),
        table_name=table_name,
        table_info=table_info,
        column_name=column_name,
        column_info=column_info
    )

    # 调用LLM获取响应
    llm = MockLLM()
    db_desc = llm.oracle(db_prompt)
    table_desc = llm.oracle(table_prompt)
    column_desc = llm.oracle(column_prompt)

    return db_desc, table_desc, column_desc
