# Projekt 3 - Volební scraper (2017)

Tento skript slouží k automatickému stažení výsledků parlamentních voleb z roku 2017 ze stránek `volby.cz` pro vybraný okres. Stažená data program uloží do přehledného CSV souboru.

## Autor
Filip Jankovský

## Instalace a spuštění
1. Než program poprvé spustí, je potřeba nainstalovat knihovny třetích stran ze souboru `requirements.txt`. V terminálu:
pip install -r requirements.txt
2. Program se spouští z příkazové řádky a vyžaduje přesně 2 argumenty:
- Odkaz na konkrétní územní celek (okres) z webu volby.cz
- Název výstupního souboru, do kterého se data uloží

Ukázka spuštění pro okres Přerov:
```bash
python projekt_3.py "[https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7104](https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7104)" "vysledky_prerov.csv"