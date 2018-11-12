import functools

# while we want to keep this miminal, the common class contains some useful functions usable by many providers.

def memoize(func):
    """
    The second time the decorated function is called, return the previous response value
    versus calling the function.
    """
    cache = func.cache = {}
    @functools.wraps(func)
    def memoized_func(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return memoized_func

