import requests
import time
from datetime import datetime, timedelta, UTC


def format_event(events):

    for event in events:
        raw_date = event.get("start")
        dt = datetime.fromisoformat(raw_date.replace("Z","+00:00"))
        event["start"] = dt.strftime("%d %B %Y - %H:%M UTC")

        if not event.get("location"):
            event["location"] = "Online"

    return events

def generate_html(events, filename="ctfs.html"):
    html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>CTF Tracker</title>

<style>
body {
    background-color: #0d0d0d;
    color: #00ff9f;
    font-family: "Courier New", monospace;
    margin: 0;
    padding: 40px;
}

h1 {
    text-align: center;
    font-size: 2.5em;
    text-shadow: 0 0 10px #00ff9f;
}

.event {
    background: #111;
    border: 1px solid #00ff9f;
    padding: 20px;
    margin-bottom: 25px;
    border-radius: 6px;
    box-shadow: 0 0 10px #00ff9f33;
    transition: 0.3s;
}

.event:hover {
    box-shadow: 0 0 20px #00ff9f;
}

a {
    color: #00ffff;
    text-decoration: none;
}

a:hover {
    text-shadow: 0 0 8px #00ffff;
}

.footer {
    text-align: center;
    margin-top: 40px;
    font-size: 0.8em;
    opacity: 0.7;
}
</style>
</head>
<body>

<h1> PRÓXIMOS CTFs </h1>
"""
    if not events:
        html += "<p>Nenhum CTF encontrado..</p>"
    else:
        for event in events:
            organizers = event.get("organizers", [])
            organizer_name = organizers[0]["name"] if organizers else "Unknown"

            html += f"""
<div class="event">
    <h2>{event.get('title')}</h2>
    <p><strong>Início:</strong> {event.get('start')}</p>
    <p><strong>Localzação:</strong> {event.get('location')}</p>
    <p><strong>Organizadores:</strong> {organizer_name}</p>
    <p><strong>Descrição:</strong> {event.get("description")}</p>
    <p>
        [ <a href="{event.get('url')}" target="_blank">Site Oficial</a> ] |
        [ <a href="{event.get('ctftime_url')}" target="_blank">CTFtime</a> ]
    </p>
</div>
"""

    html += """

</body>
</html>
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

def get_ctfs(limit=10, days_ahead=30):

    start_timestamp  = int(time.time())
    future_date = datetime.now(UTC) + timedelta(days=days_ahead)
    finish_timestamp = int(future_date.timestamp())

    url = "https://ctftime.org/api/v1/events/"

    headers = {"User-Agent": "Mozilla/5.0 (compatible; CTFTracker/1.0)"}

    params = {"limit": limit,"start": start_timestamp,"finish": finish_timestamp}

    response = requests.get(url,params=params,headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code} - {response.text}")

    return response.json()


def print_events(events):
    if not events:
        print("Sem CTFs.")
        return

    for event in events:

        organizers = event.get("organizers",[])

        print("="*50)
        print(f"Título: {event.get('title')}")
        print(f"Link: {event.get('url')}")
        print(f"Organizadores: {organizers[0]['name']}")
        print(f"Início: {event.get('start')}")
        print(f"Localização: {event.get('location')}")
        print(f"Descrição: {event.get('description')}")
        print(f"Link no CTF time: {event.get('ctftime_url')}")
        print("="*50)


def main():
    try:
        events = get_ctfs(limit=20,days_ahead=30)
        events_clean  = format_event(events)
        generate_html(events_clean)
        print("ctf.html gerado com sucesso.")
        print_events(events_clean)
    except Exception as e:
        print(f"Erro ao realizar a requisicao: {e}")


if __name__ == "__main__":
    main()
