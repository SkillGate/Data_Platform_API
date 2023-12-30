from fastapi import APIRouter, Request, Query
from schema.schemas import affindaPDF
from schema.gitHubSchemas import github_collaborators_commit_count
from schema.gitHubSchemas import github_collaborators_commit_details
from schema.mediumBlogSchemas import extract_blogger_posts
from config.database import collection_name


router = APIRouter()

@router.get("/uploadfile")
async def upload_file(fileUrl: str = Query(..., description="Description of param1")):
    result  = affindaPDF(fileUrl=fileUrl)
    return result;

@router.get("/github/collaboratorscommitcount")
async def upload_file(gitHubUrl: str = Query(..., description="Description of param1")):
    try:
        result = github_collaborators_commit_count(gitHubUrl=gitHubUrl)
        return result
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/github/collaboratorscommmitdetails")
async def upload_file(gitHubUrl: str = Query(..., description="Description of param1")):
    try:
        result = github_collaborators_commit_details(gitHubUrl=gitHubUrl)
        return result
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/blogger/posts")
async def blogger_post(bloggerUrl: str = Query(..., description="Description of param1")):
    try:
        result = extract_blogger_posts(bloggerUrl=bloggerUrl)
        return result
    except Exception as e:
        return {"error": str(e)}