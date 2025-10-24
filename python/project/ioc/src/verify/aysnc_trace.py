import asyncio
import contextvars
import threading
import time
from datetime import datetime

# 创建上下文变量
trace_id_var = contextvars.ContextVar('trace_id', default=None)
user_id_var = contextvars.ContextVar('user_id', default='anonymous')


# ============================================
# 示例 1: 基本使用
# ============================================
def example_basic():
    print("=== 基本使用示例 ===")

    # 设置值
    token = trace_id_var.set('trace-12345')
    print(f"设置后的值: {trace_id_var.get()}")

    # 重置值
    trace_id_var.reset(token)
    print(f"重置后的值: {trace_id_var.get()}")  # 返回 None (默认值)

    print()


# ============================================
# 示例 2: 异步环境中的上下文隔离
# ============================================
async def process_request(request_id: str, user: str):
    """模拟处理一个请求"""
    # 为当前协程设置上下文变量
    trace_id_var.set(request_id)
    user_id_var.set(user)

    print(f"[{request_id}] 开始处理请求，用户: {user}")

    # 模拟异步操作
    await asyncio.sleep(0.1)
    await log_operation("数据库查询")

    await asyncio.sleep(0.1)
    await log_operation("API调用")

    print(f"[{request_id}] 请求处理完成\n")


async def log_operation(operation: str):
    """记录操作，自动获取当前上下文的 trace_id"""
    trace_id = trace_id_var.get()
    user_id = user_id_var.get()
    print(f"  [{trace_id}] 用户 {user_id} 执行: {operation}")


async def example_async():
    print("=== 异步环境示例 ===")
    # 并发处理多个请求，每个请求有独立的上下文
    await asyncio.gather(
        process_request("REQ-001", "Alice"),
        process_request("REQ-002", "Bob"),
        process_request("REQ-003", "Charlie")
    )


# ============================================
# 示例 3: 多线程环境
# ============================================
def thread_worker(thread_id: int):
    """线程工作函数"""
    trace_id = f"THREAD-{thread_id:03d}"
    trace_id_var.set(trace_id)

    for i in range(3):
        current_trace = trace_id_var.get()
        print(f"线程 {thread_id}: trace_id = {current_trace}, 迭代 {i + 1}")
        time.sleep(0.05)


def example_threading():
    print("=== 多线程环境示例 ===")
    threads = []
    for i in range(3):
        t = threading.Thread(target=thread_worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    print()


# ============================================
# 示例 4: Web 框架中的实际应用
# ============================================
class RequestContext:
    """模拟 Web 请求上下文管理器"""

    def __init__(self, trace_id: str, user_id: str):
        self.trace_id = trace_id
        self.user_id = user_id
        self.tokens = []

    def __enter__(self):
        # 进入上下文时设置变量
        self.tokens.append(trace_id_var.set(self.trace_id))
        self.tokens.append(user_id_var.set(self.user_id))
        return self

    def __exit__(self, *args):
        # 退出上下文时恢复变量
        for token in reversed(self.tokens):
            contextvars.ContextVar.reset(token)


def business_logic():
    """业务逻辑函数，自动使用上下文中的 trace_id"""
    trace_id = trace_id_var.get()
    user_id = user_id_var.get()
    print(f"  执行业务逻辑 [trace: {trace_id}, user: {user_id}]")


def example_web_framework():
    print("=== Web 框架应用示例 ===")

    # 模拟处理多个请求
    with RequestContext("WEB-REQ-001", "user_alice"):
        print("处理请求 1:")
        business_logic()

    with RequestContext("WEB-REQ-002", "user_bob"):
        print("处理请求 2:")
        business_logic()

    print()


# ============================================
# 示例 5: 嵌套上下文
# ============================================
def example_nested_context():
    print("=== 嵌套上下文示例 ===")

    print(f"初始值: {trace_id_var.get()}")

    # 第一层
    token1 = trace_id_var.set("LEVEL-1")
    print(f"第一层: {trace_id_var.get()}")

    # 第二层
    token2 = trace_id_var.set("LEVEL-2")
    print(f"第二层: {trace_id_var.get()}")

    # 第三层
    token3 = trace_id_var.set("LEVEL-3")
    print(f"第三层: {trace_id_var.get()}")

    # 逐层恢复
    trace_id_var.reset(token3)
    print(f"恢复到第二层: {trace_id_var.get()}")

    trace_id_var.reset(token2)
    print(f"恢复到第一层: {trace_id_var.get()}")

    trace_id_var.reset(token1)
    print(f"恢复到初始: {trace_id_var.get()}")
    print()


# ============================================
# 示例 6: 实用工具函数
# ============================================
def get_current_trace_id() -> str:
    """获取当前 trace_id，如果没有则生成一个"""
    trace_id = trace_id_var.get()
    if trace_id is None:
        trace_id = f"AUTO-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        trace_id_var.set(trace_id)
    return trace_id


def example_utility():
    print("=== 实用工具函数示例 ===")

    # 第一次调用，自动生成
    print(f"第一次获取: {get_current_trace_id()}")

    # 第二次调用，返回已有的
    print(f"第二次获取: {get_current_trace_id()}")

    print()


# ============================================
# 运行所有示例
# ============================================
if __name__ == "__main__":
    example_basic()
    example_nested_context()
    example_utility()
    example_threading()
    example_web_framework()

    # 异步示例需要单独运行
    print("运行异步示例...")
    asyncio.run(example_async())
