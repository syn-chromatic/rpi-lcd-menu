# class abstractmethod:
#     def __init__(self, func):
#         self.func = func

#     def __call__(self, *_, **__):
#         raise NotImplementedError(
#             "Abstract method %s must be implemented by subclass" % self.func.__name__
#         )


# class ABC:
#     def __new__(cls, *_, **__):
#         cls._validate_abstract()
#         return super(ABC, cls).__new__(cls)

#     @staticmethod
#     def _join_methods(methods: list[str]) -> str:
#         string = ""
#         len_methods = len(methods) - 1
#         for idx, method in enumerate(methods):
#             string += method
#             if idx != len_methods:
#                 string += ", "
#         return string

#     @classmethod
#     def _validate_abstract(cls):
#         non_instantiated = cls._get_non_instantiated()
#         if non_instantiated:
#             methods = cls._join_methods(non_instantiated)
#             error_seg1 = "Can't instantiate abstract class %s " % cls.__name__
#             error_seg2 = "with abstract methods %s." % methods
#             error = error_seg1 + error_seg2
#             raise TypeError(error)

#     @classmethod
#     def _get_non_instantiated(cls) -> list[str]:
#         non_instantiated = []
#         for name in dir(cls):
#             val = getattr(cls, name)
#             if isinstance(val, abstractmethod):
#                 non_instantiated.append(name)
#         return non_instantiated


class abstractmethod:
    "Dummy abstractmethod wrapper."


class ABC:
    "Dummy ABC type."
