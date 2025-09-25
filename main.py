import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command(help="Calculates the sum of two numbers.")
async def calc(ctx, arg: int = commands.parameter(description="The first number to be added"), arg2: int = commands.parameter(description="The second number to be added")):
    await ctx.send('The result is ' + str((arg + arg2)))


load_dotenv()  # load .env for token to be used below.
bot.run(os.getenv('DISCORD_TOKEN'))
