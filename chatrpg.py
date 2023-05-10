import os

import openai

from termcolor import colored
from dotenv import load_dotenv
from argparse import ArgumentParser

load_dotenv()
openai.organization = os.getenv("OPENAI_ORGANIZATION")
openai.api_key = os.getenv("OPENAI_API_KEY")

GPT_MODEL = "gpt-3.5-turbo"
# GPT_MODEL="gpt-4"

parser = ArgumentParser()
parser.add_argument("--auto", dest="auto", default=False, action="store_true")
parser.add_argument(
    "--model",
    default="gpt-3.5-turbo",
    choices=[
        "gpt-4",
        "gpt-4-0314",
        "gpt-4-32k",
        "gpt-4-32k-0314",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-0301",
    ],
)
args = parser.parse_args()

# import sys

# sys.exit()

with open("prompt.txt", "r") as f:
    initial_prompt = "".join(f.readlines())

game_messages = [{"role": "system", "content": initial_prompt}]

player_messages = [
    {"role": "system", "content": "You are playing a classic text rpg game"}
]

while True:
    # 1. Get the game prompt
    response = openai.ChatCompletion.create(model=args.model, messages=game_messages)

    response = response.choices[0]["message"]["content"]
    print(colored(response, "green"), "\n")

    game_messages.append({"role": "assistant", "content": response})

    if args.auto:
        player_messages.append({"role": "user", "content": response})

        # 2. Get the player prompt
        response = openai.ChatCompletion.create(
            model=args.model, messages=player_messages
        )
        response = response.choices[0]["message"]["content"]
        game_messages.append({"role": "user", "content": response})
        player_messages.append({"role": "assistant", "content": response})

        print(response, "\n")

        # print(colored(response, 'blue'), "\n")
    else:
        prompt = ""
        while prompt == "":
            prompt = input("> ").strip()
        game_messages.append({"role": "user", "content": prompt})
        print
