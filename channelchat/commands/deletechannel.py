from discord.ext.commands import has_permissions

from channelchat.config import config


@has_permissions(manage_channels=True, manage_roles=True)
async def delete_channel(ctx, arg=None):
    if not arg:
        return
    try:
        guild = ctx.guild
    except:
        guild = ctx
    category = next(category for category in guild.categories if category.name == arg)
    for text_channel in category.text_channels:
        await text_channel.delete()
    for voice_channel in category.voice_channels:
        await voice_channel.delete()
    await category.delete()
    role = next(role for role in guild.roles if role.name == f'{config.get_channel_role_prefix()}{arg}')
    await role.delete()
