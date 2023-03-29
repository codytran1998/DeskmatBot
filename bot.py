import discord
import asyncpraw
import aiohttp
import os
from dotenv import load_dotenv #dotenv is a library that hides tokens from being seen

load_dotenv() #allows us to use os library and call the getenv function to grab tokens from.env file
session = aiohttp.ClientSession()

bot_token = os.getenv('bot_token')
reddit_client_id = os.getenv('reddit_client_id')
reddit_client_secret = os.getenv('reddit_client_secret')
reddit_user_agent = os.getenv('reddit_user_agent')
discord_channel_id = int(os.getenv('discord_channel_id'))

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents = intents) #instance of a Discord Client

async def send_post(post): #this function sends a post to the channel
    channel = client.get_channel(discord_channel_id)
    reddit_thread = f"{post.title}\n{post.url}"
    await channel.send(reddit_thread)

async def check_for_deskmats(): #Main function. This function checks every new post for the word "deskmat"
    #Create a Reddit instance and give it client id, secret, and user agent, all found on Reddit's apps page
    reddit = asyncpraw.Reddit(client_id=reddit_client_id, client_secret=reddit_client_secret, user_agent=reddit_user_agent)
    mech_posts = await reddit.subreddit('mechmarket') 
    async for post in mech_posts.stream.submissions(): #for every new post in the subreddit's "stream"
        #https://asyncpraw.readthedocs.io/en/stable/code_overview/other/subredditstream.html
        if "deskmat" in (post.title + post.selftext).lower(): #check for "deskmat" in title + body
            await send_post(post) #calls send_post() to send a message when deskmat is found

@client.event #Registers an event within Discord
async def on_ready():
    print(f'We have logged in as {client.user}')
    await check_for_deskmats() #Check for deskmats as soon as bot logs in

@client.event
async def on_message(message): #async functions that wait for a message from a user
    reddit = asyncpraw.Reddit(client_id=reddit_client_id, client_secret=reddit_client_secret, user_agent=reddit_user_agent)
    mech_posts = await reddit.subreddit('mechmarket')

    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    if message.content.startswith('$new'): # $new prints out 10 newest posts on mechmarket 
        async for post in mech_posts.new(limit=10):
            await message.channel.send(f'{post.title}') #await can only be used inside async functions
        await reddit.close()


client.run(bot_token)
