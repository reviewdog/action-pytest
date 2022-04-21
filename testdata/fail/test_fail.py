"""Fail tests."""

import pytest

from . import fail


class TestFail:
    """Tests for the fails."""

    @pytest.mark.doesnotexist(99)
    def test_fail_sum(self):
        """Test fail_sum."""
        a = 5
        b = 4
        fail_sum = fail.fail_sum(a, b)

        assert fail_sum == a + b

    @pytest.mark.timeout(5)
    def test_fail_recursive_fib(self):
        """Test fail_recursive_fib."""
        n = 20

        fib = fail.fail_recursive_fib(n)

        assert fib == 6765
