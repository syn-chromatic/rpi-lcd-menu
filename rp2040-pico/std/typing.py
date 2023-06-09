class Callable:
    def __init__(self, args=None, result=None):
        self.args = args
        self.result = result

    def __call__(self, *args, **kwds):
        raise TypeError("Instances of Callable are not meant to be called directly.")

    @classmethod
    def __class_getitem__(cls, params):
        if not isinstance(params, tuple) or len(params) != 2:
            raise TypeError("Callable must be used as " "Callable[[arg, ...], result].")
        args, result = params
        if not isinstance(args, list):
            raise TypeError("Argument types must be provided in a list.")
        return cls(args, result)



