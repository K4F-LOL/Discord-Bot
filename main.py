import discord
from discord.ext import commands
from datetime import datetime
import os
from dotenv import load_dotenv
import Utils.bot_util as util

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
if not bot_token:
    raise RuntimeError("BOT_TOKEN is missing. Add it to the .env file.")



intents = discord.Intents.default()
intents.members=True
intents.message_content = True
intents.reactions = True

EXTENSIONS = (
            "Cogs.welcome",
            "Cogs.cmd",
            "Cogs.mod",
            "Cogs.admin",
            "Cogs.poll",
            "Cogs.tickets",
            "Cogs.post_ticket",
            "Cogs.spam",
            "Cogs.template"
        )



class MyBot(commands.Bot):
    async def setup_hook(self):
        for ext in EXTENSIONS:
            try:
                await self.load_extension(ext)
                print(f"Loaded {ext}")
            except Exception as e:
                print(f"Failed to load {ext}: {e}")


bot = MyBot(command_prefix='!', intents=intents, help_command=None)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"❌  Failed to sync commands: {e}")
    
    await bot.change_presence(
        activity=discord.Game(name="Use !help or /help for commands")
    )



@bot.command()
@commands.check(util.is_me)
async def unload(ctx, ext: str):
    try:
        await ctx.bot.unload_extension(f"Cogs.{ext}")
        await ctx.send(f"🧹 Unloaded `{ext}`")
    except commands.ExtensionNotLoaded:
        await ctx.send(f"⚠️ `{ext}` is not loaded")
    except commands.ExtensionNotFound:
        await ctx.send(f"❌ `{ext}` not found")
    except Exception as e:
        await ctx.send(f"💥 Error: `{e}`")

@bot.command()
@commands.check(util.is_me)
async def reload(ctx, ext: str):
    try:
        await ctx.bot.reload_extension(f"Cogs.{ext}")
        await ctx.send(f"🔄 Reloaded `{ext}`")
    except commands.ExtensionNotLoaded:
        await ctx.send(f"⚠️ `{ext}` is not loaded")
    except commands.ExtensionNotFound:
        await ctx.send(f"❌ `{ext}` not found")
    except Exception as e:
        await ctx.send(f"💥 Error: `{e}`")

@bot.command()
@commands.check(util.is_me)
async def load(ctx, ext: str):
    try:
        await ctx.bot.load_extension(f"Cogs.{ext}")
        await ctx.send(f"✅ Loaded `{ext}`")
    except Exception as e:
        await ctx.send(f"💥 Error loading `{ext}`: ```{e}```")


