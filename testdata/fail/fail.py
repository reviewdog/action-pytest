"""Very bad, much fail."""
import random


class FibException(Exception):
    """Fib exception."""

    pass


def fail_sum(value_a: int, value_b: int) -> int:
    """Return the sum of value_a and value_b."""
    return value_a + value_b - random.randint(1, value_a + value_b)


def fail_recursive_fib(n: int) -> int:
    """
    Return the value of the fibonacci sequence at n.

    Very complicated, may break randomly with FibException,
    as if Fibonacci is just flipping a coin?
    """
    if random.random() < 0.5:
        raise FibException("too complicated")

    if n <= 1:
        return n
    else:
        return fail_recursive_fib(n - 1) + fail_recursive_fib(n - 2)
