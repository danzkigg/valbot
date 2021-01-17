import discord
import os
import json
from aiohttp import request
from urllib.request import urlopen
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv('./cogs/.env')

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
        embed.set_thumbnail (url='https://valbot.io/img/disc/games/val-logo.png')
        embed.title = (pjdata['result']['pageContext']['data']['articles'][0]['title'])
        embed.url = 'https://playvalorant.com/en-us' + (pjdata['result']['pageContext']['data']['articles'][0]['url']['url'])
        embed.description = (pjdata['result']['pageContext']['data']['articles'][0]['description'])
        await ctx.send(embed=embed)

    #Check Valorant EU Server Status
    @commands.command()
    async def vstatus(self, ctx):
        API = os.getenv('RIOT_API')
        url = 'https://eu.api.riotgames.com/val/status/v1/platform-data?api_key=' + API

        async with request('GET', url) as response:
            data = await response.json()
            if data['maintenances'] == []:
                embed = discord.Embed()
                embed.colour = 3591856
                embed.set_thumbnail (url='https://valbot.io/img/disc/games/val-logo.png')
                embed.title = ':green_circle: **Servers are Online**'
                embed.description = "Valorant's European servers are currently **Online**!\n No maintenance is in progress."
                await ctx.send(embed=embed)

            else:
                print(f'API returned a {response.status} status')
                embed = discord.Embed()
                embed.colour = 16746010
                embed.set_thumbnail (url='https://valbot.io/img/disc/games/val-logo.png')
                embed.title = ':orange_circle: **Maintenance**'
                embed.description = "Valorant's European server are currently under **Maintenance**!"
                await ctx.send(embed=embed)

    #Leaderboard in Valorant Europe
    @commands.command()
    async def leaderboard(self, ctx):
        API = os.getenv('RIOT_API')
        url = 'https://eu.api.riotgames.com/val/ranked/v1/leaderboards/by-act/97b6e739-44cc-ffa7-49ad-398ba502ceb0?startIndex=0&api_key=' + API

        async with request('GET', url) as response:
            if response.status == 200:
                data = await response.json(content_type='text/plain;charset=utf-8')
                embed = discord.Embed()
                embed.colour = 3591856
                embed.set_thumbnail (url='https://valbot.io/img/disc/games/val-logo.png')
                embed.title = 'Valorant Leaderboard'
                embed.description = "This is currently the **TOP3** ranked players in Valorant's European server."
                embed.add_field(name = 'Place', value= ':one:', inline = True)
                embed.add_field(name = 'Nickname', value= data['players'][0]['gameName'], inline = True)
                embed.add_field(name = 'Tagline', value= data['players'][0]['tagLine'], inline = True)
                embed.add_field(name = 'Number of Wins', value= data['players'][0]['numberOfWins'], inline = True)
                embed.add_field(name = 'Ranked Rating', value= data['players'][0]['rankedRating'], inline = True)
                embed.add_field(name = '\u200b', value= '\u200b', inline = True)

                embed.add_field(name = '\u200b', value= '\u200b', inline = False)

                embed.add_field(name = 'Place', value= ':two:', inline = True)
                embed.add_field(name = 'Nickname', value= data['players'][1]['gameName'], inline = True)
                embed.add_field(name = 'Tagline', value= data['players'][1]['tagLine'], inline = True)
                embed.add_field(name = 'Number of Wins', value= data['players'][1]['numberOfWins'], inline = True)
                embed.add_field(name = 'Ranked Rating', value= data['players'][1]['rankedRating'], inline = True)
                embed.add_field(name = '\u200b', value= '\u200b', inline = True)

                embed.add_field(name = '\u200b', value= '\u200b', inline = False)

                embed.add_field(name = 'Place', value= ':three:', inline = True)
                embed.add_field(name = 'Nickname', value= data['players'][2]['gameName'], inline = True)
                embed.add_field(name = 'Tagline', value= data['players'][2]['tagLine'], inline = True)
                embed.add_field(name = 'Number of Wins', value= data['players'][2]['numberOfWins'], inline = True)
                embed.add_field(name = 'Ranked Rating', value= data['players'][2]['rankedRating'], inline = True)
                embed.add_field(name = '\u200b', value= '\u200b', inline = True)
                await ctx.send(embed=embed)

            else:
                print(f'API returned a {response.status} status')
                embed = discord.Embed()
                embed.colour = 16746010
                embed.set_thumbnail (url='https://valbot.io/img/disc/games/val-logo.png')
                embed.title = "Opps... Can't connect"
                embed.description = "Sorry! We've encountered an error, please try again later!"
                await ctx.send(embed=embed)

            

def setup(client):
    client.add_cog(MainCommands(client))