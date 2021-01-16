import discord
import os
import json
from aiohttp import request
from urllib.request import urlopen
from discord.ext import commands

class MainCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Bot is online
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is online.')

    #Valorant Game Update News
    @commands.command()
    async def v(self, ctx):
        vpatchs = urlopen('https://playvalorant.com/page-data/en-us/news/game-updates/page-data.json')
        pjson = vpatchs.read()
        pjdata = json.loads(pjson)
        embed = discord.Embed()
        embed.colour = 16729684
        embed.set_thumbnail (url='https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Valorant_logo_-_pink_color_version.svg/1200px-Valorant_logo_-_pink_color_version.svg.png')
        embed.title = (pjdata['result']['pageContext']['data']['articles'][0]['title'])
        embed.url = 'https://playvalorant.com/en-us' + (pjdata['result']['pageContext']['data']['articles'][0]['url']['url'])
        embed.description = (pjdata['result']['pageContext']['data']['articles'][0]['description'])
        await ctx.send(embed=embed)

    #Check Valorant EU Server Status
    @commands.command()
    async def vstatus(self, ctx):
        url = 'https://eu.api.riotgames.com/val/status/v1/platform-data?api_key=RGAPI-358734cc-7ff4-4e13-84c9-34bb1c1611df'

        async with request('GET', url) as response:
            data = await response.json()
            if data['maintenances'] == []:
                embed = discord.Embed()
                embed.colour = 3591856
                embed.set_thumbnail (url='https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Valorant_logo_-_pink_color_version.svg/1200px-Valorant_logo_-_pink_color_version.svg.png')
                embed.title = ':green_circle: **Servers are Online**'
                embed.description = "Valorant's European servers are currently **Online**!\n No maintenance is in progress."
                await ctx.send(embed=embed)

            else:
                print(f'API returned a {response.status} status')
                embed = discord.Embed()
                embed.colour = 16746010
                embed.set_thumbnail (url='https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Valorant_logo_-_pink_color_version.svg/1200px-Valorant_logo_-_pink_color_version.svg.png')
                embed.title = ':orange_circle: **Maintenance**'
                embed.description = "Valorant's European server are currently under **Maintenance**!"
                await ctx.send(embed=embed)


    @commands.command()
    async def test(self, ctx):
        await ctx.send ('test')

def setup(client):
    client.add_cog(MainCommands(client))