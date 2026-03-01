import os
import random
import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import AllowedMentions
from discord.ext import commands
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # load .env for token to be used below.

grok_client = OpenAI(
    api_key=os.getenv('XAI_API_KEY'),
    base_url="https://api.x.ai/v1",
)

conversation_history = {}

with open("prompt.txt", "r", encoding="utf-8") as f:
    prompt = f.read()

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
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the server"))
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('--------------------------------------------')
    scheduler.add_job(send_meeting_announcement, "cron", day_of_week="tue", hour=MEETING_ANNOUNCEMENT_HOUR,
                      minute=MEETING_ANNOUNCEMENT_MINUTE)
    scheduler.start()


async def send_meeting_announcement():
    channel = bot.get_channel(ANNOUNCEMENT_CHANNEL_ID)
    await channel.send(
        f"<@&{MEETINGS_ROLE_ID}> TEST_MESSAGE",
        allowed_mentions=AllowedMentions(everyone=True))


@bot.command(help="Calculates the sum of two numbers.")
async def calc(ctx, num: int = commands.parameter(description="The first number to be added"),
               num2: int = commands.parameter(description="The second number to be added")):
    await ctx.send('The result is ' + str((num + num2)))


@bot.command(help="Play a game of rock paper scissors.")
async def rps(ctx, choice=commands.parameter(description="Either rock, paper, or scissors")):
    com_choice = random.randint(1, 3)
    moves = {1: "rock", 2: "paper", 3: "scissors"}
    com_choice_string = moves[com_choice]

    beats = {"rock": "scissors", "paper": "rock", "scissors": "paper"}

    if choice == com_choice_string:
        state = "tie"
    elif beats[choice] == com_choice_string:
        state = "win"
    else:
        state = "loss"

    if state == "tie":
        game_result = "Wow! We tied!"
    elif state == "win":
        game_result = "Aw man, you won! :/"
    elif state == "loss":
        game_result = "HAHA! I reign victorious. :)"

    await ctx.send("_Rin chose " + com_choice_string + "._")
    await ctx.send(game_result)


@bot.command()
async def ask(ctx, *, question):
    channel_id = ctx.channel.id

    if channel_id not in conversation_history:
        conversation_history[channel_id] = [
            {"role": "system",
             "content": prompt}
        ]

    conversation_history[channel_id].append({"role": "user", "content": question})

    async with ctx.typing():
        try:
            response = grok_client.chat.completions.create(
                model="grok-4-1-fast",
                messages=conversation_history[channel_id]
            )

            answer = response.choices[0].message.content

            conversation_history[channel_id].append({"role": "assistant", "content": answer})

            if len(conversation_history[channel_id]) > 31:
                conversation_history[channel_id] = [conversation_history[channel_id][0]] + conversation_history[channel_id][-30:]

            await ctx.send(answer)

        except Exception as e:
            await ctx.send(f"An error has occured: {e}")


bot.run(os.getenv('DISCORD_TOKEN'))
