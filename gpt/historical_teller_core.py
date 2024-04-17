import json

from openai import OpenAI
from datetime import datetime


class HistoricalTeller:
    api_key = ""
    client = None

    def __init__(self):
        try:
            with open("secrets.json") as f:
                secrets = json.load(f)
                api_key = secrets["api_key"]
                self.client = OpenAI(api_key=api_key)

        except FileNotFoundError:
            print("Il file 'secrets.json' non è stato trovato.")
        except KeyError:
            print("L'api_key non è stata trovata in 'secrets.json'.")

    def tellStory(self):
        # Get the current date
        current_date = datetime.now()

        # Format the date as "Month day"
        formatted_date = current_date.strftime("%B %d")
        print(formatted_date)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "you are a historical storyteller, and you have to"
                                              "talk about an event that happened on" + formatted_date + "in history, "
                                                                                                        "split it in 5 "
                                                                                                        "parts, max "
                                                                                                        "min 300 words max 450 words"
                                                                                                        "export your "
                                                                                                        "answer as "
                                                                                                        "json with "
                                                                                                        "these "
                                                                                                        "fields, "
                                                                                                        "title, date("
                                                                                                        "day, month, "
                                                                                                        "year format "
                                                                                                        "as single "
                                                                                                        "string),"
                                                                                                        "description, "
                                                                                                        "parts, "
                                                                                                        "(an array of "
                                                                                                        "objects of "
                                                                                                        "every split "
                                                                                                        "part with a "
                                                                                                        "description "
                                                                                                        "and "
                                                                                                        "imageSearch "
                                                                                                        "query) "},
            ],
            temperature=1.0
        )
        return response
