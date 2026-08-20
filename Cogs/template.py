import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime

class EmbedTemplate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="embed_template", description="Sends a visual template of a Discord embed")
    async def embed_template(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Title goes here",
            url="https://example.com",
            description="Description text goes here — this is the main body of your embed message.",
            color=0x5865F2,
            timestamp=datetime.utcnow(),
        )
      
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1462484876090671118/1484022005270581409/ChatGPT_Image_Mar_19_2026_03_53_28_AM.png?ex=69bcb6b1&is=69bb6531&hm=3a38345f95380dcafd989d3ae8f79e50b6f1530b70560f8abc24f961137c92d8&")
        embed.add_field(name="Field name", value="Field value",              inline=True)
        embed.add_field(name="Field name", value="Field value",              inline=True)
        embed.add_field(name="Field name", value="Field value (full width)", inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1462484876090671118/1484021924198748280/ChatGPT_Image_Mar_19_2026_03_52_53_AM.png?ex=69bcb69e&is=69bb651e&hm=ba7a2e21be0832f0f5eda3e5e061b56f0d8e9f082403e44109b41637404cdfb4&")
        embed.set_footer(
            text="Footer text goes here",
            icon_url="https://cdn.discordapp.com/embed/avatars/1.png",
        )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(EmbedTemplate(bot))