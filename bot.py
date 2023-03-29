import discord
import asyncpraw
import aiohttp
session = aiohttp.ClientSession()

#Create a Reddit instance and give it client id, secret, and user agent, all found on Reddit's apps page

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents = intents) #instance of a Discord Client

async def send_post(post): #this function sends a post to the channel
    channel = client.get_channel(1089153330665754657)
    reddit_thread = f"{post.title}\n{post.url}"
    await channel.send(reddit_thread)

async def check_for_deskmats(): #this function checks every new post for the word "deskmat"
    reddit = asyncpraw.Reddit(client_id='HLSxhMlDURQwlw', client_secret='9ESGBsNW6-IElJ9A7JzN-RN7NAFsiA', user_agent='DeskmatBot')
    mech_posts = await reddit.subreddit('mechmarket')
    async for post in mech_posts.stream.submissions():
        if "deskmat" in (post.title + post.selftext).lower():
            await send_post(post) #calls send_post to send a message when deskmat is found

@client.event #Registers an event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await check_for_deskmats()

@client.event
async def on_message(message): #async functions that wait for a message from a user
    reddit = asyncpraw.Reddit(client_id='HLSxhMlDURQwlw', client_secret='9ESGBsNW6-IElJ9A7JzN-RN7NAFsiA', user_agent='DeskmatBot')
    mech_posts = await reddit.subreddit('mechmarket')

    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    if message.content.startswith('$new'): # $new prints out 10 newest posts on mechmarket 
        async for post in mech_posts.new(limit=10):
            await message.channel.send(f'{post.title}') #await can only be used inside async functions
        await reddit.close()


client.run('ODU3NDU4NDQ0NTU4NjYzNzAw.G6lDLN.5hvK50dChNSP5njH4i50Rfkz0mwl9jAf5hspYE')
