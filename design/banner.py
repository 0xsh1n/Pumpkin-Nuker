from colorama import Fore, Style
import random
import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

all_color = [Style.BRIGHT + Fore.RED, Style.BRIGHT + Fore.LIGHTCYAN_EX]
chosen_color = random.choice(all_color)

logo = '''
                                                                      
\t ██▓███   █    ██  ███▄ ▄███▓ ██▓███   ██ ▄█▀ ██▓ ███▄    █ 
\t▓██░  ██▒ ██  ▓██▒▓██▒▀█▀ ██▒▓██░  ██▒ ██▄█▒ ▓██▒ ██ ▀█   █ 
\t▓██░ ██▓▒▓██  ▒██░▓██    ▓██░▓██░ ██▓▒▓███▄░ ▒██▒▓██  ▀█ ██▒
\t▒██▄█▓▒ ▒▓▓█  ░██░▒██    ▒██ ▒██▄█▓▒ ▒▓██ █▄ ░██░▓██▒  ▐▌██▒
\t▒██▒ ░  ░▒▒█████▓ ▒██▒   ░██▒▒██▒ ░  ░▒██▒ █▄░██░▒██░   ▓██░
\t▒▓▒░ ░  ░░▒▓▒ ▒ ▒ ░ ▒░   ░  ░▒▓▒░ ░  ░▒ ▒▒ ▓▒░▓  ░ ▒░   ▒ ▒ 
\t░▒ ░     ░░▒░ ░ ░ ░  ░      ░░▒ ░     ░ ░▒ ▒░ ▒ ░░ ░░   ░ ▒░
\t░░        ░░░ ░ ░ ░      ░   ░░       ░ ░░ ░  ▒ ░   ░   ░ ░ 
\t            ░            ░            ░  ░    ░           ░ 
\t                                                            
                                                       '''

def banner(color):
    print(color + logo)

def countdown():
  print(Style.BRIGHT + Fore.LIGHTYELLOW_EX, "\n\n\t\tPreparing Nuker...", Style.RESET_ALL)
  
def countdown2():
  print(Style.BRIGHT + Fore.LIGHTYELLOW_EX, "\n\n\t\tDone...", Style.RESET_ALL)
def text():

    print("\n\t", chosen_color, "  " * 7, f"Logged in as {bot.user}", "  " * 6 + Style.RESET_ALL)
    print("\n\t", chosen_color, "  " * 8, "Made by _notpumpkin", "  " * 6 + Style.RESET_ALL)
    print("\n\t", chosen_color, "  " * 9, "!cmd for help", "  " * 6 + Style.RESET_ALL)

    
