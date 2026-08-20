import discord
from discord.ext import commands
from collections import defaultdict
from datetime import datetime, timedelta
import re


class Spam_Detect_Cog(commands.Cog):
     
    def __init__(self, bot):
        self.bot = bot
        self.user_messages = defaultdict(list)
        self.user_warnings = defaultdict(int)
        self.numb_timeouts = defaultdict(int)
        self.SPAM_THRESHOLD = 5 
        self.SPAM_THRESHOLD = 5  # messages
        self.SPAM_INTERVAL = 5  # seconds
        self.DUPLICATE_THRESHOLD = 3  # same message count

    def is_spam(self, message, user_id):

        now=datetime.now()

        self.user_messages[user_id]=[
            (msg,timestamp) for  msg, timestamp in self.user_messages[user_id]
            if now-timestamp < timedelta(seconds=self.SPAM_INTERVAL)]
        
        self.user_messages[user_id].append((message.content, now))

        if len(self.user_messages[user_id]) > self.SPAM_THRESHOLD:
            return True, "sending messages too quickly"

        recent_messages = [msg for msg, _ in self.user_messages[user_id]]
        if recent_messages.count(message.content) >= self.DUPLICATE_THRESHOLD:
            return True, "sending duplicate messages"

        return False,None
    
    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return
        if not message.guild:
            return
        if message.author.guild_permissions.administrator:
            return
        
        user_id = message.author.id
        try:
            spam_detected, reason = self.is_spam(message, user_id)
        
            if spam_detected:
                await self.handle_spam(message, reason)

        except Exception as e:
            print(f"Error in spam detection: {e}")
            import traceback
            traceback.print_exc()

    async def handle_spam(self, message, reason):

        user_id = message.author.id
        
        try:
            await message.delete()
        except discord.Forbidden:
            pass
        
        
        self.user_warnings[user_id] += 1
        
       
        warning_msg = await message.channel.send(
            f"⚠️ {message.author.mention}, please stop {reason}. "
            f"Warning {self.user_warnings[user_id]}/3"
        )
        
        await warning_msg.delete(delay=5)
        
        if self.user_warnings[user_id] >= 3:
            await self.timeout_user(message, reason)

       
    async def timeout_user(self, message, reason):

        user_id = message.author.id
        guild = message.guild 
        member = guild.get_member(user_id)

        try:
            # Timeout for 10 minutes
            await message.author.timeout(
                timedelta(seconds=60),
                reason=f"Spam: {reason}"
            )
            await message.channel.send(
                    f"🔇 {message.author.mention} has been timed out for 10 minutes due to spam.",
                    delete_after=10
                )
            
            self.user_warnings[user_id] = 0
            self.numb_timeouts[user_id]+=1

            if self.numb_timeouts[user_id]==3:
              reason="3 timeouts for spaming"

              await guild.kick(member, reason=f"Spam: {reason}")
              self.numb_timeouts[user_id]=0

              await message.channel.send(
                    f"👢 {message.author.mention} has been kicked after 3 timeouts.",
                    delete_after=10)
              
              log_channel = discord.utils.get(message.guild.channels, name='spam-logs')
                
              if log_channel:
                    embed = discord.Embed(
                                title="🚨 Spam Timeout",
                                description=f"User has been kicked for spam",
                                color=discord.Color.red(),
                                timestamp=datetime.now()
                            )
                    embed.add_field(name="User", value=message.author.mention, inline=True)
                    embed.add_field(name="Reason", value=reason, inline=True)
                    embed.add_field(name="Channel", value=message.channel.mention, inline=True)
                    embed.set_footer(text=f"User ID: {message.author.id}")
                            
                    await log_channel.send(embed=embed)
                    return
              

            await self.log_action(message, reason)

        except discord.Forbidden:
            await message.channel.send(
                f"⚠️ Cannot timeout {message.author.mention}. Missing permissions.",
                delete_after=5
            )

    async def log_action(self, message, reason):
        
        # Find log channel (you can configure this)
        log_channel = discord.utils.get(message.guild.channels, name='spam-logs')
        
        if log_channel:
            embed = discord.Embed(
                title="🚨 Spam Timeout",
                description=f"User timed out for spam",
                color=discord.Color.orange(),
                timestamp=datetime.now()
            )
            embed.add_field(name="User", value=message.author.mention, inline=True)
            embed.add_field(name="Reason", value=reason, inline=True)
            embed.add_field(name="Channel", value=message.channel.mention, inline=True)
            embed.set_footer(text=f"User ID: {message.author.id}")
            
            await log_channel.send(embed=embed)

async def setup(bot):
        await bot.add_cog(Spam_Detect_Cog(bot))