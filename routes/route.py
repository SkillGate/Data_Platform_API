from fastapi import APIRouter, Request, Query
from schema.schemas import affindaPDF
from schema.gitHubSchemas import gitHubOutsideCollaborators
from config.database import collection_name


router = APIRouter()

@router.get("/uploadfile")
async def upload_file(fileUrl: str = Query(..., description="Description of param1")):
    result  = affindaPDF(fileUrl=fileUrl)
    return result;

# GET Request Method
@router.get("/health")
async def get_todos():
    # todos = list_serial(collection_name.find())
    return "Health Endpoint";

@router.get("/gitHub/outsideCollaborators")
async def upload_file(gitHubUrl: str = Query(..., description="Description of param1")):
    try:
        result = gitHubOutsideCollaborators(gitHubUrl=gitHubUrl)
        return result
    except Exception as e:
        return {"error": str(e)}