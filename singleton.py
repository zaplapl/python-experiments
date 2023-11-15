# materials based off of  https://python-patterns.guide/gang-of-four/singleton/
# cf Global object
# namespaces different
################################################################################################################
# c++ 'translation' into Python:
class CPlusPlusLogger(object):
    _instance = None

    def __init__(self):
        # similar to c++: log = new Logger()
        # it would be possible to return a compile time error for calling `new` in C++ by marking class constructor as
        # protected/private.
        raise RuntimeError("Call instance() instead")

    @classmethod
    def instance(cls):
        if cls._instance is None:
            print("Creating new instance of C++ Logger")
            cls._instance = cls.__new__(cls)
            # Put any initialization here.
        return cls._instance


################################################################################################################
# a more pythonic approach
class Logger(object):
    """
    Many other design patterns in Python:
    e.g. using a Metaclass
    class Singleton(type):
        _instances = {}
        def __call__(cls, *args, **kwargs):
            if cls not in cls._instances:
                cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            return cls._instances[cls]
    class Logger(metaclass=Singleton):
        pass
    https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Creating the Logger object")
            cls._instance = super(Logger, cls).__new__(
                cls
            )  # 1st argument passed into super() indicates which parent in the MRO it is accessing the methods of.
            # Put any initialization here.
        return cls._instance


print(f"class id {id(Logger)}")
print(f"instance id {id(Logger())}")


if __name__ == "__main__":
    cpp_log1 = CPlusPlusLogger.instance()
    cpp_log2 = CPlusPlusLogger.instance()
    print(cpp_log1)
    print("Are the two C++ Loggers the same object?", cpp_log1 is cpp_log2)
    log1 = Logger()
    log2 = Logger()
    print("Are the two Loggers the same object?", log1 is log2)
    # Advantages:
    # Encapsulation. Avoid crowding out the global namespace.
    # loggers feel like a "natural" use for singletons. As the various users are not changing the loggers
    #   in ways other users will care about, there is not really shared state.
    #   This negates the primary argument against the singleton pattern,
    #   and makes them a reasonable choice because of their ease of use for the task.
    # Other use cases: https://stackoverflow.com/questions/392160/what-are-some-concrete-use-cases-for-metaclasses
    # Drawbacks:
    # Logger() appears to be creating a new object given how we're used to seeing it in Python
    # Is the object actually, logically a singleton?
    # Use global variables in a module instead, and consider the module as the singleton https://stackoverflow.com/questions/31875/is-there-a-simple-elegant-way-to-define-singletons
    # -> see Python docs in support of this practice https://docs.python.org/3/faq/programming.html#how-do-i-share-global-variables-across-modules
    #
