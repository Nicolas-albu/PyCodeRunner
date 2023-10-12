from fastapi import APIRouter

from ..core import PyExecuteCode, PyExecuteWithTests
from ..models import ModelRunCode, ModelRunWithTests

router = APIRouter()


@router.post("/run/tests")
async def post_run_with_tests(request: ModelRunWithTests):
    runner = PyExecuteWithTests(
        request.functionName,
        request.function,
        request.tests,
    )

    return {"result": runner.exec()}


@router.post("/run/code")
async def post_run_with_code(request: ModelRunCode):
    runner = PyExecuteCode(
        request.functionName,
        request.function,
        request.argument,
    )

    return {"result": runner.exec()}
