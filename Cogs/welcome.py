import discord
import random
from discord.ext import commands

GENERAL_CHANNEL_ID=1462423382283780193

class WelcomeCog(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.Cog.listener()
    async def on_member_join(self,member):#
        if member.bot:
            return 
    
        general_channel = self.bot.get_channel(GENERAL_CHANNEL_ID)

        gc_embed=discord.Embed(
            title=f"🎉 Welcome {member.name} to the server!",
            description=f"Grab a role, say hi, and let’s have some fun together 🚀",
            color=discord.Color.green()
        )
        gc_embed.set_thumbnail(url=member.display_avatar.url)
        gc_embed.set_image(
            url="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHY1bno5ajE5ZHc5ZHJmejBsZDk1dDc2cDBmbnl3emxzOXB4Yzd6bCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l0MYC0LajbaPoEADu/giphy.gif")
        if general_channel:
            await general_channel.send(embed=gc_embed)

        try:
            dm_embed=discord.Embed(
                title=f"WELCOME {member.name} TO {member.guild.name}",
                description="1️⃣ Be respectful to everyone.\n"
                    "\n"
                    "2️⃣ No spamming or excessive self-promotion.\n"
                    "\n"
                    "3️⃣ Use the correct channels for topics.\n"
                    "\n"
                    "4️⃣ No NSFW or inappropriate content.\n"
                    "\n"
                    "5️⃣ Follow Discord's Terms of Service.\n"
                    "\n"
                    "6️⃣ Listen to the moderators and admins.",
                color=discord.Color.green()
                )
            await member.send(embed=dm_embed)
        except Exception as e:
            print(f"COULDN T SEND THE MESSAGE:{e}")

    @commands.Cog.listener()
    async def on_message(self,msg):
            username=msg.author.display_name
            if msg.author.bot:
                return
            if msg.content=="Hello Bot":
                    await msg.channel.send("Hello "+username)
                    return

async def setup(bot):
        await bot.add_cog(WelcomeCog(bot))