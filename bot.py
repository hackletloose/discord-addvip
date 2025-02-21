import os
import json
import discord
from discord.ext import commands
from dotenv import load_dotenv

from api_client import APIClient

# -------------------------------------------------------------------
# 1) Lade .env (z. B. für DISCORD_BOT_TOKEN, API_BASE_URL etc.)
# -------------------------------------------------------------------
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL")
API_TOKEN = os.getenv("API_TOKEN")
ALLOWED_CHANNEL_ID = int(os.getenv("ALLOWED_CHANNEL_ID", 0))
VIP_LOG_CHANNEL_ID = int(os.getenv("VIP_LOG_CHANNEL_ID", 0))

# -------------------------------------------------------------------
# 2) Sprache über Umgebungsvariable setzen, Default = "en"
# -------------------------------------------------------------------
LANG_CODE = os.getenv("LANG_CODE", "en")

# -------------------------------------------------------------------
# 3) Lese language.json und lade die gewünschte Sprache in "lang"
# -------------------------------------------------------------------
here = os.path.dirname(os.path.abspath(__file__))
lang_file_path = os.path.join(here, "language.json")

try:
    with open(lang_file_path, "r", encoding="utf-8") as f:
        all_translations = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"language.json nicht gefunden unter: {lang_file_path}")

if LANG_CODE not in all_translations:
    print(f"Warnung: Sprache '{LANG_CODE}' nicht in language.json gefunden. Fallback = 'en'")
    LANG_CODE = "en"

lang = all_translations[LANG_CODE]

# -------------------------------------------------------------------
# 4) Intents konfigurieren (muss auch im Developer Portal aktiviert sein)
# -------------------------------------------------------------------
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.guild_messages = True


class ConfirmVIPView(discord.ui.View):
    """
    Ein View mit zwei Buttons (z.B. auf Deutsch oder Englisch).
    """
    def __init__(self, api_client: APIClient, player_id: str, player_name: str):
        super().__init__(timeout=None)
        self.api_client = api_client
        self.player_id = player_id
        self.player_name = player_name  # sollte bereits der neueste sein

    @discord.ui.button(label=lang["confirm_vip_button"], style=discord.ButtonStyle.green)
    async def confirm_vip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        Klickt man darauf, wird tatsächlich add_vip() ausgeführt.
        """
        if not self.player_id:
            await interaction.response.send_message(
                lang["error_no_player_id"],
                ephemeral=True
            )
            return

        # VIP vergeben
        try:
            self.api_client.add_vip(self.player_id, description="VIP über Bot")
            # Text mit Platzhaltern aus language.json
            text = lang["vip_granted"].format(
                player_id=self.player_id,
                player_name=self.player_name
            )
            await interaction.response.send_message(text, ephemeral=True)
        except Exception as e:
            error_text = lang["error_vip_grant"].format(error=e)
            await interaction.response.send_message(error_text, ephemeral=True)
            return

        # VIP erfolgreich vergeben -> Embed im Log-Kanal posten
        log_channel = interaction.client.get_channel(VIP_LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(
                title=lang["new_vip_title"],
                color=discord.Color.green(),
                description=lang["new_vip_description"].format(
                    player_id=self.player_id,
                    player_name=self.player_name,
                    mention=interaction.user.mention
                )
            )
            await log_channel.send(embed=embed)

        # Beide Buttons deaktivieren
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)
        self.stop()

    @discord.ui.button(label=lang["cancel_button"], style=discord.ButtonStyle.red)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        Bricht den Vorgang ab, deaktiviert die Buttons
        und sendet eine kurze Bestätigung.
        """
        for child in self.children:
            child.disabled = True

        await interaction.message.edit(view=self)
        await interaction.response.send_message(lang["process_aborted"], ephemeral=True)
        self.stop()


