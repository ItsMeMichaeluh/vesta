import requests
from datetime import datetime
import json

# Vestaboard API-key en lokale URL
API_KEY = "NTIwMDBkNjctOTQ0My00NjJkLTg4NjItZWQyMmM3ZmNjODkw"
MESSAGE_URL = "http://192.168.42.2:7000/local-api/message"

def format_time_to_matrix(current_time):
    """
    Converteert de huidige tijd naar een matrix van 22x6 voor Vestaboard.
    Verandert dubbele punten naar '11'.
    """
    # Vervang dubbele punt met '11'
    current_time = current_time.replace(":", "11")

    # Maak een lege matrix (6 rijen, 22 kolommen) gevuld met spaties
    matrix = [[0] * 22 for _ in range(6)]
    
    # Plaats de tijd in de middelste rij
    start_col = (22 - len(current_time)) // 2  # Bereken de begin kolom om de tijd te centreren
    row = 2  # Plaats de tijd in de derde rij (0-gebaseerd index)
    
    # Vul de matrix met de huidige tijd
    for i, char in enumerate(current_time):
        matrix[row][start_col + i] = char
    
    # Flatten de matrix naar een lijst van 132 tekens (22 kolommen x 6 rijen)
    flattened_matrix = [char for row in matrix for char in row]
    
    # Controleer of de matrix 132 tekens heeft
    if len(flattened_matrix) != 132:
        print(f"Fout: De matrix heeft {len(flattened_matrix)} tekens in plaats van 132!")
    
    return flattened_matrix

def convert_to_2d_matrix(flattened_matrix):
    """
    Zet de geflatteerde matrix om naar een 2D matrix van 6x22 voor debug.
    """
    return [flattened_matrix[i:i+22] for i in range(0, 132, 22)]

# Huidige tijd ophalen
current_time = datetime.now().strftime('%H:%M:%S')

# Tijd omzetten naar een matrix
matrix_message = format_time_to_matrix(current_time)

# Debug: Converteer naar 2D matrix en print
matrix_2d = convert_to_2d_matrix(matrix_message)
print("2D Matrix Output (22x6):")
for row in matrix_2d:
    print(row)

# Headers instellen
headers = {
    "Content-Type": "application/json",
    "X-Vestaboard-Local-Api-Key": API_KEY,
}

# Payload maken
payload = {
    "characters": matrix_message
}

# Bericht versturen
response = requests.post(MESSAGE_URL, data=json.dumps(payload), headers=headers)

# Response controleren
if response.status_code == 200:
    print("Time sent to Vestaboard successfully!")
else:
    print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
