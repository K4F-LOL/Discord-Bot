import discord
from discord.ext import commands, tasks
from datetime import datetime
from discord import app_commands
import asyncio
import Utils.bot_util as util




class poll2Cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.active_polls = {} 
    
    async def send_response(self, ctx, content=None, embed=None, ephemeral=False, delete_after=None,view=None):
        if ctx.interaction:
            if ephemeral:
                if embed:
                    await ctx.interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    await ctx.interaction.response.send_message(content, ephemeral=True)
                return None
            else:
                if view:
                    if embed:
                        await ctx.interaction.response.send_message(embed=embed,view=view )
                    else:
                        await ctx.interaction.response.send_message(content,view=view)
                else:
                    if embed:
                        await ctx.interaction.response.send_message(embed=embed )
                    else:
                        await ctx.interaction.response.send_message(content)
                 
                msg = await ctx.interaction.original_response()
                return msg
        else:
            if delete_after:
                if embed:
                    return await ctx.send(embed=embed, delete_after=delete_after)
                else:
                    return await ctx.send(content, delete_after=delete_after)
            else:
                if embed:
                    return await ctx.send(embed=embed,view=view )
                else:
                    return await ctx.send(content,view=view )

    
    @commands.hybrid_command(name="poll", description="Create a poll with voting options")
    @app_commands.describe(
        minutes="How many minutes the poll should run",
        title="The poll question/title",
        option1="First option (leave all empty for Yes/No poll)",
        option2="Second option (optional)",
        option3="Third option (optional)",
        option4="Fourth option (optional)",
        option5="Fifth option (optional)",
        option6="Sixth option (optional)",
        option7="Seventh option (optional)",
        option8="Eighth option (optional)"
    )
    async def poll(
        self, 
        ctx: commands.Context, 
        minutes: int, 
        title: str,
        option1: str = None,
        option2: str = None,
        option3: str = None,
        option4: str = None,
        option5: str = None,
        option6: str = None,
        option7: str = None,
        option8: str = None
    ):
        # Collect non-None options into a tuple
        options = tuple(opt for opt in [option1, option2, option3, option4, option5, option6, option7, option8] if opt is not None)

        if ctx.channel.id != 1468018537850470520:
            await self.send_response(ctx, "❌ This is not the right channel. Please use this command in the poll channel.", ephemeral=True)
            return

        user_id = ctx.author.id

        if user_id in self.active_polls:
            await self.send_response(ctx, "❌ You already have an active poll running. Stop it first with `!stoppoll` or `/stoppoll`", ephemeral=True)
            return
       
        # Enhanced description
        description_text = (
            f"⏰ **Time Remaining:** {minutes} minute{'s' if minutes != 1 else ''}\n"
            f"👤 **Created by:** {ctx.author.mention}\n"
            f"📊 **Vote Type:** {'Yes/No' if len(options) == 0 else f'{len(options)} Options'}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"React below to cast your vote! 🗳️"
        )
        
        if len(options) == 0:

            pollembed = discord.Embed(
                title=f"📊 -----{title}-----",
                description=description_text,
                color=discord.Color.blue(),
                timestamp=datetime.now()
            )
            pollembed.set_author(
                name=f"Poll by {ctx.author.display_name}",
                icon_url=ctx.author.display_avatar.url
            )
            pollembed.set_thumbnail(url=ctx.author.display_avatar.url)
            pollembed.set_footer(
                text=f"Poll ID: {user_id}",
                icon_url=ctx.guild.icon.url if ctx.guild.icon else None
            )
            
           
            class YesNoButtons(discord.ui.View):

                def __init__(self):
                    super().__init__(timeout=None)
                    self.yes_voters = set()  # Track who voted yes
                    self.no_voters = set()   # Track who voted no
                
                @discord.ui.button(label="YES", style=discord.ButtonStyle.success, custom_id="yes_button")
                async def yes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                    user_id = interaction.user.id
                    
                    # Remove from no if they previously voted no
                    if user_id in self.no_voters:
                        self.no_voters.remove(user_id)
                    
                    # Toggle yes vote
                    if user_id in self.yes_voters:
                        self.yes_voters.remove(user_id)
                        await interaction.response.send_message("❌ You removed your YES vote!", ephemeral=True)
                    else:
                        self.yes_voters.add(user_id)
                        await interaction.response.send_message("✅ You voted YES!", ephemeral=True)

                @discord.ui.button(label="NO", style=discord.ButtonStyle.danger, custom_id="no_button")
                async def no_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                    user_id = interaction.user.id
                    
                    # Remove from yes if they previously voted yes
                    if user_id in self.yes_voters:
                        self.yes_voters.remove(user_id)
                    
                    # Toggle no vote
                    if user_id in self.no_voters:
                        self.no_voters.remove(user_id)
                        await interaction.response.send_message("❌ You removed your NO vote!", ephemeral=True)
                    else:
                        self.no_voters.add(user_id)
                        await interaction.response.send_message("✅ You voted NO!", ephemeral=True)

            view = YesNoButtons()
            if ctx.interaction:
                pass
            else:
                if ctx.message:
                    try:
                        await ctx.message.delete()
                    except:
                        pass
            msg = await self.send_response(ctx, embed=pollembed,view=view)


        else:

            pollembed = discord.Embed(
                title=f"📊 -----{title}-----",
                description=description_text,
                color=discord.Color.green(),
                timestamp=datetime.now()
            )
            pollembed.set_author(
                name=f"Poll by {ctx.author.display_name}",
                icon_url=ctx.author.display_avatar.url
            )
            pollembed.set_thumbnail(url=ctx.author.display_avatar.url)

            
            pollembed.add_field(
                name="🎯 How to Vote",
                value="Simply click the button that matches your choice! You can change your vote anytime.",
                inline=False
            )
            
            pollembed.set_footer(
                text=f"Poll ID: {user_id}",
                icon_url=ctx.guild.icon.url if ctx.guild.icon else None
            )

            class OptionsButtons(discord.ui.Button):
                def __init__(self, option, option_index, parent_view):
                    super().__init__(
                        label=f"{option}", 
                        style=discord.ButtonStyle.primary,
                        custom_id=f"option_{option_index}"
                    )
                    self.option = option
                    self.parent_view = parent_view  
                
                async def callback(self, interaction: discord.Interaction):
                    user_id = interaction.user.id
                    
                    
                    for opt in self.parent_view.option_voters:
                        if user_id in self.parent_view.option_voters[opt]:
                            self.parent_view.option_voters[opt].remove(user_id)
                    
                    
                    if user_id in self.parent_view.option_voters[self.option]:
                        self.parent_view.option_voters[self.option].remove(user_id)
                        await interaction.response.send_message(
                            f"❌ You removed your vote for **{self.option}**!", 
                            ephemeral=True
                        )
                    else:
                        self.parent_view.option_voters[self.option].add(user_id)
                        await interaction.response.send_message(
                            f"✅ You voted for **{self.option}**!", 
                            ephemeral=True
                        )
          
            
            class ViewButton(discord.ui.View):
                def __init__(self, options):
                    super().__init__(timeout=None)
                    self.option_voters = {}  
                    
                    for index, option in enumerate(options):
                        self.option_voters[option] = set() 
                        button = OptionsButtons(option, index,self)
                        self.add_item(button)

            view = ViewButton(options)
            msg = await self.send_response(ctx, embed=pollembed,view=view)

        
        self.active_polls[user_id] = {
            'ctx': ctx,           
            'minutes': minutes,   
            'title': title,       
            'options': options,   
            'msg': msg,          
            'loop': None,
            'view': view
        }

        loop = self.create_poll_loop(user_id) 
        self.active_polls[user_id]['loop'] = loop 
        loop.start()


    def create_poll_loop(self, user_id):

        @tasks.loop(minutes=1)
        async def poll_loop():

            if user_id not in self.active_polls:
                poll_loop.stop()
                return
            
            poll_data = self.active_polls[user_id]
            ctx = poll_data['ctx']
            minutes = poll_data['minutes']
            title = poll_data['title']
            options = poll_data['options']
            msg = poll_data['msg']
            view = poll_data['view']

            loops = poll_loop.current_loop
            remaining_time = minutes - loops

            

            if loops != 0:
                if remaining_time > 0:
                    
                    description_text = (
                        f"⏰ **Time Remaining:** {remaining_time} minute{'s' if remaining_time != 1 else ''}\n"
                        f"👤 **Created by:** <@{user_id}>\n"
                        f"📊 **Vote Type:** {'Yes/No' if len(options) == 0 else f'{len(options)} Options'}\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"Click one of the buttons to cast your vote! 🗳️"
                    )
                    
                    newembed = discord.Embed(
                        title=f"📊 -----{title}-----",
                        description=description_text,
                        color=discord.Color.orange(),  # Orange for active/updating
                        timestamp=datetime.now()
                    )
                    newembed.set_footer(
                        text=f"Poll ID: {user_id} • Updates every minute",
                        icon_url=ctx.guild.icon.url if ctx.guild.icon else None
                    )

                    await msg.edit(embed=newembed, view=view)
                   

                else:

                    if len(options)==0:

                        yes_count = len(view.yes_voters)
                        no_count = len(view.no_voters)
                        
                        results_embed = discord.Embed(
                            title=f"📊 Poll Results: ----{title}----",
                            color=discord.Color.red(),
                            timestamp=datetime.now()
                        )
                        
                        if yes_count==no_count:
                            results_embed.description = f"🤝 **It's a Draw!**\n\n✅ YES: {yes_count} votes\n❌ NO: {no_count} votes"
                            

                        elif yes_count>no_count:
                            results_embed.description = f"✅ **YES has won!**\n\n✅ YES: {yes_count} votes\n❌ NO: {no_count} votes"
                        

                        else:  
                            results_embed.description = f"❌ **NO has won!**\n\n❌ NO: {no_count} votes\n✅ YES: {yes_count} votes"
                        

                        await ctx.channel.send(embed=results_embed)
                        await msg.delete()
    

                    else:
                    
                        results_embed = discord.Embed(
                            title=f"📊 Poll Results: {title}",
                            color=discord.Color.red(),
                            timestamp=datetime.now()
                        )

                        
                        count_options = []
                        for option in options:  
                            vote_count = len(view.option_voters[option])  
                            count_options.append(vote_count)
                        
                        max_value = max(count_options) if count_options else 0
                        tied_count = count_options.count(max_value)
                        
                        
                        results_text = ""
                        for option in options:
                            vote_count = len(view.option_voters[option])
                            results_text += f"**{option}:** {vote_count} vote{'s' if vote_count != 1 else ''}\n"
                        
                        if max_value == 0:

                            results_embed.description = f"📭 **No votes received!**\n\n{results_text}"

                        elif tied_count == len(options):

                            results_embed.description = f"🤝 **It's a draw!** All options received equal votes.\n\n{results_text}"

                        elif tied_count > 1:
                            
                            tied_options = [options[i] for i, count in enumerate(count_options) if count == max_value]
                            tied_names = ", ".join(f"**{opt}**" for opt in tied_options)
                            results_embed.description = f"⚠️ **CONTROVERSIAL!** Tied between {tied_names}\n\n{results_text}"

                        else:

                            max_index = count_options.index(max_value)
                            winner = options[max_index]
                            results_embed.description = f"🏆 **Winner: {winner}** with {max_value} vote{'s' if max_value != 1 else ''}!\n\n{results_text}"
                        
                        results_embed.set_footer(text=f"Poll created by {ctx.author.display_name}")
                        await ctx.channel.send(embed=results_embed)
                        
                        await msg.delete()
    
                                
                    poll_loop.stop()
                    del self.active_polls[user_id]
        
        return poll_loop



    @commands.hybrid_command(name="listpolls", description="List all active polls (Owner only)")
    @commands.check(util.is_me)
    async def listpolls(self, ctx: commands.Context):
        if len(self.active_polls) == 0:
            await self.send_response(ctx, "📊 No active polls running.", ephemeral=True)
            return
        
        main_embed = discord.Embed(
            title="📊 Active Polls Overview",
            description=f"Currently tracking **{len(self.active_polls)}** active poll(s)",
            color=discord.Color.purple(),
            timestamp=datetime.now()
        )
        
        for poll_id in self.active_polls:
            poll_data = self.active_polls[poll_id]
            title = poll_data['title']
            minutes = poll_data['minutes']
            options = poll_data['options']
            msg = poll_data['msg']
            
            # Calculate remaining time
            loops = poll_data['loop'].current_loop
            remaining_time = minutes - loops
            
            option_text = "Yes/No" if len(options) == 0 else ", ".join(options)
            
            main_embed.add_field(
                name=f"📌 {title}",
                value=(
                    f"**Poll ID:** `{poll_id}`\n"
                    f"**Time Left:** {remaining_time} min\n"
                    f"**Options:** {option_text}\n"
                    f"[Jump to Poll]({msg.jump_url})"
                ),
                inline=False
            )
        
        main_embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        await self.send_response(ctx, embed=main_embed, ephemeral=True)
            

    @commands.hybrid_command(name="stoppoll", description="Stop an active poll")
    @app_commands.describe(user_id="User ID of the poll owner (leave empty to stop your own poll)")
    async def stoppoll(self, ctx: commands.Context, user_id: str = None):
        if user_id is None:
            user_id = ctx.author.id
        else:
            try:
                user_id = int(user_id)
            except ValueError:
                await self.send_response(ctx, "❌ Invalid poll ID. Please provide a valid number.", ephemeral=True)
                return

        if user_id != ctx.author.id and not ctx.author.guild_permissions.administrator:
            await self.send_response(ctx, "❌ You can only stop your own polls unless you're an administrator.", ephemeral=True)
            return
        
        if user_id in self.active_polls:
            poll_data = self.active_polls[user_id]
            msg1=poll_data['msg']
            poll_data['loop'].stop()
            del self.active_polls[user_id]
            
            stop_embed = discord.Embed(
                title=f"🛑 Poll: -{user_id}- Stopped",
                description=f"The poll has been stopped by {ctx.author.mention}",
                color=discord.Color.red(),
                timestamp=datetime.now()
            )
            await msg1.delete()
            msg=await self.send_response(ctx, embed=stop_embed)
            await asyncio.sleep(5)
            await msg.delete()

        else:
            await self.send_response(ctx, "❌ No poll is currently running for this user.", ephemeral=True)
            




async def setup(bot):
    await bot.add_cog(poll2Cog(bot))