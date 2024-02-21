#!/usr/bin/env python3

import os
# discord
import discord
from discord.ext import commands

OurIntents = discord.Intents.default()
OurIntents.message_content = True

bot = commands.Bot(command_prefix='!', intents=OurIntents)


DISCORD_TOKEN = None

# on ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# on message
@bot.event
async def on_message(message):
    print(f'{message.author} sent: {message.content}')
    if message.author == bot.user:
        return
    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')
    await bot.process_commands(message)


def get_token():
    global DISCORD_TOKEN
    # check if file .token exists
    if os.path.isfile('.token'):
        with open('.token', 'r') as f:
            DISCORD_TOKEN = f.read().strip()
    else:
        DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
    return DISCORD_TOKEN

# nudes command
@bot.command(name='nudes')
async def nudes(ctx):
    # send pic 1e9f00eff0df4ec4f6e20d5469597ace.jpg
    #await ctx.send(file=discord.File('1e9f00eff0df4ec4f6e20d5469597ace.jpg'))
    # send message
    await ctx.send('Если Лера не выучит питон, то она...')

    
def main():
    # get token
    token = get_token()
    if token is None:
        print('No token found')
        return
    # add commands
    bot.run(token)

if __name__ == '__main__':
    main()
    

