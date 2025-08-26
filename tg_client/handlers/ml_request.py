import requests


url = "http://localhost/recommender/ml"

def call_ml_service(film: str) -> str:


    #fix handling
    try:
        r = requests.get(url=url, data={"film": film})

        if r.status_code == 200:
            text = f"Your recommendation:"
        elif r.status_code == 404:
            text = "Sorry, session ID not found"
        elif r.status_code == 500:
            text = "Sorry, database error"
        elif r.status_code == 422:
            try:
                error_data = r.json()
                text = f"Validation Error: {error_data}"
            except ValueError:
                text = "Validation Error: Unable to parse error details" 
        else:
            r.raise_for_status()

    except requests.exceptions.RequestException as err:
        text = f"Sorry, failed, err: {err.args[0]}"

    return ""