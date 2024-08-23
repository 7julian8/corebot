# CoreBot by 7julian8!
# MIT-Licence
# Copyright (c) 2024 7julian8
# My english is very bad so change some Text if it is wrong

import discord
from discord.ext import commands
from discord.ui import Button, View
import asyncio
import random
import os
from dotenv import load_dotenv
import youtube_dl

# Erstelle eine Instanz des Bots
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Liste der Schimpfwörter
bad_words = ["scheiße", "shit", "fuck"]  # Swear

load_dotenv()
DISCORD_TOKEN = os.getenv("discord_token")
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

@bot.command()
async def play(ctx, url):
    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        voice_client.play(discord.FFmpegPCMAudio(url2))

@bot.command()
async def stop(ctx):
    voice_client = ctx.voice_client
    await voice_client.disconnect()




@client.event
async def on_ready():
    print("The Bot is now running!")
    print("-----------------------")
    await client.change_presence(activity=discord.Game(name="YourServer"))

@client.event
async def on_member_join(member):
    # Direct Message from join
    welcome_message = "Willkommen auf **YourServer**!" # Change 'YourServer' with the name of your Server!
    await member.send(welcome_message)
    
    # Welcome
    channel = discord.utils.get(member.guild.text_channels, name='lol')  # Change 'lol' with the channel
    if channel:
        await channel.send(f"Welecome {member.mention} on **yourServer**!") # Change 'yourServer' with the name of your server!


@client.event
async def on_message(message):
    if message.author.bot:
        return

    # Blocked words
    if any(word in message.content.lower() for word in bad_words):
        await message.delete()
        warn_message = f"Hey {message.author.mention}! please don't swear"
        await message.channel.send(warn_message, delete_after=5.0)
        
        # Create a 10 min timeout for swearing
        try:
            await message.author.timeout(duration=600, reason="Cursing & Swearing")
            timeout_message = f"{message.author.mention} got timeouted"
            await message.channel.send(timeout_message)
        except discord.Forbidden:
            error_message = f"I do not have permission, to timeout {message.author.mention}!"
            await message.channel.send(error_message)

    await client.process_commands(message)

# Commands
@client.command()
async def invite(ctx):
    await ctx.send("Share the Server with you Friends! Link: discord.gg/yourinvitelink")

@client.command()
async def service(ctx):
    help_message = """
    # SERVICE MENU
    `!service` - Show's this menu.
    `!about` - About the bot.
    `!invite` - Share the Server with others!
    `!kick [user]` - Kick's a user.
    `!ban [user]` - banning a user.
    `!mute [user]` - muting a user.
    `!joke` - Say's a joke.
    `!quote` - Show's a quote.
    """
    await ctx.send(help_message)

@client.command()
async def about(ctx):
    button = Button(label="Source Code", url="https://github.com/7julian8/corebot")
    view = View()
    view.add_item(button)
    await ctx.send("Link to Code", view=view) # Please let the source code at the button. I would be happy about that! :)

@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} got kicked.")

@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} got banned.")

@client.command()
async def mute(ctx, member: discord.Member, *, reason=None):
    mute_role = discord.utils.get(ctx.guild.roles, name='Muted')  # Change muted with the mute role
    if mute_role:
        await member.add_roles(mute_role, reason=reason)
        await ctx.send(f"{member.mention} got muted.")

@client.command()
async def joke(ctx):
    jokes = ["Insert the joke here!"]
    await ctx.send(random.choice(jokes))

@client.command()
async def quote(ctx):
    quotes = ["Insert quote here!"]
    await ctx.send(random.choice(quotes))

# Token
client.run('Insert your token in here!')
