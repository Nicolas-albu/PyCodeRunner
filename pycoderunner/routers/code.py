from fastapi import APIRouter

from ..core import PyCodeCore
from ..models import ModelCode

router = APIRouter()


@router.post("/codes/")
async def execution_code(request: ModelCode):
    runner = PyCodeCore(
        request.functionName,
        request.function,
        request.tests,
    )

    return {"result": runner.exec()}
