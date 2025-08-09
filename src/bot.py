import os
import discord, datetime
from discord.ext import commands, tasks
from config import DISCORD_TOKEN, CHANNEL_ID
from views import CheckListView, LeftoverButtonView
from data_handler import daily_summary
from data_handler import append_csv
from graph_handler import generate_monthly_graph

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"[DEBUG] Logged in as {bot.user} (ID: {bot.user.id})")

    # デバッグ用：起動したことをチャンネルに通知
    channel = await bot.fetch_channel(CHANNEL_ID)
    await channel.send(f"✅ Nekobot が起動しました ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")

    # ---起動時に通常チェックリストを投稿 -------------
    if os.getenv("BOOT_POST", "1") == "1":
        await channel.send(view=CheckListView())
        print("[DEBUG] 起動時に通常チェックリストを投稿しました")
    # -----------------------------------------------

    # スケジュール開始
    schedule_task.start()

@tasks.loop(minutes=1)
async def schedule_task():
    now = datetime.datetime.now().strftime("%H:%M")
    channel = await bot.fetch_channel(CHANNEL_ID)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    day = datetime.datetime.now().day

    if now == "07:00":
        await channel.send("🌅 朝のお世話チェックリスト", view=CheckListView())
    elif now == "09:00":
        await channel.send("⏰ 朝の餌の残量を入力してください", view=LeftoverButtonView())
        await channel.send(daily_summary(today))
    elif now == "20:00":
        await channel.send("🌙 夜のお世話チェックリスト", view=CheckListView())
    elif now == "22:00":
        await channel.send("⏰ 夜の餌の残量を入力してください", view=LeftoverButtonView())
        await channel.send(daily_summary(today))

        # 月初のみ月次グラフ送信
        if day == 1:
            img = generate_monthly_graph()
            if img:
                await channel.send("📊 月次集計グラフです", file=discord.File(img))

@bot.command(name="status")
async def status_today(ctx, *, arg=None):
    if arg != "today":
        await ctx.send("使用方法: `!status today`")
        return

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    msg = daily_summary(today)
    await ctx.send(msg)

@bot.command(name="weight")
async def record_weight(ctx, value: str):
    """体重を記録するコマンド: !weight 3.7"""
    try:
        weight = float(value)
    except ValueError:
        await ctx.send("❌ 体重は数値で入力してください。例: `!weight 3.7`")
        return

    append_csv(ctx.author.name, "weight", f"{weight}kg", True)
    await ctx.send(f"✅ 体重 {weight}kg を記録しました")

## デバッグ用
# @bot.event
# async def on_message(message):
#     print(f"[DEBUG] {message.author}: {message.content}")
#     await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
