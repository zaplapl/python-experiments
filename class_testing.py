import sys
from types import ModuleType


class DictDescriptor:
    def __init__(self) -> None:
        self.descriptored_dicts = {}
        self.call_count = 0

    def __get__(self, instance, owner):
        breakpoint()
        return self.descriptored_dicts

    def __set__(self, instance, value):
        breakpoint()
        self.descriptored_dicts[repr(instance)] = {
            "instance": instance,
            "last_assignment": value,
        }
        computed_value = sum(
            instance_input
            for descriptored_dict in self.descriptored_dicts.values()
            for instance_input in descriptored_dict.shared_inputs
        )
        for opened_dicts in self.descriptored_dicts.values():
            opened_dicts.open_state = computed_value


descriptor = DictDescriptor()


class OpenDict(dict):
    """
    class property that hooks into its own access and assignment operations

    those operations are called with the class instance and type() (and therefore have access to class state)
    """

    dict_opener = DictDescriptor()

    def __init__(self, *init_ints):
        self["secret_dict"] = {}
        self.shared_inputs = init_ints if init_ints else []
        self.__name__ = "verbose"

    def __repr__(self):
        return f"dict_instance_{id(self)}"

    def __setattr__(self, attr, value):
        print(f"Setting {attr}...")
        super().__setattr__(attr, value)
