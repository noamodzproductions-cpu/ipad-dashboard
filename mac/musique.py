#!/usr/bin/env python3
# Petit serveur sur le Mac : l'iPad (accueil /test, carte « Musique ») appelle
# http://MacBook-Pro-de-Noam.local:8765/lofi.gif et le Mac lance le live Lofi Girl
# dans Google Chrome (sans ouvrir un 2e onglet s'il tourne déjà).
# Lancé automatiquement par ~/Library/LaunchAgents/com.noam.musique.plist
# Depuis le Dashboard (page https), Safari bloque l'appel direct au Mac (http) : l'iPad envoie donc
# « lofi » sur le relais https ntfy.sh (canal NTFY_TOPIC) et ce script écoute ce canal en continu.
import json
import re
import subprocess
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8765
NTFY_TOPIC = "noam-musique-2ccbb2035061ec467497"
VIDEO = "rFZHOHl-L8A"
URL = "https://www.youtube.com/watch?v=" + VIDEO
GIF = b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"

SCRIPT = '''
tell application "Google Chrome"
  activate
  set nw to count of windows
  repeat with wi from 1 to nw
    set nt to count of tabs of window wi
    repeat with ti from 1 to nt
      if (URL of tab ti of window wi) contains "%s" then
        set active tab index of window wi to ti
        set index of window wi to 1
        return "deja"
      end if
    end repeat
  end repeat
  if nw = 0 then make new window
  tell front window to make new tab with properties {URL:"%s"}
  return "ouvert"
end tell
'''
# liens acceptés depuis l'iPad (le canal du relais est public : on n'ouvre que des sites de musique)
AUTORISES = re.compile(r"^https://([a-z0-9-]+\.)*(youtube\.com|youtu\.be)/[^\s\"\\]*$", re.I)


def lancer(url=URL):
    cle = VIDEO if url == URL else url
    r = subprocess.run(["osascript", "-e", SCRIPT % (cle, url)], capture_output=True, text=True, timeout=20)
    if r.returncode != 0:
        # pas de droit d'automatisation : on ouvre simplement le lien
        subprocess.run(["open", "-a", "Google Chrome", url])
        return "ouvert (open)"
    return r.stdout.strip()


class H(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/lofi"):
            try:
                etat = lancer()
                code = 200
            except Exception as e:
                etat, code = "erreur : %s" % e, 500
            print("lofi ->", etat, flush=True)
            self.send_response(code)
            self.send_header("Content-Type", "image/gif")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(GIF)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *a):
        pass


def ecouter_relais():
    """Écoute ntfy.sh en continu (connexion longue) ; reconnecte tout seul si elle coupe."""
    url = "https://ntfy.sh/%s/json" % NTFY_TOPIC
    attente = 2
    while True:
        try:
            with urllib.request.urlopen(url, timeout=90) as flux:
                attente = 2
                for ligne in flux:
                    try:
                        ev = json.loads(ligne.decode("utf-8"))
                    except ValueError:
                        continue
                    if ev.get("event") != "message":
                        continue
                    msg = ev.get("message", "").strip()
                    if msg == "lofi":
                        print("relais -> lofi ->", lancer(), flush=True)
                    elif AUTORISES.match(msg):
                        print("relais -> lien ->", lancer(msg), flush=True)
                    else:
                        print("relais -> ignoré (lien non autorisé)", flush=True)
        except Exception as e:
            print("relais coupé :", e, flush=True)
            time.sleep(attente)
            attente = min(attente * 2, 60)


if __name__ == "__main__":
    threading.Thread(target=ecouter_relais, daemon=True).start()
    HTTPServer(("0.0.0.0", PORT), H).serve_forever()
