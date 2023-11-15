class ErrorMessage:
    base_error_message = {"error_code": "", "error_message": {}, "details": {}}

    def __init__(self, attribute, *args):
        # set error code here

        return getattr(self, attribute)(*args)

    def simple_message(self, args):
        self.base_error_message["error_message"] = "simple error message"
        return self.base_error_message

    def complex_message(self, one_thing, another_thing):
        self.base_error_message["error_message"] = "complex error message"
        self.base_error_message["details"]["one_thing"] = one_thing
        self.base_error_message["details"]["another_thing"] = another_thing
        return self.base_error_message
