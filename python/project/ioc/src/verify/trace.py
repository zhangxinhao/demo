import contextvars
import logging
import uuid
from functools import wraps

# 创建context变量
trace_id_var = contextvars.ContextVar('trace_id', default=None)


def generate_trace_id():
    """生成唯一的trace_id"""
    return str(uuid.uuid4())


def set_trace_id(trace_id=None):
    """设置trace_id"""
    if trace_id is None:
        trace_id = generate_trace_id()
    trace_id_var.set(trace_id)
    return trace_id


def get_trace_id():
    """获取当前的trace_id"""
    return trace_id_var.get()


# 自定义日志格式化器
class TraceIdFormatter(logging.Formatter):
    def format(self, record):
        record.trace_id = get_trace_id() or 'N/A'
        return super().format(record)


# 配置日志
def setup_logging():
    handler = logging.StreamHandler()
    formatter = TraceIdFormatter(
        '%(asctime)s - [%(trace_id)s] - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


logger = setup_logging()


# 装饰器：自动为函数添加trace_id
def with_trace_id(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if get_trace_id() is None:
            set_trace_id()
        logger.info(f"Entering {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"Exiting {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise

    return wrapper


# 使用示例
@with_trace_id
def service_a():
    logger.info("Service A processing")
    service_b()


def service_b():
    logger.info("Service B processing")
    service_c()


def service_c():
    logger.info("Service C processing")


# 测试
if __name__ == "__main__":
    service_a()
    logger.info("Service A done")
    service_a()
