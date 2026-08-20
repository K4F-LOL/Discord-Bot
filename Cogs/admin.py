import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import discord
from discord.ext import commands
from discord import app_commands
import Utils.bot_util as util


class Owner_Cog(commands.Cog):
     
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content == "ping owner-cog":
            await msg.channel.send("owner-cog is connected..")
    
    async def send_response(self, ctx, content, ephemeral=False, delete_after=None):
        if ctx.interaction:
            if ephemeral:
                await ctx.interaction.response.send_message(content, ephemeral=True)
            else:
                await ctx.interaction.response.send_message(content)
        else:
            if delete_after:
                await ctx.send(content, delete_after=delete_after)
            else:
                await ctx.send(content)
    
    @commands.hybrid_command(name="servername", description="Change the server name (Owner only)")
    @app_commands.describe(input="The new server name")
    @commands.check(util.is_me)
    async def servername(self, ctx: commands.Context, *, input: str):
        await ctx.guild.edit(name=input)
        await self.send_response(ctx, f"✅ Server name changed to: **{input}**", ephemeral=True)
    
    @commands.hybrid_command(name="region", description="Change the server region (Owner only)")
    @app_commands.describe(input="The new server region")
    @commands.check(util.is_me)
    async def region(self, ctx: commands.Context, *, input: str):
        await ctx.guild.edit(region=input)
        await self.send_response(ctx, f"✅ Server region changed to: **{input}**", ephemeral=True)
    
    @region.error
    async def errorhandler(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await self.send_response(ctx, "❌ Please enter a valid region", ephemeral=True)

    @commands.hybrid_command(name="ban", description="Ban a member from the server (Owner only)")
    @app_commands.describe(
        member="The member to ban",
        reason="Reason for the ban"
    )
    @commands.check(util.is_me)
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason: str = None):
        await ctx.guild.ban(member, reason=reason)
        await self.send_response(ctx, f"🔨 Banned **{member.name}** | Reason: {reason or 'No reason provided'}", ephemeral=True)
    
    @commands.hybrid_command(name="unban", description="Unban a user from the server (Owner only)")
    @app_commands.describe(input="Username of the person to unban")
    @commands.check(util.is_me)
    async def unban(self, ctx: commands.Context, *, input: str):
        banned_users = [entry async for entry in ctx.guild.bans()]
        
        for entry in banned_users:
            username = entry.user.name
            if input == username:
                await ctx.guild.unban(entry.user)
                await self.send_response(ctx, f"✅ Unbanned **{username}**", ephemeral=True)
                return
        
        await self.send_response(ctx, f"❌ User **{input}** not found in ban list", ephemeral=True)
    
    @commands.hybrid_command(name="createtextchannel", description="Create a new text channel")
    @app_commands.describe(input="Name of the text channel")
    @commands.has_permissions(manage_channels=True)
    async def createtextchannel(self, ctx: commands.Context, *, input: str):
        channel = await ctx.guild.create_text_channel(name=input)
        await self.send_response(ctx, f"✅ Created text channel: {channel.mention}", ephemeral=True)

    @commands.hybrid_command(name="createvoicechannel", description="Create a new voice channel")
    @app_commands.describe(input="Name of the voice channel")
    @commands.has_permissions(manage_channels=True)
    async def createvoicechannel(self, ctx: commands.Context, *, input: str):
        channel = await ctx.guild.create_voice_channel(name=input)
        await self.send_response(ctx, f"✅ Created voice channel: **{channel.name}**", ephemeral=True)
    
async def setup(bot):
    await bot.add_cog(Owner_Cog(bot))