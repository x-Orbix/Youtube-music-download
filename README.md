# YouTube MP3 Downloader

Jednoduchý nástroj pro stahování audia z YouTube ve formátu MP3 přímo z příkazové řádky. Umožňuje vyhledat video podle názvu nebo vložit přímý odkaz, vybrat kvalitu MP3 a stáhnout ho do složky `Music/YTB` v domovském adresáři.

## Funkce

- Vyhledávání videí na YouTube podle názvu (přes `scrapetube`)
- Stahování a konverze do MP3 (přes `yt-dlp` + `ffmpeg`)
- Výběr kvality MP3 (128–320 kbps)
- Automatická kontrola a stažení `ffmpeg`, pokud chybí
- Progress bar během stahování

## Požadavky

- Python 3.12+
- Knihovny: `yt-dlp`, `scrapetube`, `certifi`

Instalace závislostí:
```bash
pip install -r requirements.txt
```

`ffmpeg` se stahuje automaticky při prvním spuštění, pokud není v systému nalezen.

## Použití

```bash
python main.py
```

Po spuštění zadej název videa nebo přímý YouTube odkaz, vyber video z výsledků vyhledávání (pokud jsi zadal název) a zvol požadovanou kvalitu MP3.
## Stažení
Je zde hotová `.exe` v [reales](https://github.com/x-Orbix/Youtube-music-download/releases)
## Sestavení do .exe (volitelné)

```bash
pip install pyinstaller certifi
python -c "import certifi; print(certifi.where())"
pyinstaller --onefile --add-data "CESTA_ZE_ZJISTENI_VYSE\certifi;certifi" main.py
```

Hotová `.exe` bude ve složce `dist/`.

## Upozornění

Tento nástroj je určen pouze pro osobní a vzdělávací účely. Stahování obsahu chráněného autorským právem bez souhlasu vlastníka může být v rozporu s podmínkami služby YouTube a/nebo s platnými zákony o autorském právu v tvé zemi.

**Používáním tohoto nástroje přebíráš plnou odpovědnost za způsob, jakým ho použiješ.** Autor tohoto projektu nenese žádnou odpovědnost za případné zneužití, škody nebo právní důsledky vzniklé v souvislosti s používáním tohoto softwaru.

## Licence

Tento projekt je poskytován "tak jak je" (as-is), bez jakékoli záruky.
