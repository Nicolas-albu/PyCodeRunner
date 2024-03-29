from typing import Dict, List

from ..error import TestCaseException


class PyExecuteWithTests:
    def __init__(
        self,
        function_name: str,
        function: str,
        tests: List[Dict[str, str]],
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
        self.__tests = tests

    @classmethod
    def convert_type(cls, value: str):
        # Check for float values
        if "." in value:
            try:
                return float(value)
            except ValueError:
                ...

        # Check for integer values
        elif value.lstrip("-").isdigit() or (
            value.startswith("-") and value[1:].isdigit()
        ):
            try:
                return int(value)
            except ValueError:
                ...

        # Check for boolean values
        elif value.lower() == "true":
            return True

        elif value.lower() == "false":
            return False

        # Check for single-quoted or double-quoted string
        elif (value.startswith("\'") and value.endswith("\'")) or (
            value.startswith('\"') and value.endswith('\"')
        ):
            return value[1:-1]  # Remove the quotes

        # Check for tuple, list, and dictionary structures
        elif value.startswith("(") and value.endswith(")"):
            # Try to convert to tuple
            try:
                elements = value[1:-1].split(",")
                return tuple(
                    cls.convert_type(element.strip()) for element in elements
                )
            except Exception:
                ...

        elif value.startswith("[") and value.endswith("]"):
            # Try to convert to list
            try:
                elements = value[1:-1].split(",")
                return [
                    cls.convert_type(element.strip()) for element in elements
                ]
            except Exception:
                ...

        elif value.startswith("{") and value.endswith("}"):
            # Try to convert to dictionary
            try:
                elements = value[1:-1].split(",")
                key_value_pairs = [element.split(":") for element in elements]
                return {
                    cls.convert_type(key.strip()): cls.convert_type(
                        value.strip()
                    )
                    for key, value in key_value_pairs
                }
            except Exception:
                ...

        # Return the original value if no conversion succeeds
        return value

    def exec(self) -> bool | str:
        try:
            # Create a code object
            code_obj = compile(self.__function, "<string>", "exec")

            # Execute the code within a namespace
            namespace = {}
            exec(code_obj, namespace)

            if self.__tests:
                for index, test in enumerate(self.__tests):
                    _input, output = [*test.items()][0]

                    # Split the input by commas and strip whitespace
                    _input = _input.split(",")
                    _input = [value.strip() for value in _input]

                    # Convert the input to the correct type using convert_type
                    arguments = [self.convert_type(value) for value in _input]

                    # Gets the execution result
                    result = namespace[self.__fn_name](*arguments)

                    if str(result) != output:
                        message = f"Erro no caso de teste {index + 1}"
                        raise TestCaseException(message)
            else:
                return namespace[self.__fn_name]()

        except Exception as err:
            print(err.__class__)
            return f"{err}"

        return True
