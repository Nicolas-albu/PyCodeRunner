from typing import Dict

from ..error import TestCaseException


class PyCodeCore:
    def __init__(
        self,
        function_name: str,
        function: str,
        output_type: str,
        tests: Dict[str, str],
    ):
        """Criação do Core da execução de códigos escritos em Python.

        Args:
            function_name (str): Nome da função a ser executada.
            function (str): Texto da função a ser executada.
            output_type (str): Tipo da saída da função.
            tests (Dict[str, str]): Dicionário de teste onde as chaves são os
                valores de entrada da função e seu valor correspondente o
                output da entrada.

        Example:
            >>> function = '''
            ... def _sum(*args):
            ...     return sum(args)
            ... '''
            >>> tests = {'1, 2, 3': '6'}
            >>> PyCodeCore('_sum', function, 'int', tests).exec()
            ... True
        """

        self.__fn_name = function_name
        self.__function = function
        self.__out_type = eval(
            output_type,
            {
                "__builtins__": {
                    "bool": bool,
                    "float": float,
                    "int": int,
                    "str": str,
                },
            },
        )
        self.__tests = tests

    def exec(self):
        try:
            for index, (inp, out) in enumerate(self.__tests.items()):
                namespace = {}
                exec(self.__function, namespace)
                inp = tuple(
                    _arg if (_arg := arg.strip()).isalpha() else float(_arg)
                    for arg in inp.split(",")
                )
                if str(self.__out_type(namespace[self.__fn_name](*inp))) != out:
                    raise TestCaseException(f"Erro no caso de teste {index + 1}")

        except Exception as err:
            print(err.__class__)
            return f"{err}"

        return True
