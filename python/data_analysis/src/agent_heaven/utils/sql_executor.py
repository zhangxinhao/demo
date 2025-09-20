# -*- coding: utf-8 -*-
import threading
from contextlib import contextmanager
from typing import List, Dict, Any, Optional

import psycopg2
from psycopg2 import pool

from agent_heaven.common.config.constants import DB_CONFIG
from agent_heaven.utils.logger import logger


class SQLExecutor:
    """SQL执行器，支持连接复用和并行调用"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._connection_pool = None
            self._pool_lock = threading.Lock()
            self._initialized = True

    def _get_connection_pool(self):
        """获取连接池，线程安全"""
        if self._connection_pool is None:
            with self._pool_lock:
                if self._connection_pool is None:
                    try:
                        # 创建连接池，最小连接数2，最大连接数20
                        self._connection_pool = psycopg2.pool.ThreadedConnectionPool(
                            minconn=5,
                            maxconn=20,
                            **DB_CONFIG
                        )
                        logger.info("数据库连接池已创建")
                    except psycopg2.Error as e:
                        logger.error(f"创建数据库连接池失败: {e}")
                        raise
        return self._connection_pool

    @contextmanager
    def _get_connection(self):
        """安全获取和释放数据库连接的上下文管理器"""
        connection_pool = self._get_connection_pool()
        conn = None
        try:
            conn = connection_pool.getconn()
            yield conn
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            logger.error(f"数据库操作错误: {e}")
            raise
        finally:
            if conn:
                connection_pool.putconn(conn)

    def execute_query(self, sql: str) -> Optional[List[Dict[str, Any]]]:
        """执行SQL查询并返回结果数据 - 线程安全版本"""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    column_names = [desc[0] for desc in cursor.description] if cursor.description else []
                    rows = cursor.fetchall()

                    result = []
                    for row in rows:
                        row_dict = dict(zip(column_names, row))
                        result.append(row_dict)

                    conn.commit()
                    return result

        except psycopg2.Error as e:
            logger.error(f"SQL执行错误: {e}, SQL: {sql}")
            return None
        except Exception as e:
            logger.error(f"执行SQL时发生未知错误: {e}, SQL: {sql}")
            return None

    def close_connection(self):
        """关闭数据库连接池"""
        if self._connection_pool:
            self._connection_pool.closeall()
            self._connection_pool = None
            logger.info("数据库连接池已关闭")

    def __del__(self):
        """析构函数，确保连接被关闭"""
        self.close_connection()


# 创建全局执行器实例
_executor = SQLExecutor()


def execute_sql(sql: str) -> Optional[List[Dict[str, Any]]]:
    """执行SQL查询的便捷函数"""
    return _executor.execute_query(sql)


def close_sql_connection():
    """关闭SQL连接的便捷函数"""
    _executor.close_connection()
