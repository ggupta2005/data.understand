import timeit

SEPARATOR_LENGTH = 120


def measure_time(compute_func):
    def compute_wrapper(*args, **kwargs):
        print(get_separator(SEPARATOR_LENGTH))
        start_time = timeit.default_timer()
        result = compute_func(*args, **kwargs)
        elapsed = timeit.default_timer() - start_time
        m, s = divmod(elapsed, 60)
        print("Time taken: {0} min {1} sec".format(m, s))
        print(get_separator(SEPARATOR_LENGTH))
        return result

    return compute_wrapper


def get_separator(max_len: int) -> str:
    return "=" * max_len
