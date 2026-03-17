# March M-AI-dness
A Simply Python Script to use an LLM to predict the NCAA Men's Basketball Champion

## How it Works
The Script runs through EVERY game in the Play-In Brackets and the Round 1 games, then automatically continues through the matchups until it outputs a winning team.

## How to Install
1. Download both `main.py` and `Bracket_Teams.csv`
2. Create a Python Environment
  `python3 -m venv venv`
3. Activate Python Environment
   `source venv/bin/activate`
4. Install OpenAI and Pandas
   `pip install pandas openai`
5. Inside `main.py` replace `<IP ADDRESS>` with the actual IP Address of your LLM server
6. Run `main.py`
   `python3 main.py`


## Deciphering Output
The Script outputs the next series of Matchups. So as an example of what that looks like;
`[('Duke', 'Michigan'), ('Florida', 'Arizona')]`

When there are no matchups left, it will output just the final team name.

If you'd like to see an example of what the output looks like in it's entirety, you can check inside the `Brackets` folder which houses the outputs of the model named in the file.
