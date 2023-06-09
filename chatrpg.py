import os
import time
from argparse import ArgumentParser

import openai
from termcolor import colored
from dotenv import load_dotenv

GPT_MODEL_CHOICES = [
    "gpt-4",
    "gpt-4-0314",
    "gpt-4-32k",
    "gpt-4-32k-0314",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301",
]

load_dotenv()
openai.organization = os.getenv("OPENAI_ORGANIZATION")
openai.api_key = os.getenv("OPENAI_API_KEY")

parser = ArgumentParser()
parser.add_argument(
    "--auto",
    dest="auto",
    default=False,
    action="store_true",
    help="Have an AI play the game for you.",
)
parser.add_argument(
    "--theme",
    default="fantasy adventure",
    help=("The theme for the RPG")
)
parser.add_argument(
    "--model",
    default="gpt-3.5-turbo",
    help=(
        "Set the AI Model used for the player and game AIs. "
        "For information about available models see "
        "https://platform.openai.com/docs/models/model-endpoint-compatibility"
    ),
)
parser.add_argument(
    "--player-model",
    help=(
        "Set the AI Model used for the player AI. Overrides --model"
    ),
)
parser.add_argument(
    "--game-model",
    help=(
        "Set the AI Model used for the game AI. Overrides --model"
    ),
)

args = parser.parse_args()
PLAYER_MODEL = args.player_model or args.model
GAME_MODEL = args.game_model or args.model

with open("prompt.txt", "r") as f:
    initial_prompt = "".join(f.readlines()).format(args.theme)

game_messages = [{"role": "system", "content": initial_prompt}]
player_messages = [
    {
        "role": "system",
        "content": (
            "You are playing a classic text rpg game. "
            "The game will present you with a scenario. "
            "Respond in first person with an action you take. "
            "Do not talk about the outcome of your action. "
            "Keep your response short. "
        ),
    }
]


def typing_effect(text, delay=0.01, color="white"):
    for character in text:
        print(colored(character, color), end="", flush=True)
        time.sleep(delay)
    print("\n")


while True:
    # 1. Get the game prompt
    response = openai.ChatCompletion.create(model=GAME_MODEL, messages=game_messages)
    response = response.choices[0]["message"]["content"]
    game_messages.append({"role": "assistant", "content": response})

    typing_effect(response, color="green")

    if args.auto:
        player_messages.append({"role": "user", "content": response})

        # 2. Get the player prompt
        response = openai.ChatCompletion.create(
            model=PLAYER_MODEL, messages=player_messages
        )
        response = response.choices[0]["message"]["content"]
        game_messages.append({"role": "user", "content": response})
        player_messages.append({"role": "assistant", "content": response})

        typing_effect("> " + response)

    else:
        prompt = ""
        while prompt == "":
            prompt = input("> ").strip()
        game_messages.append({"role": "user", "content": prompt})
        print()
