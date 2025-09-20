import os
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''

from agent_heaven.utils.sql_executor import execute_sql

if __name__ == '__main__':
    # 使用一个肯定返回空结果的查询
    sql = "SELECT 1 as num WHERE 1 = 0"
    result = execute_sql(sql)

    print(f"执行SQL: {sql}")
    print(f"返回结果: {result}")
    print(f"结果类型: {type(result)}")
