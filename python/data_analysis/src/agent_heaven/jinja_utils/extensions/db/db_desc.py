import json
import os

from agent_heaven.jinja_utils.utils.jinja_utils import load_jinja_env
from agent_heaven.jinja_utils.utils.llm_utils import MockLLM


def get_db_info(db_data):
    """字符串拼接DB表当中的所有表的名字"""
    db_name = db_data.get("name", db_data.get("id", "unknown"))
    tables = db_data.get("tables", {})
    table_names = list(tables.keys())

    db_info = f"Database Name: {db_name}\nTables: {', '.join(table_names)}"
    return db_info


def get_table_info(table_name, table_meta):
    """处理表的元数据信息，转换为英文格式"""
    n_records = table_meta.get("n_records", "Unknown")
    table_info = f"Table Name: {table_name}\nNumber of Records: {n_records}"

    return table_info


def get_column_info(col_name, col_meta):
    """处理列的元数据信息，转换为英文格式"""
    col_type = col_meta.get("type", "text")
    column_info = f"Column Name: {col_name}\nData Type: {col_type}"

    return column_info


def db_desc():
    """
    生成数据库、表和列的描述信息

    Returns:
        dict: 包含数据库、表和列描述的字典
        {
            "database": {
                "description": "数据库描述"
            },
            "tables": {
                "table_name": {
                    "description": "表描述",
                    "columns": {
                        "column_name": "列描述",
                        ...
                    }
                },
                ...
            }
        }
    """
    # 加载数据库信息
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, "db_info.json")

    with open(json_file_path, "r", encoding="utf-8") as f:
        db_data = json.load(f)

    # 获取数据库信息
    db_info = get_db_info(db_data)
    db_name = db_data.get("name", db_data.get("id", "unknown"))

    # 加载Jinja2模板环境
    env = load_jinja_env()
    db_template = env.get_template("db/db/default.jinja")
    table_template = env.get_template("db/table/default.jinja")
    column_template = env.get_template("db/column/default.jinja")

    # 初始化LLM
    llm = MockLLM()

    # 准备结果字典
    result = {
        "database": {},
        "tables": {}
    }

    # 生成数据库描述
    db_prompt = db_template.render(db_info=db_info)
    result["database"]["description"] = llm.oracle(db_prompt)

    # 遍历所有表
    tables = db_data.get("tables", {})
    if not tables:
        result["tables"] = {"error": "No tables found"}
        return result

    for table_name, table_meta in tables.items():
        print(f"处理表: {table_name}")

        # 获取表信息
        table_info = get_table_info(table_name, table_meta)

        # 生成表描述
        table_prompt = table_template.render(
            db_info=db_info,
            table_name=table_name,
            table_info=table_info
        )
        table_desc = llm.oracle(table_prompt)

        # 初始化表结果
        result["tables"][table_name] = {
            "description": table_desc,
            "columns": {}
        }

        # 遍历表中的所有列
        columns = table_meta.get("columns", {})
        if not columns:
            result["tables"][table_name]["columns"] = {"error": "No columns found"}
            continue

        for column_name, column_meta in columns.items():
            print(f"  处理列: {column_name}")

            # 获取列信息
            column_info = get_column_info(column_name, column_meta)

            # 生成列描述
            column_prompt = column_template.render(
                db_name=db_name,
                table_name=table_name,
                table_info=table_info,
                column_name=column_name,
                column_info=column_info
            )
            column_desc = llm.oracle(column_prompt)

            # 存储列描述
            result["tables"][table_name]["columns"][column_name] = column_desc

    return result


if __name__ == '__main__':
    db_desc()
