#!/usr/bin/env python
import discord
from discord import VoiceState, Member, Forbidden, HTTPException, Colour
from configparser import ConfigParser
from discord.ext import commands
from discord.ext.commands import has_permissions

config = ConfigParser()
config.read('config.ini')
token = config.get('main', 'token')
log_channel = int(config.get('log', 'channel'))


bot = commands.Bot(command_prefix='!')

last_command_create = False
last_args = None

def get_channel_role(voiceState: VoiceState):
    try:
        return 'Channel: ' + voiceState.channel.category.name
    except:
        return None

@bot.event
async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState):
    if member is None or before is None or after is None:
        await log(f'on_voice_state_update error: {member=}, {before=}, {after=}')
        return
    # Unsubscribe before text-channel
    old_role = discord.utils.get(member.guild.roles, name=get_channel_role(before))
    if not old_role is None:
        try:
            await member.remove_roles(old_role, atomic=True)
        except Forbidden as e:
            print(e)
        except HTTPException as e:
            print(e)
    # Subscribe to after text-channel
    new_role = discord.utils.get(member.guild.roles, name=get_channel_role(after))
    if not new_role is None:
        try:
            await member.add_roles(new_role, atomic=True)
        except Forbidden as e:
            print(e)
        except HTTPException as e:
            print(e)

async def log(message: str):
    channel = bot.get_channel(log_channel)
    await channel.send(message)

@bot.command()
@has_permissions(manage_channels=True, manage_roles=True)
async def create_channel(ctx, arg):
    guild = ctx.guild
    role = None
    category = None
    voice_channel = None
    text_channel = None
    try:
        role = await guild.create_role(name='Channel: ' + arg,
                                       color=Colour.dark_gold(),
                                       mentionable=False,
                                       reason=f'Role for {arg}-chat')
        category = await guild.create_category_channel(arg, position=1)
        voice_channel = await category.create_voice_channel('Voice')
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            role: discord.PermissionOverwrite(read_messages=True)
        }
        text_channel = await category.create_text_channel('chat', overwrites=overwrites)
    except Exception:
        if voice_channel:
            await voice_channel.delete()
        if text_channel:
            await text_channel.delete()
        if role:
            await role.delete()
        if category:
            await category.delete()
    global last_command_create
    last_command_create = True
    global last_args
    last_args = arg

@bot.command()
@has_permissions(manage_channels=True, manage_roles=True)
async def delete_channel(ctx, arg):
    guild = ctx.guild
    category = next(category for category in guild.categories if category.name == arg)
    for text_channel in category.text_channels:
        await text_channel.delete()
    for voice_channel in category.voice_channels:
        await voice_channel.delete()
    await category.delete()
    role = next(role for role in guild.roles if role.name == 'Channel: ' + arg)
    await role.delete()
    global last_command_create
    last_command_create = False
    global last_args
    last_args = arg


@bot.command()
@has_permissions(manage_channels=True, manage_roles=True)
async def undo(ctx):
    if last_command_create:
        await delete_channel(ctx, last_args)
    elif last_command_create is not None:
        await create_channel(ctx, last_args)


bot.run(token)
