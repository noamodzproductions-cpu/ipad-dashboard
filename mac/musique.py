#!/usr/bin/env python3
# Petit serveur sur le Mac : l'iPad (accueil /test, carte « Musique ») appelle
# http://MacBook-Pro-de-Noam.local:8765/lofi.gif et le Mac lance le live Lofi Girl
# dans Google Chrome (sans ouvrir un 2e onglet s'il tourne déjà).
# Lancé automatiquement par ~/Library/LaunchAgents/com.noam.musique.plist
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8765
VIDEO = "CwPCy1GLS38"
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
''' % (VIDEO, URL)


def lancer():
    r = subprocess.run(["osascript", "-e", SCRIPT], capture_output=True, text=True, timeout=20)
    if r.returncode != 0:
        # pas de droit d'automatisation : on ouvre simplement le lien
        subprocess.run(["open", "-a", "Google Chrome", URL])
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


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", PORT), H).serve_forever()
