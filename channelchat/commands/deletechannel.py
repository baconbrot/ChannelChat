from discord.ext.commands import has_permissions


@has_permissions(manage_channels=True, manage_roles=True)
async def delete_channel(ctx, arg=None):
    if not arg:
        return
    guild = ctx.guild
    category = next(category for category in guild.categories if category.name == arg)
    for text_channel in category.text_channels:
        await text_channel.delete()
    for voice_channel in category.voice_channels:
        await voice_channel.delete()
    await category.delete()
    role = next(role for role in guild.roles if role.name == 'Channel: ' + arg)
    await role.delete()