@bot.hybrid_command(name="help", description="Shows all available bot commands")
async def help(ctx):
    
    embed = discord.Embed(
        title="🤖 Bot Command Center",
        description="Welcome! Here's everything I can do for you.\n**Tip:** Most commands work with both `!` and `/`\n\u200b",
        color=discord.Color.blue(),
        timestamp=datetime.now()
    )
    
    # Fun & Games Commands (Everyone)
    embed.add_field(
        name="🎮 Fun & Games",
        value=(
            "`!ping` or `/ping` - Check if the bot is responsive\n"
            "`!coinflip` or `/coinflip` - Flip a coin (heads or tails)\n"
            "`!RPS <hand>` or `/rps <hand>` - Play Rock, Paper, Scissors\n"
            "┗ Use: ✌️ (scissors), ✋ (paper), or 👊 (rock)\n"
            "\u200b"
        ),
        inline=False
    )
    
    # Utility Commands (Everyone)
    embed.add_field(
        name="⏰ Utility",
        value=(
            "`!SetAlarm <HH:MM>` or `/setalarm <time>` - Set a personal alarm\n"
            "┗ Example: `!SetAlarm 14:30` or `/setalarm 14:30` (24-hour format)\n"
            "`!help` or `/help` - Shows this help message\n"
            "\u200b"
        ),
        inline=False
    )
    
    # Poll Commands (Everyone)
    embed.add_field(
        name="📊 Polls",
        value=(
            "`/poll <minutes> <title> [options...]` - Create a poll\n"
            "┗ Yes/No: `/poll 5 \"Do you like pizza?\"`\n"
            "┗ Multiple Choice: `/poll 10 \"Best color?\" Red Blue Green`\n"
            "`/stoppoll [user_id]` - Stop your poll (or any poll if admin)\n"
            "┗ Example: `/stoppoll` or `/stoppoll 123456789`\n"
            "`/listpolls` - View all active polls (Owner only)\n"
            "\u200b"
        ),
        inline=False
    )
    
    # Ticket Commands (Everyone)
    embed.add_field(
        name="🎫 Support Tickets",
        value=(
            "`!ticket_open [problem]` or `/ticket_open [problem]` - Open a new support ticket\n"
            "┗ Example: `/ticket_open I need help with the bot`\n"
            "┗ Must be used in the designated ticket channel\n"
            "\u200b"
        ),
        inline=False
    )
    
    # Check if user has "Moderator" role or is administrator
    moderator_role = discord.utils.get(ctx.guild.roles, name="Moderator")
    if (moderator_role and moderator_role in ctx.author.roles) or ctx.author.guild_permissions.administrator:
        # Moderation Commands (Moderators Only)
        embed.add_field(
            name="🛡️ Moderation Commands",
            value=(
                "**Member Management**\n"
                "`!kick <member> [reason]` or `/kick <member> [reason]` - Kick a member\n"
                "\u200b"
            ),
            inline=False
        )
        
        embed.add_field(
            name="🎙️ Voice Moderation",
            value=(
                "`!mute <member>` or `/mute <member>` - Server mute a member\n"
                "`!unmute <member>` or `/unmute <member>` - Unmute a member\n"
                "`!deafen <member>` or `/deafen <member>` - Server deafen a member\n"
                "`!undeafen <member>` or `/undeafen <member>` - Undeafen a member\n"
                "`!voicekick <member>` or `/voicekick <member>` - Disconnect from voice\n"
                "\u200b"
            ),
            inline=False
        )
        
        embed.add_field(
            name="🗑️ Channel Management",
            value=(
                "`!purge <amount>` or `/purge <amount>` - Delete messages\n"
                "┗ Example: `/purge 10` deletes 10 messages\n"
                "`!purge / <day> <month> [year]` - Delete messages after a date\n"
                "┗ Example: `!purge / 15 12 2024` deletes all after Dec 15, 2024\n"
                "\u200b"
            ),
            inline=False
        )
        
        embed.add_field(
            name="👑 Role Management",
            value=(
                "`!createrole <name>` or `/createrole <name>` - Create a new role\n"
                "`!deleterole <name>` or `/deleterole <name>` - Delete a role\n"
                "\u200b"
            ),
            inline=False
        )
        
        # Ticket Moderation Commands (Moderators Only)
        embed.add_field(
            name="🎫 Ticket Management",
            value=(
                "`!ticket_close` or `/ticket_close` - Close a ticket\n"
                "┗ Notifies the ticket owner via DM\n"
                "┗ Must be used in a ticket channel\n"
                "\u200b"
            ),
            inline=False
        )
    
    # Administrator Commands
    if ctx.author.guild_permissions.administrator:
        embed.add_field(
            name="⚙️ Admin Ticket Commands",
            value=(
                "`!ticket_assign <@member>` or `/ticket_assign <member>` - Assign ticket\n"
                "┗ Example: `/ticket_assign @StaffMember`\n"
                "┗ Must be used in a ticket channel\n"
                "\u200b"
            ),
            inline=False
        )
    
    # Check if user is the bot owner
    if ctx.author.id == 1386150521378705498:
        embed.add_field(
            name="🔧 Bot Administration (Owner Only)",
            value=(
                "`!load <cog>` - Load a cog extension\n"
                "`!unload <cog>` - Unload a cog extension\n"
                "`!reload <cog>` - Reload a cog extension\n"
                "┗ Available cogs: `welcome`, `cmd`, `mod`, `tasks`, `poll`, `tickets`\n"
                "`/listpolls` - View all active polls\n"
            ),
            inline=False
        )
    
    embed.set_footer(
        text=f"Requested by {ctx.author.display_name} | Prefix: ! or /",
        icon_url=ctx.author.display_avatar.url
    )
    embed.set_thumbnail(url=bot.user.display_avatar.url)
    
    # Send response appropriately
    if ctx.interaction:
        await ctx.interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await ctx.send(embed=embed)
        await ctx.message.delete()


bot.run(bot_token)
