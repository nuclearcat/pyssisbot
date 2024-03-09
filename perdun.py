#!/usr/bin/env python3

import os
# discord
import discord
from discord.ext import commands
import random
import re

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
    # lowercase and check if message contains 'когда проверят анкету' words sequence
    seq = ['когда', 'проверят', 'анкету']
    if all(x in message.content.lower() for x in seq):
        print('Когда проверят анкету!!!')
        await message.channel.send(file=discord.File('1bL9Q4iOOd0.jpg'))
    # lowercase and check if message contains 'актива опять нет' words sequence
    seq = ['актива', 'нет']
    if all(x in message.content.lower() for x in seq):
        print('Актива нет!!!')
        await message.channel.send(file=discord.File('сука.png'))
    # answer for 'hello'
    if message.content.startswith('Привет Пердун' or 'Пердун'):
        await message.channel.send(file=discord.File('c0W7sBP0A5c.jpg'))
    await bot.process_commands(message)


def get_token():
    global DISCORD_TOKEN
    # check if file .token exists
    if os.path.isfile('perdun.token'):
        with open('perdun.token', 'r') as f:
            DISCORD_TOKEN = f.read().strip()
    else:
        DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
    return DISCORD_TOKEN

# COMMANDS
# penis command
@bot.command(name='penis')
async def penis(ctx):
    # send pic 
    await ctx.send(file=discord.File('fd.png'))
    # send message
    # await ctx.send('Если Лера не выучит питон, то она...')

# roll command
@bot.command(name='roll')
async def roll(ctx, *, dice_expression: str):
    try:
        # Parse the expression
        match = re.match(r'(\d+)d(\d+)([+-]\d+)?', dice_expression)
        if not match:
            raise ValueError("Возможно, вы не поставили 1 перед 'd'")
        num_dice, die_type, modifier = match.groups()
        num_dice, die_type, modifier = int(num_dice), int(die_type), int(modifier) if modifier else 0

        # Roll the dice and sum
        rolls = [random.randint(1, die_type) for _ in range(num_dice)]
        total = sum(rolls) + modifier

        # Send the response
        message = f'Выкинуто {num_dice}d{die_type} + {modifier}: {rolls} = **{total}**'
        await ctx.send(message)
        
    except ValueError as e:
        await ctx.send(f"Неверный формат: {e}")

    
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
    

