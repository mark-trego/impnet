def assert_almost_zero(x, epsilon=1e-9):
    if abs(x) > epsilon:
        raise AssertionError()

def assert_lists_almost_equal(a, b, epsilon=1e-9):
    if not len(a) == len(b):
        raise AssertionError("The list lengths differ")

    for x, y in zip(a, b):
        assert_almost_zero(x - y)
