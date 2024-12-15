from fastapi import APIRouter
from src.utils import extract_all_functionalies_testcases,ModelInput,ModelOutput
import time


router = APIRouter()


@router.post("/quality_analyst_report")
async def extract_qa_report(application_input: ModelInput) -> dict:
    result= dict()
    result = extract_all_functionalies_testcases(application_input)
    # except Exception as e:
    #     print(e)
    #     result={"error":f"Error : {e}","result":""}
    return result




