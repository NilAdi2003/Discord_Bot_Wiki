import discord
from discord.ext import commands
import wikipedia as wk
from googletrans import Translator
import requests
import json

DiscordToken = ""
RapidApiToken = ""

def wikisearch(sen):
    data = wk.summary(sen,sentences=2)
    return data

def nerdJokes():
    url = "https://jokes-always.p.rapidapi.com/erJoke"
    headers = {
        "X-RapidAPI-Key": RapidApiToken,
        "X-RapidAPI-Host": "jokes-always.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    return json.loads(response.text)["data"]

def translation(sen,trg):
    trs = Translator()
    if(len(trg)==0):
        trg='eng'
        output = trs.translate(sen,dest=trg).text
    else:
        output = trs.translate(sen,dest=trg).text
    return output
    

def pickUpLines():
    url = "https://nerdy-pickup-lines1.p.rapidapi.com/cheesy-pickup-lines/random"

    headers = {
        "X-RapidAPI-Key": RapidApiToken,
        "X-RapidAPI-Host": "nerdy-pickup-lines1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers) 
    return json.loads(response.text)["random_cheesy_pickup_line"] 

def gif_gen():
    return 

def GetMovie(name):
    url = "https://movie-tv-music-search-and-download.p.rapidapi.com/search"
    querystring = {"keywords":name,"quantity":"40","page":"1"}
    headers = {
        "X-RapidAPI-Key": RapidApiToken,
        "X-RapidAPI-Host": "movie-tv-music-search-and-download.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return json.loads(response.text)

def search_torrent(query):
    api_url = f"https://yts.mx/api/v2/list_movies.json?query_term={query}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data['data']['movie_count'] > 0:
            movies = data['data']['movies']
            return [(movie['title'], movie['torrents'][0]['url']) for movie in movies]
    return []

#############################################################################################################################

Bot = commands.Bot(command_prefix="!", intents=discord.Intents.all()) 


@Bot.event
async def on_ready():
    print("(●'◡'●) ====> I am Ready for Use.")

@Bot.event
async def on_member_join(member):
    channel = Bot.get_channel(1128362204765368432)
    await channel.send("Welcome to BOTS-LAB")

@Bot.event
async def on_member_leave(member):
    channel = Bot.get_channel(1239959942505431110)
    await channel.send("Bye Bye")

@Bot.command()
async def hi(ctx):
    await ctx.send(f"Hello {ctx.author.mention}")
    data = [f"Guild: {ctx.guild}",f"Channel: {ctx.channel}",f"Author: {ctx.author}"]
    print(data)

# nerdy jokes   
@Bot.command()
async def nerdjokes(ctx):
    await ctx.send(nerdJokes())

#pickUp lines
@Bot.command()
async def pickup(ctx):
    await ctx.send(pickUpLines())

#wikipedia search
@Bot.command()
async def search(ctx,sen):
    await ctx.send(wikisearch(sen))

#language translation
@Bot.command()
async def translate(ctx,sen,trg):
    if(len(trg)==0):
        trg = 'eng'
    await ctx.send("Translated text: "+translation(sen,trg))

#gif 
@Bot.command()
async def gif(ctx,category):
    await ctx.send()

#movie downloader
@Bot.command()
async def getMovie(ctx,movie):
    await ctx.send(GetMovie(movie))

@Bot.command()
async def torrent(ctx, *, query: str):
    results = search_torrent(query)
    if results:
        response = '\n'.join([f"{title}: {url}" for title, url in results])
        await ctx.send(response)
    else:
        await ctx.send('No torrents found.')

Bot.run(DiscordToken)