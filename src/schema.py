from pydantic import BaseModel
from typing import List,Optional, Dict

class ModelInput(BaseModel):
    application_url: str
    doc_path: str

class SingleModule(BaseModel):
    id: str
    name: str

class ModelOutput(BaseModel):
    modules : List[SingleModule]

