# Importeren van benodigde modules

import requests  # Voor het maken van HTTP-verzoeken

import json  # Voor het werken met JSON-data

from datetime import datetime  # Voor het ophalen en bewerken van datum en tijd

import pytz  # Voor het werken met tijdzones

import time  # Voor het toevoegen van vertragingen (bijvoorbeeld een wachttijd van 60 seconden)
 
# API-sleutel (specifiek voor jouw Vestaboard-apparaat)

API_KEY = "NTIwMDBkNjctOTQ0My00NjJkLTg4NjItZWQyMmM3ZmNjODkw"
 
# Vestaboard lokale API-endpoint

message_url = "http://192.168.42.2:7000/local-api/message"
 
# Functie om de huidige tijd en datum op te halen

def get_current_time():

    # Stel de tijdzone in op Europe/Amsterdam (GMT+1)

    timezone = pytz.timezone("Europe/Amsterdam")

    # Haal de huidige tijd op in de ingestelde tijdzone

    now = datetime.now(timezone)

    # Verkorte dagnaam in hoofdletters, bijv. "MON" of "TUE"

    day_short = now.strftime("%a").upper()

     # Datum in formaat "DD MON", bijv. "11 DEC"

    date_part = now.strftime("%d %b").upper()

    # Combineer de dag en datum, bijv. "MON 11 DEC"

    date_str = f"{day_short} {date_part}"

    # Haal het huidige uur en minuut op

    hour = now.strftime("%H")

    minute = now.strftime("%M")

    # AM/PM-indeling (niet strikt nodig voor 24-uursformaat)

    period = "PM" if int(hour) >= 12 else "AM"

    # Combineer de tijd in het formaat "HH:MM AM/PM"

    time_str = f"{hour}:{minute} {period}"

    return date_str, time_str
 
# Functie om een tekst om te zetten naar een matrix van codes

def text_to_matrix(text, row_length=22):

    # Mapping van tekens naar matrixcodes volgens Vestaboard-specificaties

    mapping = {

        " ": 0,  # Lege ruimte

        "-": 44,  # Streepje

        ":": 50,  # Dubbele punt

        **{chr(i): i - 64 for i in range(65, 91)},  # letters beginnen bij 65. dit zet 1 gelijk aan a

        **{str(i): i + 26 for i in range(1, 10)},  # zelfde maar dan met de cijfers

        "0": 36  # 0 word gezet op de 36

    }

    # hier word de code gehaald uit de mapping dictonary en alles in hoofdletters gezet. geen waarde = 0

    row = [mapping.get(char, 0) for char in text.upper()]

    # hier word berekend hoeveel ruimte er nog over is na de text

    padding = (row_length - len(row)) // 2

    # Voeg padding aan beide zijden toe toegevoegd

    return [0] * padding + row + [0] * (row_length - len(row) - padding)
 
# Functie om de progressiebalk te berekenen

def calculate_progress_bar():

    # Stel de tijdzone in op Europe/Amsterdam

    timezone = pytz.timezone("Europe/Amsterdam")

    # Haal de huidige tijd op

    now = datetime.now(timezone)

    # Definieer het begin van de dag (middernacht)

    start_of_day = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=timezone)

    # Definieer het einde van de dag (23:59:59)

    end_of_day = datetime(now.year, now.month, now.day, 23, 59, 59, tzinfo=timezone)

    # Bereken het totale aantal seconden in de dag

    total_seconds = (end_of_day - start_of_day).total_seconds()

    # Bereken hoeveel seconden er verstreken zijn sinds middernacht

    elapsed_seconds = (now - start_of_day).total_seconds()

    # Bereken de voortgang als een percentage van 22 kolommen (maximale breedte)

    progress = int((elapsed_seconds / total_seconds) * 22)

    # Maak een progressiebalk met blauwe (67) en witte (69) segmenten

    return [67] * progress + [69] * (22 - progress)
 
# Functie om het bericht naar de Vestaboard te sturen

def send_vestaboard_message():

    # Haal de dynamische datum en tijd op

    date_str, time_str = get_current_time()

    # Bereken de progressiebalk

    progress_bar = calculate_progress_bar()

    # Stel de matrix samen voor het Vestaboard-bericht

    message_matrix = [

        progress_bar,               # Progressiebalk als bovenrand

        [0] * 22,                   # Lege regel

        text_to_matrix(date_str),   # Datumregel

        text_to_matrix(time_str),   # Tijdregel

        [0] * 22,                   # Lege regel

        progress_bar                # Progressiebalk als onderrand

    ]

    # Debug-output van de payload (voor controle)

    print("Verstuurde Payload:")

    print(json.dumps(message_matrix, indent=4))

    # Headers voor het verzoek

    headers = {

        "Content-Type": "application/json",  # Dataformaat is JSON

        "X-Vestaboard-Local-Api-Key": API_KEY,  # Authenticatie voor de lokale API

    }

    # Probeer het bericht te verzenden via een POST-verzoek

    try:

        response = requests.post(message_url, headers=headers, data=json.dumps(message_matrix))

        # Controleer of het verzoek succesvol was

        if response.status_code == 200:

            print("Bericht succesvol geplaatst!")

        else:

            # Toon foutmeldingen als het verzoek faalt

            print(f"Fout: {response.status_code}")

            print("Response Headers:", response.headers)

            print("Response Body:", response.text)

    except requests.exceptions.RequestException as e:

        # Foutafhandeling voor netwerkproblemen

        print("Er is een fout opgetreden:", str(e))
 
# Automatische update-loop

if __name__ == "__main__":

    print("Start automatische updates elke minuut...")

    # Oneindige lus om de Vestaboard continu te updaten

    while True:

        send_vestaboard_message()  # Verstuur het bericht

        time.sleep(60)  # Wacht 60 seconden voor de volgende update

 