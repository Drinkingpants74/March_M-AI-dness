import pandas as pd
from openai import OpenAI

# CHANGE <IP ADDRESS> TO YOUR ACTUAL IP ADDRESS
# ON DEVICE: localhost OR 127.0.0.1
# OFF DEVICE: IP Address of Other Device (192.168.1.x)
baseURL = "http://<IP ADDRESS>:8080"

df = pd.read_csv('Bracket_Teams.csv')

records = df.to_dict(orient='records')

stats_dict = {}
for i in records:
    stats_dict[i['School']] = i

client = None

system_prompt = """You are a College Basketball Expert. You will be given two teams, and their statistics over a season, and you determine which team should win on a neutral court.

When you have decided which team should win, you will output ONLY THE NAME OF THE WINNING TEAM. For example, if you were given "TeamA" and "TeamB" and you decide "TeamA" should win, you will simply reply with "TeamA".
Do no reply with any punctuation, extra information, or a justification of your pick, just pick the team."""

def get_authorized():
    global client, baseURL

    client = OpenAI(
        base_url=f"{baseURL}/v1",
        api_key="sk-no-key-required",
        timeout=120.0
    )

def send_message(messages):
    global client
    return client.chat.completions.create(
        model="",
        messages=messages,
        stream=False,
        temperature=0.8,
        top_p=0.95,
        frequency_penalty=0.0,
        seed=74,
        extra_body={
            "min_p": 0.05,
            "top_k": 40,
            "repeat_penalty": 1.1,
            "batch_size": 2048
        }
    )

def build_message(role: str, text: str) -> dict[str,str]:
    return {"role": role, "content": text}

def build_matchup(home: str, away: str) -> tuple:
    return (home, away)

def simulate_tournament_rounds(round_matchups):
    count = 0
    prevWinner = None
    next_round = []
    for match in round_matchups:
        team1, team2 = match
        winner = simulate_winner(team1, team2)
        count += 1
        if (count == 2):
            next_round.append(build_matchup(prevWinner, winner))
            count = 0
        else:
            prevWinner = winner

    return next_round


def simulate_winner(team1, team2) -> str:
    prompt = f"Pick a winner on a neutral court between the following two teams: {team1} vs. {team2}.\n{team1} Stats:\n{stats_dict[team1]}\n{team2} Stats:\n{stats_dict[team2]}"

    message = [
        build_message("system", system_prompt),
        build_message("user", prompt)
    ]

    response = send_message(message)

    return str(response.choices[0].message.content)



get_authorized()

round_1 = [
    # East
    build_matchup("Duke", "Siena"),
    build_matchup("Ohio State", "Texas Christian"),
    build_matchup("St. John's (NY)", "Northern Iowa"),
    build_matchup("Kansas", "California Baptist"),
    build_matchup("Louisville", "South Florida"),
    build_matchup("Michigan State", "North Dakota State"),
    build_matchup("UCLA", "UCF"),
    build_matchup("Connecticut", "Furman"),

    # South
    build_matchup("Florida", simulate_winner("Prairie View A&M", "Lehigh")),
    build_matchup("Clemson", "Iowa"),
    build_matchup("Vanderbilt", "McNeese"),
    build_matchup("Nebraska", "Troy"),
    build_matchup("North Carolina", "Virginia Commonwealth"),
    build_matchup("Illinois", "Pennsylvania"),
    build_matchup("Saint Mary's", "Texas A&M"),
    build_matchup("Houston", "Idaho"),

    # West
    build_matchup("Arizona", "Long Island University"),
    build_matchup("Villanova", "Utah State"),
    build_matchup("Wisconsin", "High Point"),
    build_matchup("Arkansas", "Hawaii"),
    build_matchup("Brigham Young", simulate_winner("Texas", "NC State")),
    build_matchup("Gonzaga", "Kennesaw State"),
    build_matchup("Miami (FL)", "Missouri"),
    build_matchup("Purdue", "Queens (NC)"),

    # Midwest
    build_matchup("Michigan", simulate_winner("Maryland-Baltimore County", "Howard")),
    build_matchup("Georgia", "Saint Louis"),
    build_matchup("Texas Tech", "Akron"),
    build_matchup("Alabama", "Hofstra"),
    build_matchup("Tennessee", simulate_winner("Miami (OH)", "Southern Methodist")),
    build_matchup("Virginia", "Wright State"),
    build_matchup("Kentucky", "Santa Clara"),
    build_matchup("Iowa State", "Tennessee State"),
]

results_round_1 = simulate_tournament_rounds(round_1)
print(results_round_1)

results_round_2 = simulate_tournament_rounds(results_round_1)
print(results_round_2)

results_round_3 = simulate_tournament_rounds(results_round_2)
print(results_round_3)

results_round_4 = simulate_tournament_rounds(results_round_3)
print(results_round_4)

results_round_5 = simulate_tournament_rounds(results_round_4)
print(results_round_5)

final_team_1, final_team_2 = results_round_5[0]

results_final = simulate_winner(final_team_1, final_team_2)
print(results_final)
