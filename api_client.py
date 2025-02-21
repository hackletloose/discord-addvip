import requests
from datetime import datetime, timedelta

class APIClient:
    def __init__(self, base_url, api_token):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_token}",
            "Connection": "keep-alive",
            "Content-Type": "application/json"
        })

    def get_players_history(self, player_name=None, player_id=None, page=1, page_size=5):
        """
        Ruft den /api/get_players_history Endpoint auf und kann
        sowohl nach Name als auch ID filtern.

        Der Endpoint gibt ein JSON-Objekt zurück, das in etwa so aufgebaut ist:
          {
            "result": {
              "total": 4,
              "players": [...],
              "page": 1,
              "page_size": 500
            },
            ...
          }
        """
        url = f"{self.base_url}/api/get_players_history"

        # Query-Parameter für GET
        params = {
            "page": str(page),
            "page_size": str(page_size),
        }
        if player_name:
            params["player_name"] = player_name
        if player_id:
            params["player_id"] = player_id

        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()  # Erwartet ein Dict mit "result" etc.

    def find_player_id(self, name=None, pid=None):
        """
        Ruft get_players_history auf und gibt den player_id-Wert
        des ersten Eintrags zurück, falls vorhanden.

        Der JSON-Aufbau erfordert:
          data["result"]["players"] -> Liste der Spielerdaten.
          Im ersten Element: ["player_id"] -> z. B. "76561198036685843".
        """
        if not name and not pid:
            raise ValueError("Weder Spielername noch ID wurden übergeben")

        data = self.get_players_history(player_name=name, player_id=pid)
        # "result" => {"players": [...], ...}
        result = data.get("result", {})
        players = result.get("players", [])
        if not players:
            # Keine Spieler gefunden
            return None

        # Nimm den ersten Treffer
        first_hit = players[0]
        return first_hit.get("player_id")

    def add_vip(self, player_id, description=None):
        """
        Vergibt einen 24h-VIP-Status an die angegebene player_id.
        """
        expiration = (datetime.utcnow() + timedelta(hours=2)).isoformat()
        url = f"{self.base_url}/api/add_vip"
        data = {
            "player_id": player_id,
            "description": description,
            "expiration": expiration
        }
        resp = self.session.post(url, json=data)
        resp.raise_for_status()
        return resp.json()  # z. B. "VIP added"
