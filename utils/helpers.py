import datetime

def log_event(msg: str):
    with open("guardian.log", "a") as f:
        f.write(f"{datetime.datetime.now()}: {msg}\n")
