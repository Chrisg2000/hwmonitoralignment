from ctypes import GetLastError, FormatError


def function_factory(function,
                     argument_types=None,
                     return_type=None,
                     error_checking=None):
    if argument_types is not None:
        function.argtypes = argument_types
    function.restype = return_type
    if error_checking is not None:
        function.errcheck = error_checking
    return function


def make_error(function, function_name=None, rcode=None):
    code = rcode if rcode else GetLastError()
    description = FormatError(code).strip()
    if function_name is None:
        function_name = function.__name__
    exception = WindowsError()
    exception.winerror = code
    exception.function = function_name
    exception.strerror = description
    return exception


def check_null_factory(function_name=None):
    def check_null(result, function, arguments, *args):
        if result is None:
            raise make_error(function, function_name)
        return result

    return check_null


check_null = check_null_factory()


def check_zero_factory(function_name=None):
    def check_zero(result, function, arguments, *args):
        if result == 0:
            raise make_error(function, function_name)
        return result

    return check_zero


check_zero = check_zero_factory()


def check_rcode_factory(function_name=None):
    def check_rcode(result, function, arguments, *args):
        if result != 0:
            raise make_error(function, function_name, result)
        return result

    return check_rcode


check_rcode = check_rcode_factory()


def check_false_factory(function_name=None):
    def check_false(result, function, arguments, *args):
        if not bool(result):
            raise make_error(function, function_name)
        return result

    return check_false


check_false = check_false_factory()
