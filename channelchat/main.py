#!/usr/bin/env python3
from collections import deque

from discord import VoiceState, Member
from configparser import ConfigParser
import sys
from discord.ext import commands
import getopt

from channelchat.commands import createchannel, deletechannel
from channelchat.events import dispatch
from channelchat.events.eventType import EventType
from channelchat.config import config

command_history = deque(maxlen=config.get_command_history_length())
bot = commands.Bot(command_prefix=config.get_command_prefix())


@bot.event
async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState):
    await dispatch.trigger(EventType.VOICE_STATE_UPDATE, member, before, after)


@bot.command()
async def create_channel(ctx, arg=None):
    await createchannel.create_channel(ctx, arg)


@bot.command()
async def delete_channel(ctx, arg=None):
    await deletechannel.delete_channel(ctx, arg)


@bot.command
async def undo(ctx, arg=None):
    await undo.undo(ctx, arg)


async def log(message: str):
    channel = bot.get_channel(config.get_log_channel())
    await channel.send(message)

bot.run(config.get_token())

