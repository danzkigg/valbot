import discord
import json
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv('.env')
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix = '.')

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

#Clear messages in bulk
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear (ctx, amount=5):
    await ctx.channel.purge(limit=amount)

client.run(TOKEN)