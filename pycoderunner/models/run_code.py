import re
from typing import Any, List

from pydantic import BaseModel, validator


class ModelRunCode(BaseModel):
    functionName: str
    function: str
    argument: List[Any]

    @validator("function")
    def contain(cls, _function_value: str) -> str:
        _imports_pattern = (
            r"(import|from)\s+(os|subprocess|shutil|tempfile|ctypes|psutil|"
            r"getpass|platform|sys)\b"
        )

        _builtins_pattern = r"(eval|exec|breakpoint|callable|compile)\b"

        if re.findall(_imports_pattern, _function_value) or re.findall(
            _builtins_pattern, _function_value
        ):
            raise ValueError()

        return _function_value
