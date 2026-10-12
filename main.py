
import os
import requests

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
API = f"https://api.telegram.org/bot{TOKEN}"


def send_message(chat_id, text):
    requests.post(
        f"{API}/sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=15,
    )


def main():
    if not TOKEN:
        print("Erreur : le token Telegram manque.")
        return

    offset = None
    print("Bot Telegram démarré.")

    while True:
        try:
            response = requests.get(
                f"{API}/getUpdates",
                params={"timeout": 30, "offset": offset},
                timeout=35,
            )
            response.raise_for_status()

            for update in response.json().get("result", []):
                offset = update["update_id"] + 1
                message = update.get("message", {})
                chat = message.get("chat", {})
                chat_id = chat.get("id")
                command = message.get("text", "").strip().lower()

                if not chat_id:
                    continue

                if command == "/start":
                    send_message(
                        chat_id,
                        "Salut ! Ton bot est connecté. "
                        "Utilise /help pour voir les commandes."
                    )
                elif command == "/help":
                    send_message(
                        chat_id,
                        "Commandes disponibles :\n"
                        "/start - Démarrer le bot\n"
                        "/help - Afficher l'aide\n"
                        "/annonce - Préparer une annonce Vinted"
                    )
                elif command == "/annonce":
                    send_message(
                        chat_id,
                        "Envoie-moi le nom de l'article, sa marque "
                        "et son état pour préparer une annonce."
                    )
                else:
                    send_message(
                        chat_id,
                        "Commande inconnue. Tape /help."
                    )

        except requests.RequestException as error:
            print(f"Erreur réseau : {error}")


if __name__ == "__main__":
    main()
