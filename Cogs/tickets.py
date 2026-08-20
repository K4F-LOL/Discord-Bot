import discord
import sqlite3
import asyncio
from datetime import datetime, timedelta, timezone
from discord.ext import commands, tasks
from Utils.ticket_database import TicketDatabase 
from discord import app_commands

roles = ("Moderator",)
GUILD_ID = 1462423381575208961


class tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = TicketDatabase() 
        self.auto_delete_tickets.start()
        
    
    @commands.hybrid_command(name="ticket_open", description="Open a new support ticket")
    @app_commands.describe(problem="Describe your issue")
    async def ticket_open(self, ctx: commands.Context, *, problem: str = None):

        if ctx.channel.id != 1468388227000959017:
            message = await ctx.send("❌ This is not the right channel. Please use this command in the ticket channel.", ephemeral=True)
            await asyncio.sleep(3)
            # Only delete if it's a prefix command (has a message)
            if ctx.message:
                try:
                    await ctx.message.delete()
                except:
                    pass
            try:
                await message.delete()
            except:
                pass
            return
        
        category = discord.utils.get(ctx.guild.categories, name="Tickets")
            
        if not category:  
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                ctx.guild.me: discord.PermissionOverwrite(read_messages=True)
            }
            
            for role_name in roles: 
                role = discord.utils.get(ctx.guild.roles, name=role_name)
                if role:
                    overwrites[role] = discord.PermissionOverwrite(read_messages=True)
            
            category = await ctx.guild.create_category(
                name="Tickets",
                overwrites=overwrites
            )
            
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
            
        for role_name in roles: 
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if role:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
            
           
        channel = await ctx.guild.create_text_channel(
            name=f"ticket-{ctx.author.name}",
            overwrites=overwrites,
            category=category,
            topic=f"{ctx.author.id}"
        )

        ctx_embed = discord.Embed(
            title="✅ Ticket Created Successfully!",
            description=f"Your support ticket has been created in {channel.mention}\n\nPlease head over there to describe your issue.",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )

        ctx_embed.add_field(
            name="📍 Next Steps",
            value="• Go to your ticket channel\n• Describe your issue in detail\n• Wait for staff response",
            inline=False
        )

        ctx_embed.set_footer(
            text=f"Ticket for {ctx.author.name}",
            icon_url=ctx.author.display_avatar.url
        )

        # Delete the original message if it's a prefix command
        if ctx.message:
            try:
                await ctx.message.delete()
            except:
                pass
        
        await ctx.send(embed=ctx_embed)


        channel_embed = discord.Embed(
            title="🎫 New Support Ticket",
            description=f"**Ticket Owner:** {ctx.author.mention}\n**Status:** 🟢 Open",
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow()
        )

        channel_embed.add_field(
            name="📝 Issue Description",
            value=problem if problem else "No description provided yet.",
            inline=False
        )

        channel_embed.add_field(
            name="ℹ️ Instructions",
            value="• Describe your issue in detail\n• Staff will respond shortly\n",
            inline=False
        )

        channel_embed.set_thumbnail(url=ctx.author.display_avatar.url)
        channel_embed.set_footer(
            text=f"Ticket created by {ctx.author.name}",
            icon_url=ctx.author.display_avatar.url
        )
            
        await channel.send(embed=channel_embed)

        self.db.create_ticket(
            channel_id=channel.id,
            user_id=ctx.author.id,
            username=ctx.author.name,
            problem=problem if problem else "No description provided"
        )



    @commands.hybrid_command(name="ticket_close", description="Close the current support ticket")
    async def ticket_close(self, ctx: commands.Context):
 
        if not ctx.channel.name.startswith("ticket-"):
            message = await ctx.send("❌ This isn't a ticket channel!")
            await asyncio.sleep(4)
            if ctx.message:
                try:
                    await ctx.message.delete()
                except:
                    pass
            try:
                await message.delete()
            except:
                pass
            return
        
        if not ctx.channel.topic:
            return await ctx.send("❌ This ticket has no owner information.")

    
        owner_id = int(ctx.channel.topic)
        ticket_requester = ctx.guild.get_member(owner_id)


        abob_roles = any(role.name in roles for role in ctx.author.roles)

        if not abob_roles:
            msg = await ctx.send("❌ You need the **Moderator** role to use this command.")
            await asyncio.sleep(3)
            if ctx.message:
                try:
                    await ctx.message.delete()
                except:
                    pass
            try:
                await msg.delete()
            except:
                pass
            return


        if ctx.channel.name.startswith("ticket-"):
            await ticket_requester.create_dm()
            try:
                embed = discord.Embed(
                    title="🎫 Ticket Closed",
                    description="Your support ticket has been closed.",
                    color=discord.Color.green(),
                    timestamp=discord.utils.utcnow()
                )
                embed.add_field(
                    name="Status",
                    value="✅ Issue Resolved",
                    inline=False
                )
                embed.add_field(
                    name="Closed By",
                    value=ctx.author.mention,
                    inline=True
                )
                embed.add_field(
                    name="Server",
                    value=ctx.guild.name,
                    inline=True
                )
                embed.set_footer(text="Thank you for using our support system!")
                
                await ticket_requester.dm_channel.send(embed=embed)
            except discord.Forbidden:
                pass
     
            await ctx.send("🗑️ Closing ticket...")
            self.db.close_ticket(
                channel_id=ctx.channel.id,
                closed_by=ctx.author.id
            )
            await asyncio.sleep(2)
            await ctx.channel.delete()


    @commands.hybrid_command(name="ticket_assign", description="Assign this ticket to a staff member")
    @app_commands.describe(member="The staff member to assign this ticket to")
    async def ticket_assign(self, ctx: commands.Context, member: discord.Member):

        if not ctx.author.guild_permissions.administrator:
            return await ctx.send("Admins only ❌", ephemeral=True)
    
        if not ctx.channel.name.startswith("ticket-"):
            return await ctx.send("❌ This command must be used in a ticket channel!", ephemeral=True)

        if not any(role.name in roles for role in member.roles):
            return await ctx.send("That user is not part of the staff ❌", ephemeral=True)
        
        self.db.assign_ticket(
            channel_id=ctx.channel.id,
            assigned_to=member.id
        )

        await ctx.send(f"✅ Ticket assigned to {member.mention}")


    @commands.hybrid_command(name="ticket_stats", description="View ticket statistics")
    @commands.has_permissions(administrator=True)
    async def ticket_stats(self, ctx: commands.Context):
        
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        
        cursor.execute("SELECT COUNT(*) FROM tickets")
        total = cursor.fetchone()[0]
        
        
        cursor.execute("SELECT COUNT(*) FROM tickets WHERE status = 'open'")
        open_tickets = cursor.fetchone()[0]
        
       
        cursor.execute("SELECT COUNT(*) FROM tickets WHERE status = 'closed'")
        closed_tickets = cursor.fetchone()[0]
        
        conn.close()
        
        
        embed = discord.Embed(
            title="📊 Ticket Statistics",
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow()
        )
        
        embed.add_field(name="Total Tickets", value=f"🎫 {total}", inline=True)
        embed.add_field(name="Open Tickets", value=f"🟢 {open_tickets}", inline=True)
        embed.add_field(name="Closed Tickets", value=f"🔴 {closed_tickets}", inline=True)
        
        await ctx.send(embed=embed)


    @tasks.loop(minutes=10)
    async def auto_delete_tickets(self):

        guild = self.bot.get_guild(GUILD_ID)
        
        if not guild:
            return

        category = discord.utils.get(guild.categories, name="Tickets")
        if not category:
            return

        for channel in category.text_channels:
            if not channel.name.startswith("ticket-"):
                continue

            staff_spoke = False
            async for msg in channel.history(limit=20):
                if any(role.name in roles for role in msg.author.roles):
                    staff_spoke = True
                    break

            if staff_spoke:
                continue 

            age = datetime.now(timezone.utc) - channel.created_at

            if age >= timedelta(hours=24):
                try:
                    self.db.close_ticket(
                        channel_id=channel.id,
                        closed_by=self.bot.user.id 
                    )
                    await channel.delete(reason="Auto-deleted after 24 hours")
                except discord.NotFound:
                    pass


async def setup(bot):  
    await bot.add_cog(tickets(bot))