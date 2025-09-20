CUTOFF_LENGTH_DEFAULT = 256  # 默认截断长度


def value_repr(value, cutoff=CUTOFF_LENGTH_DEFAULT):
    """
    返回值的字符串表示，截断到指定长度。

    参数:
        value: 需要表示的值
        cutoff: 字符串表示的最大长度
            如果cutoff为负数，则不进行截断

    返回:
        值的字符串表示，必要时进行截断
    """
    s = repr(value)
    return s if len(s) <= cutoff or cutoff < 0 else s[: cutoff - 3] + "..."
