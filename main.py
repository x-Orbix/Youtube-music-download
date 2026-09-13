import scrapetube
import yt_dlp
import os
from pathlib import Path
import shutil
import zipfile
import urllib.request
import ssl
import certifi

def checkFfmpeg():
    if shutil.which("ffmpeg"):
        return "ffmpeg"

    slozka_skriptu = Path(__file__).parent
    ffmpeg_slozka = slozka_skriptu / "ffmpeg"
    ffmpeg_exe = ffmpeg_slozka / "bin" / "ffmpeg.exe"

    if ffmpeg_exe.exists():
        os.environ["PATH"] += os.pathsep + str(ffmpeg_exe.parent)
        return str(ffmpeg_exe)

    print("ffmpeg nenalezen, stahuji...")
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_cesta = slozka_skriptu / "ffmpeg.zip"

    ssl_context = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(url, context=ssl_context) as response, open(zip_cesta, "wb") as out_file:
        shutil.copyfileobj(response, out_file)

    with zipfile.ZipFile(zip_cesta, "r") as zf:
        zf.extractall(slozka_skriptu)

    zip_cesta.unlink()

    rozbalene = [p for p in slozka_skriptu.iterdir() if p.is_dir() and p.name.startswith("ffmpeg-")]
    if rozbalene:
        rozbalene[0].rename(ffmpeg_slozka)

    ffmpeg_exe = ffmpeg_slozka / "bin" / "ffmpeg.exe"
    os.environ["PATH"] += os.pathsep + str(ffmpeg_exe.parent)
    print("ffmpeg připraven.")
    return str(ffmpeg_exe)





links = ["youtube.com", "www.youtube.com", "https://www.youtube.com", "https://youtube.com"]


slozka = Path.home() / "Music" / "YTB"
slozka.mkdir(parents=True, exist_ok=True)


cls = lambda: os.system("cls")


kvality = {
    1: "128",
    2: "160",
    3: "192",
    4: "256",
    5: "320",
}

def progressHook(d):
    if d["status"] == "downloading":
        total = d.get("total_bytes") or d.get("total_bytes_estimate")
        downloaded = d.get("downloaded_bytes", 0)

        if total:
            percent = downloaded / total * 100
            bar_len = 30
            filled = int(bar_len * percent // 100)
            bar = "█" * filled + "░" * (bar_len - filled)
            rychlost = d.get("_speed_str", "").strip()
            print(f"\r[{bar}] {percent:5.1f}%  {rychlost}", end="", flush=True)
        else:
            mb = downloaded / 1024 / 1024
            print(f"\rStahuji... {mb:6.1f} MB", end="", flush=True)

    elif d["status"] == "finished":
        print("\r\n\nStahování dokončeno, konvertuji do MP3...                              ")


def getYdlStuff(kvalita):
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": kvalita,
        }],
        "outtmpl": os.path.join(slozka, "%(title)s.%(ext)s"),
        "progress_hooks": [progressHook],
        "quiet": True,
        "no_warnings": True,
    }
    return ydl_opts


def isLink(video):
    for i in links:
        if video.startswith(i):
            return video
    return False


def main():
    cls()
    print("--------------------------------------------------------------\n" \
          "                   Youtube video download\n" \
          "--------------------------------------------------------------\n\n")

    video = input("Jméno nebo odkaz videa: ")

    link = isLink(video)
    if link:
        download(link)
        return

    videos_search = list(scrapetube.get_search(video, limit=5))
    search(videos_search)

def search(videos_search):
    cls()
    if not videos_search:
        print("Nic se nenašlo.")
        input("\nENTER pro pokračování...")
        main()
        return

    print("\nNalezená videa:")
    for i, v in enumerate(videos_search, start=1):
        title = v.get("title", {}).get("runs", [{}])[0].get("text", "(bez názvu)")
        autor = v.get("longBylineText", {}).get("runs", [{}])[0].get("text", "(neznámý autor)")
        print(f"{i} - {autor} | {title}")

    choice = input("\nVyber číslo videa: ")
    try:
        idx = int(choice)
    except ValueError:
        print("Musíš zadat číslo.")
        search(videos_search)
        return

    if idx < 1 or idx > len(videos_search):
        print("Neplatná volba.")
        search(videos_search)
        return

    video_id = videos_search[idx - 1]["videoId"]
    link = f"https://www.youtube.com/watch?v={video_id}"
    download(link)


def download(link):
    cls()
    print("Vyber kvalitu MP3:")
    print("1 - Nejnižší (128 kbps)")
    print("2 - Nízká (160 kbps)")
    print("3 - Střední (192 kbps)")
    print("4 - Vysoká (256 kbps)")
    print("5 - Nejvyšší (320 kbps)")

    choice = input("\n: ")
    try:
        int_choice = int(choice)
    except:
        print("Výber musí být číslo od 1 do 5.")
        download(link)
        return

    if int_choice not in kvality:
        print("Neplatná volba. Vyber číslo 1-5.")
        download(link)
        return
    
    try:
        with yt_dlp.YoutubeDL(getYdlStuff(kvality[int_choice])) as ydl:
            ydl.download([link])
    except Exception as e:
        print(f"Něco se pokazilo. ({e})")

    cls()
    print(f"Video staženo do: {slozka}")
    input("\nZmackni CTRL + C pro ukoncení nebo ENTER pro pokračování...")
    main()

checkFfmpeg()
main()