import requests

import json

from datetime import datetime 

import pytz

import time
 
# API-sleutel

API_KEY = "NTIwMDBkNjctOTQ0My00NjJkLTg4NjItZWQyMmM3ZmNjODkw"
 
# Endpoint
  
message_url = "http://192.168.42.2:7000/local-api/message"
 
# Functie om de huidige tijd op te halen

def get_current_time():

    timezone = pytz.timezone("Europe/Amsterdam")  # GMT+1 tijdzone

    now = datetime.now(timezone)

    day_short = now.strftime("%a").upper()  # Verkorte dagnaam, bijv. "MON", "TUE"

    date_part = now.strftime("%d %b").upper()  # Bijv. "11 DEC"

    date_str = f"{day_short} {date_part}"  # Combineer, bijv. "MON 11 DEC"

    hour = now.strftime("%H")  # 24-uurs formaat

    minute = now.strftime("%M")

    period = "PM" if int(hour) >= 12 else "AM"

    time_str = f"{hour}:{minute} {period}"  # Bijv. "13:47 PM"

    return date_str, time_str
 
# Functie om tekst om te zetten naar matrixcodes

def text_to_matrix(text, row_length=22):

    mapping = {

        " ": 0, "-": 44, ":": 50,

        **{chr(i): i - 64 for i in range(65, 91)},  # Letters A-Z

        **{str(i): i + 26 for i in range(1, 10)},  # Cijfers 1-9

        "0": 36  # Correcte mapping voor "0"

    }

    row = [mapping.get(char, 0) for char in text.upper()]

    padding = (row_length - len(row)) // 2  # Bereken padding voor centreren

    return [0] * padding + row + [0] * (row_length - len(row) - padding)
 
# Functie om de progressiebalk te berekenen

def calculate_progress_bar():

    timezone = pytz.timezone("Europe/Amsterdam")

    now = datetime.now(timezone)

    start_of_day = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=timezone)

    end_of_day = datetime(now.year, now.month, now.day, 23, 59, 59, tzinfo=timezone)

    total_seconds = (end_of_day - start_of_day).total_seconds()

    elapsed_seconds = (now - start_of_day).total_seconds()

    progress = int((elapsed_seconds / total_seconds) * 22)  # Maximaal 22 kolommen

    return [67] * progress + [69] * (22 - progress)  # Blauwe en witte progressiebalk
 
# Functie om het bericht te versturen

def send_vestaboard_message():

    # Dynamische datum en tijd ophalen

    date_str, time_str = get_current_time()
 
    # Progressiebalk berekenen

    progress_bar = calculate_progress_bar()
 
    # Dynamische matrix maken

    message_matrix = [

        progress_bar,               # Blauwe bovenrand (loading bar)

        [0] * 22,                   # Lege regel

        text_to_matrix(date_str),   # Dynamische datum (verkorte dagnaam)

        text_to_matrix(time_str),   # Dynamische tijd

        [0] * 22,                   # Lege regel

        progress_bar                # Blauwe onderrand (loading bar)

    ]
 
    # Debug-output van de payload

    print("Verstuurde Payload:")

    print(json.dumps(message_matrix, indent=4))
 
    # Headers

    headers = {

        "Content-Type": "application/json",

        "X-Vestaboard-Local-Api-Key": API_KEY,

    }
 
    # Verstuur het bericht

    try:

        response = requests.post(message_url, headers=headers, data=json.dumps(message_matrix))

        if response.status_code == 200:

            print("Bericht succesvol geplaatst!")

        else:

            print(f"Fout: {response.status_code}")

            print("Response Headers:", response.headers)

            print("Response Body:", response.text)

    except requests.exceptions.RequestException as e:

        print("Er is een fout opgetreden:", str(e))
 
# Automatische update-loop

if __name__ == "__main__":

    print("Start automatische updates elke minuut...")

    while True:

        send_vestaboard_message()

        time.sleep(60)  # Wacht 60 seconden

 