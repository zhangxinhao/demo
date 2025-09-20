CUTOFF_LENGTH_DEFAULT = 256


def value_repr(value, cutoff=CUTOFF_LENGTH_DEFAULT):
    """\
    Returns a string representation of the value, truncated to the specified length.

    Args:
        value: The value to be represented.
        cutoff: The maximum length of the string representation.
            If cutoff is negative, no truncation will be applied.

    Returns:
        A string representation of the value, truncated if necessary.
    """
    s = repr(value)
    return s if len(s) <= cutoff or cutoff < 0 else s[: cutoff - 3] + "..."
