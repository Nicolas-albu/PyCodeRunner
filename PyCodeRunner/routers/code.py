from fastapi import APIRouter

from ..core import PyCodeCore
from ..models import ModelCode

router = APIRouter()


@router.get("/codes/")
async def execution_code(request: ModelCode):
    runner = PyCodeCore(
        request.functionName,
        request.function,
        request.outputType,
        request.tests,
    )

    return {"result": runner.exec()}
