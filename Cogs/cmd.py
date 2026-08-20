import discord
import random
from discord.ext import commands
from discord import app_commands


class Cmd_Cog(commands.Cog):
     
    def __init__(self, bot):
        self.bot = bot
    
    async def send_response(self, ctx, content, ephemeral=False, delete_after=None):
        if ctx.interaction:
            if not ctx.interaction.response.is_done():
                await ctx.interaction.response.send_message(
                    content,
                    ephemeral=ephemeral
                )
            else:
                await ctx.interaction.followup.send(
                    content,
                    ephemeral=ephemeral
                )
        else:
            await ctx.send(content, delete_after=delete_after)
            
    
    @commands.hybrid_command(name="ping", description="Check if the bot is responsive")
    async def ping(self, ctx: commands.Context):
        await self.send_response(ctx, "bo3bo3",ephemeral=True)
    
    @commands.hybrid_command(name="coinflip", description="Flip a coin (heads or tails)")
    async def coinflip(self, ctx: commands.Context):
        num = random.randint(1, 2)
        if num == 1:
            await self.send_response(ctx, "🪙 **Heads**")
        else:
            await self.send_response(ctx, "🪙 **Tails**")

    @commands.hybrid_command(name="rps", description="Play Rock, Paper, Scissors with the bot")
    @app_commands.describe(hand="Choose your hand: ✌️ (scissors), ✋ (paper), or 👊 (rock)")
    @app_commands.choices(hand=[
        app_commands.Choice(name="✌️ Scissors", value="✌️"),
        app_commands.Choice(name="✋ Paper", value="✋"),
        app_commands.Choice(name="👊 Rock", value="👊")
    ])
    async def rps(self, ctx: commands.Context, hand: str):
        hands = ["✌️", "✋", "👊"]
        bothand = random.choice(hands)
        
        await self.send_response(ctx, f"You chose: {hand}\nBot chose: {bothand}")

        if hand == bothand:
            await self.send_response(ctx, "🤝 **It's a Draw!**")
        elif hand == "✌️":
            if bothand == "✋":
                await self.send_response(ctx, "🎉 **You won!**")
            elif bothand == "👊":
                await self.send_response(ctx, "🤖 **The bot won!**")
        elif hand == "✋":
            if bothand == "👊":
                await self.send_response(ctx, "🎉 **You won!**")
            elif bothand == "✌️":
                await self.send_response(ctx, "🤖 **The bot won!**")
        elif hand == "👊":
            if bothand == "✋":
                await self.send_response(ctx, "🤖 **The bot won!**")
            elif bothand == "✌️":
                await self.send_response(ctx, "🎉 **You won!**")


async def setup(bot):
    await bot.add_cog(Cmd_Cog(bot))