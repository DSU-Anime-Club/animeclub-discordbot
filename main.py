import os
import random
import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import AllowedMentions
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

scheduler = AsyncIOScheduler()

ANNOUNCEMENT_CHANNEL_ID = 1067939590440235122
TEST_CHANNEL_ID = 1418893571729395824
MEETINGS_ROLE_ID = 1419223956430524508
MEETING_ANNOUNCEMENT_HOUR = 12
MEETING_ANNOUNCEMENT_MINUTE = 30


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    scheduler.add_job(send_meeting_announcement, "cron", day_of_week="tuesday", hour=MEETING_ANNOUNCEMENT_HOUR,
                      minute=MEETING_ANNOUNCEMENT_MINUTE)
    scheduler.start()


async def send_meeting_announcement():
    channel = bot.get_channel(ANNOUNCEMENT_CHANNEL_ID)
    await channel.send(f"<@{MEETINGS_ROLE_ID}> Hiya! Today's meeting begins at 4:00 — be there or be square. Also, we'll be announcing the winners of the draw!", allowed_mentions=AllowedMentions(everyone=True))


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
