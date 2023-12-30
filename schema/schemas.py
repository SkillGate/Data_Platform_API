import requests
from config.database import collection_name
from models.todo import CV
import logging

def affindaPDF(fileUrl):

    url = "https://api.affinda.com/v3/documents"

    payload = {
        "wait": "true",
        "collection": "gVPHcvdV",
        "workspace": "ihQcVSlq",
        "url": fileUrl
    }
    headers = {
        "accept": "application/json",
        "authorization": "Bearer aff_ac5f125b77897d56a2cb8d95003b08e8b1bef634"
    }

    response = requests.post(url, data=payload, headers=headers)

    data = response.json();

    error = data.get("error").get("errorCode");

    print(error);

    if(error is not None):
        logging.info("Error happened: %s", error);
        errorResponse = {"error": error}
        # jsonErrorResponse = json.dumps(errorResponse)
        return errorResponse;

    data = response.json()

    hardSkills = []
    softSkills = []

    for skill in data.get("data", {}).get("skills", []):
        if skill.get("type") == "hard_skill":
            hardSkills.append(skill.get("name"))
        if skill.get("type") == "soft_skill":
            softSkills.append(skill.get("name"))


    educationSet=[]

    for education in data.get("data", {}).get("education", []):
        educationSet.append(education.get("accreditation").get("education"))


    # filtering the working experience.
    workExperience = []

    workExperience.append(data.get("data", {}).get("totalYearsExperience"))

    body = {
        "educationSet": educationSet,
        "hardskill": hardSkills,
        "softskill": softSkills,
        "workExperience": workExperience
    }

    data = {
    "educationSet": ["Degree in Computer Science", "Certification in AI"],
    "hardskill": ["Python", "Machine Learning", "Database Management"],
    "softskill": ["Communication", "Problem Solving", "Teamwork"],
    "workExperience": ["Software Engineer at Company A", "Data Analyst at Company B"]
}
    
    cv_instance = CV(**data)
    try:
    # Attempt to insert data into the database
        collection_name.insert_one(cv_instance)
        return body;
    except Exception as e:
        print("Error:", str(e))
        return str(e)




