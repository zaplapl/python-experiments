def curry_vector(a):
    # 1
    def line(b=0):
        #  b = 0
        def compute(x):
            # 1 + 0 * xi for xi in x
            return [a + b * xi for xi in x]

        # return function w a + b as local vars
        return compute

    # return a callable that returns a callable
    # that returns the result of the computation
    return line


# set values for a for inner computation
base_func = curry_vector(
    10
)  # is a callable that returns a callable that returns the results of the computation

# base_func is line in the sense that calling it with no args will return compute (the function)

# with the value of b set in the computation

inner_callable = base_func()  # b = 0, returns compute'

inner_callable([2, 3, 4])  # returns 10 + 0 * x for x in *args


def draw_vector(a, b, points):
    return [a + b * xi for xi in points]


# also recursive partial application
from functools import partial
from inspect import signature


def mult(x, y, z):
    return x * y * z


mult_10 = partial(mult, 10)
mult_10_20 = partial(mult_10, 20)
print(mult_10_20(30))


def curry(func):
    def inner(arg):
        # checking if the function has one argument,
        # then return function as it is
        if len(signature(func).parameters) == 1:
            return func(arg)

        return curry(partial(func, arg))

    return inner


# using cuury function on the previous example function
@curry
def mult(x, y, z):
    return x * y * z


print(mult(10)(20)(30))


from typing import Callable, Generic, TypeVar, Union

ReturnType = TypeVar("ReturnType")


class Partial(Generic[ReturnType]):
    """Represents a partial function application. `fn` is the function being
    wrapped, and the args and kwargs are the saved ones from previous calls.
    """

    def __init__(
        self, num_args: int, fn: Callable[..., ReturnType], *args, **kwargs
    ) -> None:
        self.num_args = num_args
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def __call__(
        self, *more_args, **more_kwargs
    ) -> Union[Partial[ReturnType], ReturnType]:
        all_args = self.args + more_args  # tuple addition
        all_kwargs = dict(**self.kwargs, **more_kwargs)  # non-mutative dictionary union
        num_args = len(all_args) + len(all_kwargs)
        if num_args >= self.num_args:
            return self.fn(*all_args, **all_kwargs)
        else:
            return Partial(self.num_args, self.fn, *all_args, **all_kwargs)

    def __repr__(self):
        return f"Partial({self.fn}, args={self.args}, kwargs={self.kwargs})"


def curry(num_args: int) -> Callable[[Callable[..., ReturnType]], Partial[ReturnType]]:
    """Curries the decorated function. Instead of having to provide all arguments
    at once, they can be provided one or a few at a time. Once at least `num_args`
    arguments are provided, the wrapped function will be called. The doctests below
    best illustrate its use.

    The decorator returns a `Partial` object, which represents a partial application
    of `fn`. This object is callable. It stores the arguments provided thus far, and
    after receiving at least `num_args` arguments, it calls `fn`, otherwise it returns
    another `Partial` object representing the partial progress made.

    >>> @curry(num_args=3)
    ... def add(a, b, c):
    ...     return a + b + c
    >>> add5 = add(5)
    >>> add7 = add5(2)

    You can still call the function without currying.
    >>> add(1, 2, 3)
    6

    This is not "real" currying, but it allows passing more complex state,
    so I'd say this is in the spirit of currying and should be legal.
    >>> add5(4, 3)
    12
    >>> add(1)(2, 3)
    6
    >>> add(1, 2)(3)
    6

    Strict currying:
    >>> add5(4)(3)
    12
    >>> add7(2)
    9
    >>> add(1)(2)(3)
    6

    It is okay to have some default arguments. Notice that the wrapped function
    `make_email` takes up to three arguments, but gets called when at least two
    are provided.
    >>> @curry(num_args=2)
    ... def make_email(username, domain, separator="@"):
    ...     return username + separator + domain
    >>> make_gmail = make_email(domain="gmail.com")
    >>> make_gmail("haskell")
    'haskell@gmail.com'
    >>> make_gmail(username="curry")
    'curry@gmail.com'
    >>> make_gmail("curry", separator=">>=")
    'curry>>=gmail.com'
    >>> make_email("haskell", "curry.com")
    'haskell@curry.com'
    >>> make_email("haskell")("curry.com", ">>=")
    'haskell>>=curry.com'

    Note that I did consider using `inspect.signature` instead of using `num_args`,
    but I chose the latter for making my code less verbose, since my objective here
    is to show how one can curry functions elegantly in Python, and not to write
    a bulletproof currying function that can handle all of Python's wonders. And
    even then I think this is a very useful and flexible function.

    Parameters
    ----------
    num_args    number of arguments to wait for before evaluating wrapped function

    Returns
    -------
    a decorator that curries a function
    """

    def decorator(fn: Callable[..., ReturnType]):
        return Partial(num_args, fn)

    return decorator


def curry_functional(num_args: int):
    """Curries the decorated function. Instead of having to provide all arguments
    at once, they can be provided one or a few at a time. Once at least `num_args`
    arguments are provided, the wrapped function will be called. The doctests below
    best illustrate its use.

    This is a purely functional implementation, not relying on any user-defined
    classes. This fundamentally does the same thing as the implementation with
    `Partial`, and I deliberately named the private functions `init` and `call`
    to highlight their similarities to `Partial.__init__` and `Partial.__call__`.

    >>> @curry_functional(num_args=3)
    ... def add(a, b, c):
    ...     return a + b + c
    >>> add5 = add(5)
    >>> add7 = add5(2)

    You can still call the function without currying.
    >>> add(1, 2, 3)
    6

    This is not "real" currying, but it allows passing more complex state,
    so I'd say this is in the spirit of currying and should be legal.
    >>> add5(4, 3)
    12
    >>> add(1)(2, 3)
    6
    >>> add(1, 2)(3)
    6

    Strict currying:
    >>> add5(4)(3)
    12
    >>> add7(2)
    9
    >>> add(1)(2)(3)
    6

    It is okay to have some default arguments. Notice that the wrapped function
    `make_email` takes up to three arguments, but gets called when at least two
    are provided.
    >>> @curry_functional(num_args=2)
    ... def make_email(username, domain, separator="@"):
    ...     return username + separator + domain
    >>> make_gmail = make_email(domain="gmail.com")
    >>> make_gmail("haskell")
    'haskell@gmail.com'
    >>> make_gmail(username="curry")
    'curry@gmail.com'
    >>> make_gmail("curry", separator=">>=")
    'curry>>=gmail.com'
    >>> make_email("haskell", "curry.com")
    'haskell@curry.com'
    >>> make_email("haskell")("curry.com", ">>=")
    'haskell>>=curry.com'

    Parameters
    ----------
    num_args    number of arguments to wait for before evaluating wrapped function

    Returns
    -------
    a decorator that curries a function
    """

    def decorator(fn: Callable[..., ReturnType]):
        def init(*args, **kwargs):
            def call(*more_args, **more_kwargs):
                all_args = args + more_args
                all_kwargs = dict(**kwargs, **more_kwargs)
                if len(all_args) + len(all_kwargs) >= num_args:
                    return fn(*all_args, **all_kwargs)
                else:
                    return init(*all_args, **all_kwargs)

            return call

        return init()

    return decorator