class AddVIPModal(discord.ui.Modal):
    """
    Modal mit Eingabefeldern für Spielername / Spieler-ID.
    """
    def __init__(self, api_client: APIClient):
        # Modal-Titel auch aus der Sprachdatei
        super().__init__(title=lang["modal_title"])
        self.api_client = api_client

        # 1. Feld: Spielernamen (optional)
        self.player_name_input = discord.ui.TextInput(
            label=lang["label_player_name"],
            required=False
        )
        # 2. Feld: Spieler-ID (optional)
        self.player_id_input = discord.ui.TextInput(
            label=lang["label_player_id"],
            required=False
        )

        self.add_item(self.player_name_input)
        self.add_item(self.player_id_input)

    async def on_submit(self, interaction: discord.Interaction):
        name_val = self.player_name_input.value.strip()
        id_val = self.player_id_input.value.strip()

        # Wenigstens eins muss ausgefüllt sein
        if not name_val and not id_val:
            await interaction.response.send_message(
                lang["no_name_or_id"],
                ephemeral=True
            )
            return

        try:
            if id_val:
                data = self.api_client.get_players_history(player_id=id_val)
            else:
                data = self.api_client.get_players_history(player_name=name_val)

            result = data.get("result", {})
            players = result.get("players", [])
            if not players:
                await interaction.response.send_message(
                    lang["no_player_found"].format(value=(name_val or id_val)),
                    ephemeral=True
                )
                return

            player_data = players[0]
        except Exception as e:
            error_text = lang["error_search"].format(error=e)
            await interaction.response.send_message(
                error_text,
                ephemeral=True
            )
            return

        # IDs und Namen
        player_id = player_data.get("player_id", lang["unknown"])
        names = player_data.get("names", [])

        if names:
            # Neuesten Namen anhand "last_seen" ermitteln:
            most_recent = max(names, key=lambda n: n["last_seen"])
            player_name = most_recent.get("name", lang["unknown"])
        else:
            player_name = lang["unknown"]

        total_seconds = player_data.get("total_playtime_seconds", 0)
        hours = round(total_seconds / 3600.0, 2)

        # Embed erstellen
        embed = discord.Embed(
            title=lang["review_title"],
            description=lang["review_desc"],
            color=discord.Color.blue()
        )
        embed.add_field(
            name=lang["embed_field_player_id"],
            value=str(player_id),
            inline=False
        )
        embed.add_field(
            name=lang["embed_field_player_name"],
            value=player_name,
            inline=False
        )
        embed.add_field(
            name=lang["embed_field_total_playtime"],
            value=str(hours),
            inline=False
        )

        # DM an den Admin
        try:
            dm = await interaction.user.create_dm()
            view = ConfirmVIPView(self.api_client, player_id, player_name)
            await dm.send(
                content=lang["found_data_pre_dm"],
                embed=embed,
                view=view
            )
            await interaction.response.send_message(
                lang["dm_sent_info"],
                ephemeral=True
            )
        except Exception as e:
            dm_error = lang["dm_send_error"].format(error=e)
            await interaction.response.send_message(dm_error, ephemeral=True)


class AddVIPView(discord.ui.View):
    """
    View mit dem Button im öffentlichen Kanal.
    """
    def __init__(self, api_client: APIClient):
        super().__init__(timeout=None)
        self.api_client = api_client

    @discord.ui.button(
        label=lang["public_button_label"],
        style=discord.ButtonStyle.green,
        custom_id="vip_vergeben_button"
    )
    async def add_vip_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_modal(AddVIPModal(self.api_client))


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.api_client = APIClient(API_BASE_URL, API_TOKEN)

    async def setup_hook(self):
        # Registriere die persistente View
        self.add_view(AddVIPView(self.api_client))

    async def on_ready(self):
        print(f"Bot {self.user} ist online. ID={self.user.id}")
        await self.ensure_vip_button_message()

    async def ensure_vip_button_message(self):
        """
        Sucht im ALLOWED_CHANNEL_ID nach einer vorhandenen Bot-Nachricht,
        in der lang["public_button_message"] steht.
        Falls vorhanden, editiert sie und hängt (erneut) unsere View an.
        Falls nicht, sendet der Bot eine neue Nachricht.
        """
        channel = self.get_channel(ALLOWED_CHANNEL_ID)
        if not channel:
            return

        target_text = lang["public_button_message"]
        existing_message = None

        async for msg in channel.history(limit=50):
            if (
                msg.author.id == self.user.id
                and msg.content.startswith(target_text)
            ):
                existing_message = msg
                break

        if existing_message:
            # Aktualisiere die vorhandene Nachricht
            await existing_message.edit(
                content=target_text,
                view=AddVIPView(self.api_client)
            )
            print("Existierende VIP-Button-Nachricht aktualisiert.")
        else:
            # Falls keine passende Nachricht gefunden
            await channel.send(
                target_text,
                view=AddVIPView(self.api_client)
            )
            print("Neue VIP-Button-Nachricht gesendet.")


if __name__ == "__main__":
    bot = MyBot()
    bot.run(DISCORD_BOT_TOKEN)
