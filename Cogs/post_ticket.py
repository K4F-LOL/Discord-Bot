import discord
from discord.ext import commands
import asyncio
from discord import app_commands


STAFF_ROLES = ["Moderator"]
TICKET_CHANNEL_ID=1468388227000959017

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_ready(self, ):

        ticket_channel = self.bot.get_channel(TICKET_CHANNEL_ID)

        if ticket_channel:
                await ticket_channel.purge(limit=100)

        embed = discord.Embed(
            title="🎫 Support Tickets",
            description="Click the button below to create a support ticket!",
            color=discord.Color.purple()
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1462484876090671118/1469152755838091326/ticket.png?ex=69869ea0&is=69854d20&hm=373a1fcaf85da4a61f19af479f06d80c09a829a4d076e93dcb00ae319d926178&"
            )
        
        class TicketButton(discord.ui.View):

            @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.success, row=2)
            async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
                await self.create_ticket(interaction)

            async def create_ticket(self, interaction: discord.Interaction):
                
                category = discord.utils.get(interaction.guild.categories, name="Tickets")
                if not category:
                    overwrites = {
                        interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        interaction.guild.me: discord.PermissionOverwrite(read_messages=True)
                    }
                    for role_name in STAFF_ROLES:
                        role = discord.utils.get(interaction.guild.roles, name=role_name)
                        if role:
                            overwrites[role] = discord.PermissionOverwrite(read_messages=True)
                    category = await interaction.guild.create_category("Tickets", overwrites=overwrites)

                # Step 3: Create ticket channel
                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    interaction.guild.me: discord.PermissionOverwrite(read_messages=True)
                }
                for role_name in STAFF_ROLES:
                    role = discord.utils.get(interaction.guild.roles, name=role_name)
                    if role:
                        overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

                channel = await interaction.guild.create_text_channel(
                    name=f"ticket-{interaction.user.name}",
                    overwrites=overwrites,
                    category=category,
                    topic=f"{interaction.user.id}"
                )

                # Step 4: Send ephemeral confirmation
                await interaction.response.send_message(
                    f"✅ Ticket created: {channel.mention}", ephemeral=True
                )

                # Step 5: Send embed in ticket channel
                ticket_embed = discord.Embed(
                    title="🎫 New Support Ticket",
                    description=f"Ticket Owner: {interaction.user.mention}\nStatus: 🟢 Open",
                    color=discord.Color.blue()
                )
                ticket_embed.add_field(
                    name="📝 Instructions",
                    value="Please describe your issue clearly.\n"   
                        " Staff will respond shortly."
                )
                ticket_embed.set_footer(
                    text=f"Ticket created for {interaction.user.name}",
                    icon_url=interaction.user.display_avatar.url
                )
                await channel.send(embed=ticket_embed)

        view = TicketButton()
        await ticket_channel.send(embed=embed, view=view)




    @commands.hybrid_command( name="post_ticket", description="Post the ticket button embed")
    @commands.has_role("Moderator")
    async def post_ticket(self, ctx: commands.Context):

        if ctx.interaction:
            await ctx.defer()
                
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
        
        await ctx.channel.purge(limit=1000000)

        embed = discord.Embed(
            title="🎫 Support Tickets",
            description="Click the button below to create a support ticket!",
            color=discord.Color.purple()
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1462484876090671118/1469152755838091326/ticket.png?ex=69869ea0&is=69854d20&hm=373a1fcaf85da4a61f19af479f06d80c09a829a4d076e93dcb00ae319d926178&"
            )
        
        class TicketButton(discord.ui.View):

            @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.success, row=2)
            async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
                await self.create_ticket(interaction)

            async def create_ticket(self, interaction: discord.Interaction):
                
                category = discord.utils.get(interaction.guild.categories, name="Tickets")
                if not category:
                    overwrites = {
                        interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        interaction.guild.me: discord.PermissionOverwrite(read_messages=True)
                    }
                    for role_name in STAFF_ROLES:
                        role = discord.utils.get(interaction.guild.roles, name=role_name)
                        if role:
                            overwrites[role] = discord.PermissionOverwrite(read_messages=True)
                    category = await interaction.guild.create_category("Tickets", overwrites=overwrites)

                # Step 3: Create ticket channel
                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    interaction.guild.me: discord.PermissionOverwrite(read_messages=True)
                }
                for role_name in STAFF_ROLES:
                    role = discord.utils.get(interaction.guild.roles, name=role_name)
                    if role:
                        overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

                channel = await interaction.guild.create_text_channel(
                    name=f"ticket-{interaction.user.name}",
                    overwrites=overwrites,
                    category=category,
                    topic=f"{interaction.user.id}"
                )

                # Step 4: Send ephemeral confirmation
                await interaction.response.send_message(
                    f"✅ Ticket created: {channel.mention}", ephemeral=True
                )

                # Step 5: Send embed in ticket channel
                ticket_embed = discord.Embed(
                    title="🎫 New Support Ticket",
                    description=f"Ticket Owner: {interaction.user.mention}\nStatus: 🟢 Open",
                    color=discord.Color.blue()
                )
                ticket_embed.add_field(
                    name="📝 Instructions",
                    value="Please describe your issue clearly.\n"   
                        " Staff will respond shortly."
                )
                ticket_embed.set_footer(
                    text=f"Ticket created for {interaction.user.name}",
                    icon_url=interaction.user.display_avatar.url
                )
                await channel.send(embed=ticket_embed)

        view = TicketButton()
        if ctx.interaction:
            pass
        else:
            if ctx.message:
                try:
                    await ctx.message.delete()
                except:
                    pass
                
        await ctx.channel.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(TicketSystem(bot))
