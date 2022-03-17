import discord
from discord import Colour
from discord.ext.commands import has_permissions

from channelchat.config import config


@has_permissions(manage_channels=True, manage_roles=True)
async def create_channel(ctx, arg=None):
    if not arg:
        return
    guild = ctx.guild
    role = None
    category = None
    voice_channel = None
    text_channel = None
    try:
        role = await guild.create_role(name=f'{config.get_channel_role_prefix()}{arg}',
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