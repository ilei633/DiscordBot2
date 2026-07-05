import os
import random
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")

class GIFBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def on_ready(self):
        await self.tree.sync()
        print(f"Бот {self.user} успешно запущен и готов искать гифки через GIPHY!")

bot = GIFBot()

@bot.tree.command(name="gif", description="Поиск гифок со всего интернета (GIPHY)")
@app_commands.describe(query="Что ищем?")
async def gif(interaction: discord.Interaction, query: str):
    await interaction.response.defer()

    url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={query}&limit=5"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                results = data.get("data", [])
                
                if results:
                    chosen_gif = random.choice(results)
                    gif_url = chosen_gif["url"]
                    await interaction.followup.send(f"Результат по запросу **{query}**:\n{gif_url}")
                else:
                    await interaction.followup.send(f"По запросу `{query}` ничего не найдено.")
            else:
                await interaction.followup.send("Произошла ошибка при обращении к API гифок.")

if __name__ == "__main__":
    if not TOKEN or not GIPHY_API_KEY:
        print("Ошибка: Укажите DISCORD_TOKEN и GIPHY_API_KEY в переменных окружения!")
    else:
        bot.run(TOKEN)
