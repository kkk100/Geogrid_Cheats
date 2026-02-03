if __name__ == "__main__":
    import os
    import requests
    from time import sleep
    DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(DATA_DIR, exist_ok=True)

    TOTAL_BOARDS = 668


    def download_json(url, filename):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            with open(filename, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"Pobrano: {filename}")
        except Exception as e:
            print(f"Błąd pobierania {url}: {e}")


    for i in range(1, TOTAL_BOARDS + 1):
        board_num = str(i)

        url_cdn = f"https://cdn-assets.teuteuf.fr/data/geogrid/boards/{board_num}.json"
        file_cdn = os.path.join(DATA_DIR, f"{board_num}_cdn.json")
        download_json(url_cdn, file_cdn)

        url_api = f"https://api.geogridgame.com/api/game/rarity/{board_num}"
        file_api = os.path.join(DATA_DIR, f"{board_num}_api.json")
        download_json(url_api, file_api)

        sleep(0.2)

    print("Pobieranie zakończone!")