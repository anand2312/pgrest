def sanitize_param(param: str) -> str:
    param = str(param)
    reserved_chars = ",.:()"
    if any(char in param for char in reserved_chars):
        return f"%22{param}%22"
    return param


def sanitize_pattern_param(pattern: str) -> str:
    return sanitize_param(
        pattern.replace("%", "*")
    )  # postgrest specifies to use * instead of %
