import os
import json
from dotenv import load_dotenv
from discord.ext import commands, tasks
import discord
from discord import app_commands
from typing import Literal, Optional

# Load .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Load JSON data
def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)
    
# Save JSON data
def save_json(filename, content):
    with open(filename, 'w') as f:
        json.dump(content, f, indent=4)
admin_list = load_json('admins.json')
global_ban_list = load_json('global_ban_list.json')

# Initialize bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}")
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
            ret += 1
        except discord.HTTPException:
            pass

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=GUILD))
    print(f'{bot.user.name} has connected to Discord!')
# Commands
#Ping
@bot.tree.command()
async def mping(inter: discord.Interaction) -> None:
    await inter.response.send_message(f"> Pong! {round(bot.latency * 1000)}ms")


#Global Ban
@bot.tree.command()
async def mglobal_ban(inter: discord.Interaction, user: discord.Member = None):
    if str(inter.id) in admin_list:
        user_id = str(user.id)
        if user_id in global_ban_list:
            await inter.response.send_message(f"{user} already on GBL")
        else:
            global_ban_list.append(user_id)
            save_json('global_ban_list.json', global_ban_list)
            await inter.response.send_message(f"{user} successfully put on the GBL")
    else:
        await inter.response.send_message("You dont have permission to ban someone")


#Global Unban
@bot.tree.command()
async def mglobal_unban(inter:discord.Interaction, user: discord.Member = None):
    if str(inter.id) in admin_list:
        user_id = str(user.id)
        try:
            global_ban_list.remove(user_id)
            save_json('global_ban_list.json', global_ban_list)
            await inter.response.send_message(f"{user} successfully removed from the GBL")
        except:
            await inter.response.send_message(f"{user} not found in GBL")
    else:
        await inter.response.send_message("You dont have permission to unban someone")

#Uphold GBL
# @bot.event
# async def on_member_join(member: discord.member):
#     guild = bot.get_guild(int(GUILD))
#     if guild:
#         print(f"Members in {guild.name}:")
#         for member in guild.members:
#             print(f"{member.id} - {member.name}")
#             if member.id in global_ban_list:
#                 await bot.kick(member.name)


# @bot.tree.command()
# async def muphold_gbl(inter:discord.Interaction):
#     guild = bot.get_guild(int(GUILD))
#     if guild:
#         print(f"Members in {guild.name}:")
#         for member in guild.members:
#             print(f"{member.id} - {member.name}")
#             if member.id in global_ban_list:
#                 await bot.kick(member.name)
bot.run(TOKEN)