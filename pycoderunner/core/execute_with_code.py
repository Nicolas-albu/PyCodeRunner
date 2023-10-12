from typing import Any, List


class PyExecuteCode:
    def __init__(
        self,
        function_name: str,
        function: str,
        argument: List[Any],
        /,
    ):
        self.__function_name = function_name
        self.__function = function
        self.__argument = argument

    def exec(self):
        namespace = {}
        exec(self.__function, namespace)

        return namespace[self.__function_name](*self.__argument)
