from fastapi import APIRouter, HTTPException, Request, Query, Response
from fastapi.responses import StreamingResponse
# from schema.schemas import affindaPDF
from schema.gitHubSchemas import github_collaborators_commit_count
from schema.gitHubSchemas import github_collaborators_commit_details
from schema.gitHubSchemas import github_organization_languages
from schema.gitHubSchemas import github_user_profile_info
from schema.gitHubSchemas import get_github_project_details
from schema.mediumBlogSchemas import extract_blogger_posts
from schema.mediumBlogSchemas import extract_medium_posts
from schema.LinkedInSchemas import extract_linkedIn_skills_and_recommendation_data
from schema.LinkedInSchemas import extract_linkedIn_skills
from schema.LinkedInSchemas import extract_linkedIn_recommendations
from schema.gitHubSchemas import github_repositories
from typing import Generator
import json
import time
# from config.database import collection_name


router = APIRouter()

# @router.get("/uploadfile")
# async def upload_file(fileUrl: str = Query(..., description="Description of param1")):
#     result  = affindaPDF(fileUrl=fileUrl)
#     return result;

@router.get("/github/collaboratorsCommitCount")
async def upload_file(gitHubUrl: str = Query(..., description="Description of param1")):
    try:
        result = github_collaborators_commit_count(gitHubUrl=gitHubUrl)
        return result
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/github/collaboratorsCommitDetails")
async def upload_file(gitHubUrl: str = Query(..., description="Description of param1")):
    try:
        result = github_collaborators_commit_details(gitHubUrl=gitHubUrl)
        return result
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/github/organizationLanguages")
async def upload_file(gitHubUrl: str = Query(..., description="Description of param1")):
    try:
        result = github_organization_languages(gitHubUrl=gitHubUrl)
        return result
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/github/userInfo")
async def upload_file(gitHubUrl: str = Query(..., description="Description of param1")):
    try:
        result = github_user_profile_info(gitHubUrl=gitHubUrl)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found")
    
# @router.get("/github/projects")
# async def blogger_post(gitHubUrl: str = Query(..., description="Description of param1")):
#         try:
#             result = get_github_project_details(gitHubUrl)
#             return result
#         except Exception as e:
#             return {"error": str(e)}

@router.get("/github/projects")
async def blogger_post(gitHubUrl: str = Query(..., description="Description of param1")):
    response = StreamingResponse(get_github_project_details(gitHubUrl), media_type="application/json")
    response.headers["Transfer-Encoding"] = "chunked"
    return response
    
@router.get("/github/projectRepos")
async def blogger_post(gitHubUrl: str = Query(..., description="Description of param1")):
    print("github repositories")
    try:
        result = github_repositories(gitHubUrl)
        response = Response(content=result, headers={"Access-Control-Allow-Origin": "*"})
        return response
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/blog/posts")
def blogger_post(blogUrl: str = Query(..., description="Description of param1")):
    try:
        if 'medium' in blogUrl.lower():
            result = extract_medium_posts(mediumUrl=blogUrl)
            return result
        else:
            result = extract_blogger_posts(bloggerUrl=blogUrl)
            return result
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/linkedIn/skillsandRecommendations")
def blogger_post(linkedInUrl: str = Query(..., description="Description of param1")):
    try:
        result = extract_linkedIn_skills_and_recommendation_data(linkedInUrl=linkedInUrl)
        return result
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/linkedIn/skills")
def blogger_post(linkedInUrl: str = Query(..., description="Description of param1")):
    try:
        result = extract_linkedIn_skills(linkedInUrl=linkedInUrl)
        return result
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/linkedIn/recommendations")
def blogger_post(linkedInUrl: str = Query(..., description="Description of param1")):
    try:
        result = extract_linkedIn_recommendations(linkedInUrl=linkedInUrl)
        return result
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/")
def hello():
    return "Hello Ashani"

def generate_data():
    for i in range(10):
        yield json.dumps({"index": i, "message": "This is message {}".format(i)}) + '\n'
        time.sleep(1)  # Simulate some delay between each data item

@router.get("/stream")
async def stream_data():
    response = StreamingResponse(content=generate_data(), media_type="application/json")
    response.headers["Transfer-Encoding"] = "chunked"
    return response