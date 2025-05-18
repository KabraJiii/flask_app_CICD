from flask import Flask, render_template
import requests
import json
from tabulate import tabulate
import os

app = Flask(__name__)

def fetch_cricket_scores():
    url = 'https://crickbuzz-official-apis.p.rapidapi.com/matches/list'
    headers = {
        'x-rapidapi-key': '831af6d415msh83780108e78df43p127955jsn56ed552814e7',
        'x-rapidapi-host': 'crickbuzz-official-apis.p.rapidapi.com'
    }

    response = requests.get(url, headers=headers)
    matches_data = []

    if response.status_code == 200:
        try:
            data = response.json()

            type_matches = data.get("typeMatches", [])
            for match_type in type_matches:
                for series in match_type.get("seriesMatches", []):
                    wrapper = series.get("seriesAdWrapper", {})
                    for match in wrapper.get("matches", []):
                        # same processing logic
                        ...
        except Exception as e:
            print("Error while processing match data:", e)
    else:
        print("Failed to fetch. Status code:", response.status_code)

    return matches_data


def fetch_upcoming_matches():
    url = 'https://crickbuzz-official-apis.p.rapidapi.com/schedules/international'
    headers = {
    'x-rapidapi-key': '831af6d415msh83780108e78df43p127955jsn56ed552814e7',
    'x-rapidapi-host': 'crickbuzz-official-apis.p.rapidapi.com'
  }

    response = requests.get(url, headers=headers)
    upcoming_matches = []

    if response.status_code == 200:
        try:
            data = response.json()
            match_schedules = data.get('matchScheduleMap', [])

            for schedule in match_schedules:
                if 'scheduleAdWrapper' in schedule:
                    date = schedule['scheduleAdWrapper']['date']
                    matches = schedule['scheduleAdWrapper']['matchScheduleList']

                    for match_info in matches:
                        for match in match_info['matchInfo']:
                            description = match['matchDesc']
                            team1 = match['team1']['teamName']
                            team2 = match['team2']['teamName']
                            match_data = {
                                'Date': date,
                                'Description': description,
                                'Teams': f"{team1} vs {team2}"
                            }
                            upcoming_matches.append(match_data)
                else:
                    print("No match schedule found for this entry.")

        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)
        except KeyError as e:
            print("Key error:", e)
    else:
        print("Failed to fetch upcoming matches. Status code:", response.status_code)

    return upcoming_matches


@app.route('/')
def index():
    cricket_scores = fetch_cricket_scores()
    upcoming_matches = fetch_upcoming_matches()
    return render_template('index.html', cricket_scores=cricket_scores, upcoming_matches=upcoming_matches)


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 8080)), host='0.0.0.0', debug=True)