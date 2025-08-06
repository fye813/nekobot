import discord
from discord.ext import tasks, commands
import os
import csv
import datetime
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

# BOT設定
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "health_log.csv")

# CSVに追記する関数
def append_csv(user, type_, value, flag=True):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, user, type_, value, flag])

# リマインド用タスク
@tasks.loop(minutes=1)
async def reminder_task():
    now = datetime.datetime.now().strftime("%H:%M")
    if now in ["07:00", "20:00"]:
        channel = bot.get_channel(CHANNEL_ID)
        await send_reminder(channel)

async def send_reminder(channel):
    view = CheckListView()
    await channel.send("🐾 お世話チェックリスト\n・餌やり\n・水替え\n・トイレ掃除", view=view)

# ボタン・Modal実装
class MealModal(discord.ui.Modal, title="餌やり記録"):
    meal_amount = discord.ui.TextInput(label="給与量", placeholder="例: 30g")

    async def on_submit(self, interaction: discord.Interaction):
        append_csv(interaction.user.name, "meal", self.meal_amount.value, True)
        await interaction.response.send_message(
            f"✅ {self.meal_amount.value} を記録しました", ephemeral=True
        )

class CheckListView(discord.ui.View):
    @discord.ui.button(label="餌やり", style=discord.ButtonStyle.primary)
    async def meal_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(MealModal())

    @discord.ui.button(label="水替え", style=discord.ButtonStyle.success)
    async def water_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        append_csv(interaction.user.name, "water", "", True)
        await interaction.response.send_message("💧 水替え完了を記録しました", ephemeral=True)

    @discord.ui.button(label="トイレ掃除", style=discord.ButtonStyle.success)
    async def toilet_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        append_csv(interaction.user.name, "toilet", "cleaned", True)
        await interaction.response.send_message("🚽 トイレ掃除完了を記録しました", ephemeral=True)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    reminder_task.start()

bot.run(TOKEN)
