import discord
from data_handler import append_csv, update_meal_left

class MealModal(discord.ui.Modal, title="餌やり記録"):
    meal_given = discord.ui.TextInput(label="給与量(g)", placeholder="例: 30")
    async def on_submit(self, interaction: discord.Interaction):
        given = int(self.meal_given.value)
        append_csv(interaction.user.name, "meal", f"給与{given}g/残0g/実食{given}g", True, given, 0)
        await interaction.response.send_message(f"✅ {given}g を記録しました", ephemeral=True)

class LeftoverModal(discord.ui.Modal, title="残量記録"):
    meal_left = discord.ui.TextInput(label="残量(g)", placeholder="例: 5")
    async def on_submit(self, interaction: discord.Interaction):
        left = int(self.meal_left.value)
        updated = update_meal_left(left)
        msg = "更新できませんでした" if not updated else f"✅ 残量{left}gを記録しました"
        await interaction.response.send_message(msg, ephemeral=True)

class LeftoverButtonView(discord.ui.View):
    @discord.ui.button(label="残量を入力", style=discord.ButtonStyle.primary)
    async def leftover_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(LeftoverModal())

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
