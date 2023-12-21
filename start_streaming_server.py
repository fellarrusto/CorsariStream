import subprocess
import cv2

# Funzione per elencare le webcam disponibili
def elenca_webcam():
    indice = 0
    webcam_disponibili = []
    while True:
        cap = cv2.VideoCapture(indice, cv2.CAP_DSHOW)
        if not cap.read()[0]:
            break
        else:
            webcam_disponibili.append(indice)
        cap.release()
        indice += 1
    return webcam_disponibili

# Elenca le webcam e chiedi all'utente di sceglierne una
webcam_disponibili = elenca_webcam()
print("Webcam disponibili:")

for w in webcam_disponibili:
    print(f"> {w}")

selezione = int(input("Inserisci l'ID della webcam che vuoi usare: "))

# Controlla se la selezione è valida
if selezione in webcam_disponibili:
    id_webcam_scelta = selezione
    print(f"Webcam selezionata: ID {id_webcam_scelta}")
    # Start streaming with selected device in the same environment
    subprocess.Popen(["python", "streaming_server.py", str(id_webcam_scelta)], shell=True)
else:
    print("Selezione non valida.")
    exit(1)
