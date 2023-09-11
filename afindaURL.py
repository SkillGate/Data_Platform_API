import os
import requests
import json
import csv

# Define the API endpoint and headers
url = 'https://api.affinda.com/v3/documents'
headers = {
    'accept': 'application/json',
    'authorization': 'Bearer aff_ac5f125b77897d56a2cb8d95003b08e8b1bef634'
}

# Define the form data for the request
data = {
    'wait': 'true',
    'collection': 'gVPHcvdV',
    'workspace': 'ihQcVSlq',
    'fileName': 'XVT_SE_19000626.pdf'
}

# Get the current working directory (where the script is located)
current_directory = os.path.dirname(__file__)

# Define the file to upload using a relative path
file_path = os.path.join(current_directory, 'XVT_SE_19000626.pdf')

files = {
    'file': ('XVT_SE_19000626.pdf', open(file_path, 'rb'))
}

# Make the POST request
response = requests.post(url, headers=headers, data=data, files=files)

# Check the response
if response.status_code == 200:
    print('Request successful!')
    # print(response.json())
else:
    print(f'Request failed with status code: {response.status_code}')
    print(response.text)


# Assuming you have already made the API request and have 'response' as the response object
# Get the JSON data from the response
data = response.json()

# Initialize a list to store hard skills and soft skills
hardSkills = []
softSkills = []

# Iterate through the "skills" array in the JSON data
for skill in data.get("data", {}).get("skills", []):
    if skill.get("type") == "hard_skill":
        # Append the entire skill object to the hardSkills list
        hardSkills.append(skill.get("name"))
    if skill.get("type") == "soft_skill":
            # Append the entire skill object to the hardSkills list
        softSkills.append(skill.get("name"))


#filtering the education qualifications
educationSet=[]

# Iterate through the "education" array in the JSON data
for education in data.get("data", {}).get("education", []):
    educationSet.append(education.get("accreditation").get("education"))


# filtering the working experience.
workExperience = []

workExperience.append(data.get("data", {}).get("totalYearsExperience"))

# writing to a csv file.

# record=[softSkills,hardSkills,educationSet,workExperience]

# csvFile="data.csv"

# with open(csvFile, mode='a', newline='') as file:
#     writer = csv.writer(file)


#     writer.writerow(record)
