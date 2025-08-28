import requests
from typing import List, Union


url = "http://localhost/recommender/"

def call_ml_service(film: str, recommendation: List[str]) -> dict:

    try:
        r = requests.post(url=f"{url}ml", json={"film": film, "recommendation": recommendation})

        if r.status_code == 200:
            return {"status": "ok",
                "text": r.json()["recommendation"]}
        elif r.status_code == 404:
            return {"status": "no",
                    "text":"Sorry, session ID not found"}
        elif r.status_code == 500:
            return {"status": "no",
                "text":"Sorry, database error"}
        elif r.status_code == 422:
            try:
                error_data = r.json()
                return {"status": "no",
                            "text": f"Validation Error: {str(error_data)[:40]}"}
            except ValueError:
                return {"status": "no",
                        "text": "Validation Error: Unable to parse error details" }
        else:
            r.raise_for_status()

    except requests.exceptions.RequestException as err:
        return {"status": "no",
            "text": f"Sorry, failed, err: {str(err)[:30]}"}
 
    
    return {"status": "no",
            "text": "sorry, unhandling error"}

def generate_films(session_id: str, film: str, recommendation: List[str]) -> str:

    answer = call_ml_service(film, recommendation=recommendation)

    if answer["status"] == "ok":
        film_recommendations = answer["text"]
    
        data_post = {
        "session_id": f"{session_id}",
        "film": f"{film}",
        "recommendation": f"{film_recommendations}"
        }  


        try:
            r = requests.post(url=f"{url}db", json=data_post)

            if r.status_code == 200:
                text = f"Your recommendation: {film_recommendations}"
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
            text = f"Sorry, failed, err: {str(err)[:30]}"
    else:
        text = answer["text"]

    return text


def regenerate_films(session_id: str, film: str) -> str:
    data_regenerate = {
        "session_id": session_id
    }
    try:
        r = requests.get(url=f"{url}db", data=data_regenerate)

        if r.status_code == 200:
            #fix it
            recommended_films = [i[1].split(' ') for i in (r.json())["recommendation"] if i[0] == film]

            text = generate_films(session_id=session_id, film=film, recommendation=recommended_films)
            
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

    return text