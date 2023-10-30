def input_error(msg):
    def actual_decorator(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (KeyError, ValueError, IndexError):
                return msg
        return inner
    return actual_decorator

