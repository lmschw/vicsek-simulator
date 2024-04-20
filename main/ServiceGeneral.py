from datetime import datetime

def logWithTime(text):
    dateTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"{dateTime}: {text}")


def formatTime(timeInSecs):
    mins = int(timeInSecs / 60)
    secs = timeInSecs % 60

    if mins >= 60:
        hours = int(mins / 60)
        mins = mins % 60
        return f"{hours}h {mins}min {secs:.1f}s"
    return f"{mins}min {secs:.1f}s"

