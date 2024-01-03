import requests
from datetime import datetime
import os

NT_APP_ID = os.environ.get("NT_APP_ID", "App ID does not exists")
NT_API_KEY = os.environ.get("NT_API_KEY", "API Key does not exists")

SHEET_BASIC_AUTH = os.environ.get("SHEET_BASIC_AUTH", "Basic Auth does not exists")
SHEET_TOKEN = os.environ.get("SHEET_TOKEN", "Token does not exists")
SHEET_EP = os.environ.get("SHEET_EP", "Sheet end point does not exists")

GENDER = "male"
WEIGHT_KG = 78
HEIGHT_CM = 176
AGE = 45

exercise_text = input("Tell me which exercises you did:")

headers = {
    "x-app-id": NT_APP_ID,
    "x-app-key": NT_API_KEY,
}
parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}

nutritionix_ep = "https://trackapi.nutritionix.com/v2/natural/exercise"
response = requests.post(url=nutritionix_ep, json=parameters, headers=headers)
result = response.json()

user_inputs = [exercise['user_input'] for exercise in result.get('exercises', [])]
exercise_duration = [duration['duration_min'] for duration in result.get('exercises', [])]
calories_burned = [calories['nf_calories'] for calories in result.get('exercises', [])]

today = datetime.now()
exercise_date = today.strftime('%d/%m/%Y')
exercise_time = today.strftime('%H:%M:%S')

sheet_headers_basic_auth = {
    "Authorization": SHEET_BASIC_AUTH,
}
sheet_headers_bearer_token = {
    "Authorization": SHEET_TOKEN,
}

sheet_ep = SHEET_EP
for exercise in result['exercises']:
    sheet_inputs = {
        "workout": {
            "date": exercise_date,
            "time": exercise_time,
            "exercise": exercise['name'].title(),
            "duration": exercise['duration_min'],
            "calories": exercise['nf_calories'],
        }
    }

    # There are 2 ways of basic authentication:
    # 1) using username and password tuple
    # 2) using authorization header.

    # sheet_response = requests.post(url=sheet_ep, json=sheet_inputs, auth=('username', 'password'))
    # sheet_response = requests.post(url=sheet_ep, json=sheet_inputs, headers=sheet_headers_basic_auth)

    # Authentication using bearer token. It's essentially same as that basic authentication using
    # authentication header
    sheet_response = requests.post(url=sheet_ep, json=sheet_inputs, headers=sheet_headers_bearer_token)

