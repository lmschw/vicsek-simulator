from datetime import datetime

def logWithTime(text):
    dateTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"{dateTime}: {text}")
