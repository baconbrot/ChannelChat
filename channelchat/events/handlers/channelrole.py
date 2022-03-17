import discord
from discord import Member, VoiceState, Forbidden, HTTPException

from channelchat.config import config
from channelchat.events.dispatch import register
from channelchat.events.eventType import EventType


@register(EventType.VOICE_STATE_UPDATE)
async def assign_role(member: Member, before: VoiceState, after: VoiceState):
    """
    Assigns and removes "Channel: Channel-Name" roles to and from users.
    """
    if member is None or before is None or after is None:
        # await log(f'on_voice_state_update error: {member=}, {before=}, {after=}')
        return
    # Unsubscribe before text-channel
    old_role = discord.utils.get(member.guild.roles, name=f'{config.get_channel_role_prefix()}{before.channel.category.name}')
    if old_role is not None:
        try:
            await member.remove_roles(old_role, atomic=True)
        except Forbidden as e:
            print(e)
        except HTTPException as e:
            print(e)
    # Subscribe to after text-channel
    new_role = discord.utils.get(member.guild.roles, name=f'{config.get_channel_role_prefix()}{after.channel.category.name}')
    if new_role is not None:
        try:
            await member.add_roles(new_role, atomic=True)
        except Forbidden as e:
            print(e)
        except HTTPException as e:
            print(e)