class abstractmethod:
    def __init__(self, func):
        self.func = func

    def __call__(self, *_, **__):
        func_name = self.func.__name__
        raise NotImplementedError(
            f"Abstract method {func_name} must be implemented by subclass"
        )


class ABC:
    _checked = False

    def __new__(cls, *_, **__):
        if not cls._checked:
            cls._validate_abstract()
            cls._checked = True
        return super(ABC, cls).__new__(cls)

    @staticmethod
    def _join_methods(methods: list[str]) -> str:
        return ", ".join(methods)

    @classmethod
    def _validate_abstract(cls):
        non_instantiated = cls._get_non_instantiated()
        if non_instantiated:
            methods = cls._join_methods(non_instantiated)
            error = f"Can't instantiate abstract class {cls.__name__} \
                with abstract methods {methods}."
            raise TypeError(error)

    @classmethod
    def _get_non_instantiated(cls) -> list[str]:
        non_instantiated = []
        for name in dir(cls):
            val = getattr(cls, name)
            if isinstance(val, abstractmethod):
                non_instantiated.append(name)
        return non_instantiated
