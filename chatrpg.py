import os
import logging
from argparse import ArgumentParser

import openai
from termcolor import colored
from dotenv import load_dotenv

# logging.basicConfig(loglevel=logging.ERROR)

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
    help=(
        "The default GPT Model used by both the AI generating and playing the RPG Adventure. "
        "For information about available models see "
        "https://platform.openai.com/docs/models/model-endpoint-compatibility"
    ),
)
parser.add_argument(
    "--player-model",
    # default="gpt-3.5-turbo",
    choices=[
        "gpt-4",
        "gpt-4-0314",
        "gpt-4-32k",
        "gpt-4-32k-0314",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-0301",
    ],
    help=(
        "The GPT Model used by the AI playing the RPG Adventure. Overrides the default model. "
        "For information about available models see "
        "https://platform.openai.com/docs/models/model-endpoint-compatibility"
    ),
)
parser.add_argument(
    "--game-model",
    choices=[
        "gpt-4",
        "gpt-4-0314",
        "gpt-4-32k",
        "gpt-4-32k-0314",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-0301",
    ],
    help=(
        "The GPT Model used by the AI generating the RPG Adventure. Overrides default model "
        "For information about available models see "
        "https://platform.openai.com/docs/models/model-endpoint-compatibility"
    ),
)
args = parser.parse_args()

PLAYER_MODEL = args.player_model or args.model
GAME_MODEL = args.game_model or args.model

with open("prompt.txt", "r") as f:
    initial_prompt = "".join(f.readlines())

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

while True:
    # 1. Get the game prompt
    response = openai.ChatCompletion.create(model=GAME_MODEL, messages=game_messages)
    response = response.choices[0]["message"]["content"]
    game_messages.append({"role": "assistant", "content": response})
    print(colored(response, "green"), "\n")

    if args.auto:
        player_messages.append({"role": "user", "content": response})

        # 2. Get the player prompt
        response = openai.ChatCompletion.create(
            model=PLAYER_MODEL, messages=player_messages
        )
        response = response.choices[0]["message"]["content"]
        game_messages.append({"role": "user", "content": response})
        player_messages.append({"role": "assistant", "content": response})

        print(">", response, "\n")
    else:
        prompt = ""
        while prompt == "":
            prompt = input("> ").strip()
        game_messages.append({"role": "user", "content": prompt})
        print()
