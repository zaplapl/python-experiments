import socket
import random
import time
import array
from functools import reduce
from ipaddress import IPv4Address


def f1(list):
    """
    Me like code
    """
    string = ""
    for item in list:
        string += chr(item)
    return string


def f2(list):
    """
    Create function call frames for each conversion
    """
    return reduce(lambda string, item: string + chr(item), list, "")


def f3(list):
    """
    Double space complexity (return value of map() call is another array
    of len == len(list))

    Double the number of loops (for ... in + map())

    Call to chr happens "under the hood"
    """
    string = ""
    for character in map(chr, list):
        string = string + character
    return string


def f4(list):
    """
    Mentioned as an optimisation for Python 2

    No longer delivers improved performance
    """
    string = ""
    lchr = chr
    for item in list:
        string = string + lchr(item)
    return string


def f5(list):
    """
    Compare long && short strings
    """
    string = ""
    for i in range(0, 256, 16):  # 0, 16, 32, 48, 64, ...
        s = ""
        for character in map(chr, list[i : i + 16]):
            s = s + character
        string = string + s
    return string


def f6(list):
    """
    No loops for you
    """
    return "".join(map(chr, list))


def f7(list):
    """
    Back to builtins (input list)
    """
    return array.array("B", list).tobytes().decode("utf-8")


def f8(bytes):
    """
    Back to builtins (input bytes object)
    """
    return bytes.decode("utf-8")


def banner_grab():
    banner = b""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        message = b"GET HTTP/1.1"
        host = str(IPv4Address(random.randint(1234, 2**32)))
        print(f"trying {host}")
        sock.sendto(message, (str(IPv4Address(host)), 443))

        banner = sock.recv(1024)
        sock.close()
    except:
        if not banner:
            banner_grab()

    return banner


import time


def timing(f, n, a):
    print(f.__name__)
    r = range(n)
    t1 = time.perf_counter()
    for i in r:
        f(a)
        f(a)
        f(a)
        f(a)
        f(a)
        f(a)
        f(a)
        f(a)
        f(a)
        f(a)
    t2 = time.perf_counter()
    print(round(t2 - t1, 3))


banner = b"nice work if you can get it"
