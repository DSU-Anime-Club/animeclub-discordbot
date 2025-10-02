import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command(help="Calculates the sum of two numbers.")
async def calc(ctx, num: int = commands.parameter(description="The first number to be added"),
               num2: int = commands.parameter(description="The second number to be added")):
    await ctx.send('The result is ' + str((num + num2)))


@bot.command(help="Play a game of rock paper scissors.")
async def rps(ctx, choice=commands.parameter(description="Either rock, paper, or scissors")):
    player_choice = 0
    com_choice = random.randint(1, 3)
    com_choice_string = ""

    if choice == "rock":
        player_choice = 1
        if com_choice == 1:
            state = "tie"
            com_choice_string = "rock"
        elif com_choice == 2:
            state = "loss"
            com_choice_string = "paper"
        elif com_choice == 3:
            state = "win"
            com_choice_string = "scissors"

    elif choice == "paper":
        player_choice = 2
        if com_choice == 1:
            state = "win"
            com_choice_string = "rock"
        elif com_choice == 2:
            state = "tie"
            com_choice_string = "paper"
        elif com_choice == 3:
            state = "loss"
            com_choice_string = "scissors"

    elif choice == "scissors":
        player_choice = 3
        if com_choice == 1:
            state = "loss"
            com_choice_string = "rock"
        elif com_choice == 2:
            state = "win"
            com_choice_string = "paper"
        elif com_choice == 3:
            state = "tie"
            com_choice_string = "scissors"

    if state == "tie":
        game_result = "Wow! We tied!"
    elif state == "win":
        game_result = "Aw man, you won! :/"
    elif state == "loss":
        game_result = "HAHA! I reign victorious. :)"

    await ctx.send("_Rin chose " + com_choice_string + "._")
    await ctx.send(game_result)


load_dotenv()  # load .env for token to be used below.
bot.run(os.getenv('DISCORD_TOKEN'))
