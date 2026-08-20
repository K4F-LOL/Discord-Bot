import discord
from datetime import datetime
from discord.ext import commands
from discord import app_commands
from discord import Forbidden, HTTPException


class ModeratorRoleCog(commands.Cog):
     
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
        if msg.content == "ping moderator-cog":
            await msg.channel.send("moderator-cog is connected")

    
    async def send_response(self, ctx, content, ephemeral=False, delete_after=None):
        if ctx.interaction:
            
            if ctx.interaction.response.is_done():
               
                await ctx.interaction.followup.send(content, ephemeral=ephemeral)
            else:

                await ctx.interaction.response.send_message(content, ephemeral=ephemeral)
        else:
            if delete_after:
                await ctx.send(content, delete_after=delete_after)
            else:
                await ctx.send(content)



    @commands.hybrid_command(name="createrole", description="Create a new role in the server")
    @app_commands.describe(input="Name of the role to create")
    @commands.has_role("Moderator")   
    async def createrole(self, ctx: commands.Context, *, input: str):
        await ctx.guild.create_role(name=input) 
        await self.send_response(ctx, f"✅ Role `{input}` created successfully!", ephemeral=True)

    @commands.hybrid_command(name="deleterole", description="Delete a role from the server")
    @app_commands.describe(role_name="Name of the role to delete")
    @commands.has_role("Moderator")   
    async def deleterole(self, ctx: commands.Context, *, role_name: str):
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            return await self.send_response(ctx, f"❌ Role `{role_name}` not found.", ephemeral=True)
        try:
            await role.delete() 
            await self.send_response(ctx, f"✅ Role `{role_name}` deleted successfully!", ephemeral=True)
        except Forbidden:
            await self.send_response(ctx, "❌ I don't have permission to delete this role!", ephemeral=True)
        except HTTPException as e:
            await self.send_response(ctx, f"⚠️ Something went wrong: {e}", ephemeral=True)
    
    @commands.hybrid_command(name="kick", description="Kick a member from the server")
    @app_commands.describe(
        member="The member to kick",
        reason="Reason for kicking"
    )
    @commands.has_role("Moderator") 
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason: str = None):
        await ctx.guild.kick(member, reason=reason)
        await self.send_response(ctx, f"👢 Kicked **{member.name}** | Reason: {reason or 'No reason provided'}", ephemeral=True)

    @commands.hybrid_command(name="mute", description="Server mute a member in voice")
    @app_commands.describe(member="The member to mute")
    @commands.has_role("Moderator") 
    async def mute(self, ctx: commands.Context, member: discord.Member):
        if not member.voice:
            return await self.send_response(ctx, f"❌ {member.mention} is not in a voice channel!", ephemeral=True)
        await member.edit(mute=True)
        await self.send_response(ctx, f"🔇 Muted **{member.name}** in voice", ephemeral=True)
    
    @commands.hybrid_command(name="unmute", description="Unmute a member in voice")
    @app_commands.describe(member="The member to unmute")
    @commands.has_role("Moderator") 
    async def unmute(self, ctx: commands.Context, member: discord.Member):
        if not member.voice:
            return await self.send_response(ctx, f"❌ {member.mention} is not in a voice channel!", ephemeral=True)
        await member.edit(mute=False)
        await self.send_response(ctx, f"🔊 Unmuted **{member.name}** in voice", ephemeral=True)

    @commands.hybrid_command(name="deafen", description="Server deafen a member in voice")
    @app_commands.describe(member="The member to deafen")
    @commands.has_role("Moderator") 
    async def deafen(self, ctx: commands.Context, member: discord.Member):
        if not member.voice:
            return await self.send_response(ctx, f"❌ {member.mention} is not in a voice channel!", ephemeral=True)
        await member.edit(deafen=True)
        await self.send_response(ctx, f"🔇 Deafened **{member.name}** in voice", ephemeral=True)
                          
    @commands.hybrid_command(name="undeafen", description="Undeafen a member in voice")
    @app_commands.describe(member="The member to undeafen")
    @commands.has_role("Moderator") 
    async def undeafen(self, ctx: commands.Context, member: discord.Member):
        if not member.voice:
            return await self.send_response(ctx, f"❌ {member.mention} is not in a voice channel!", ephemeral=True)
        await member.edit()
        await self.send_response(ctx, f"🔊 Undeafened **{member.name}** in voice", ephemeral=True)
    
    @commands.hybrid_command(name="voicekick", description="Disconnect a member from voice channel")
    @app_commands.describe(member="The member to disconnect")
    @commands.has_role("Moderator") 
    async def voicekick(self, ctx: commands.Context, member: discord.Member):
        if not member.voice:
            return await self.send_response(ctx, f"❌ {member.mention} is not in a voice channel!", ephemeral=True)
        await member.edit(voice_channel=None)
        await self.send_response(ctx, f"👢 Disconnected **{member.name}** from voice", ephemeral=True)
    

    @commands.hybrid_command(name="purge", description="Delete messages in the channel")
    @app_commands.describe(
        amount="Number of messages to delete, or use '/' for date-based purge",
        day="Day for date-based purge (if amount is '/')",
        month="Month for date-based purge (if amount is '/')",
        year="Year for date-based purge (optional, defaults to current year)"
    )
    @commands.has_role("Moderator")
    async def purge(self, ctx: commands.Context, amount: str, day: int = None, month: int = None, year: int = None):

        if ctx.interaction:
            # Defer immediately to avoid "did not respond"
            await ctx.interaction.response.defer(ephemeral=True)

        if year is None:
            year = datetime.now().year

        try:
            # DATE-BASED PURGE
            if amount == "/":
                if day is None or month is None:
                    if ctx.interaction:
                        await ctx.interaction.followup.send(
                            "❌ Please provide both day and month with the command for date-based purge.",
                            ephemeral=True
                        )
                    else:
                        await ctx.send(
                            "❌ Please provide both day and month with the command for date-based purge.",
                            delete_after=5
                        )
                    return

                deleted = await ctx.channel.purge(after=datetime(year, month, day))
                message_text = f"🗑️ Deleted {len(deleted)} messages after {month}/{day}/{year}"

            # NUMBER-BASED PURGE
            else:
                num = int(amount)
                if ctx.interaction:
                    deleted = await ctx.channel.purge(limit=num)
                else:
                    deleted = await ctx.channel.purge(limit=num + 1)
                message_text = f"🗑️ Deleted {len(deleted)} messages"

            # SEND THE RESULT
            if ctx.interaction:
                await ctx.interaction.followup.send(message_text, ephemeral=True)
            else:
                await ctx.send(message_text, delete_after=5)

        except ValueError:
            if ctx.interaction:
                await ctx.interaction.followup.send(
                    "❌ Amount must be a number or '/' for date-based purge.",
                    ephemeral=True
                )
            else:
                await ctx.send(
                    "❌ Amount must be a number or '/' for date-based purge.",
                    delete_after=5
                )

        


    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await self.send_response(ctx, "❌ You need the **Moderator** role to use this command.", ephemeral=True)
        if isinstance(error, commands.MissingRequiredArgument):
            await self.send_response(ctx, "❌ You have to specify either a date or a number.", ephemeral=True)
        elif isinstance(error, commands.CommandInvokeError):
            await self.send_response(ctx, "❌ Invalid input. Use a number or '/' followed by day and month.", ephemeral=True)
    

    @createrole.error
    @kick.error
    @mute.error
    @deleterole.error
    @unmute.error
    @deafen.error
    @undeafen.error
    async def role_error_handler(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await self.send_response(ctx, "❌ You need the **Moderator** role to use this command.", ephemeral=True)



async def setup(bot):
    await bot.add_cog(ModeratorRoleCog(bot))