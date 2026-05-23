"webscraper.py"

import sys
import csv
import requests
from bs4 import BeautifulSoup

# 1. KONTROLA ARGUMENTŮ
# Program potřebuje přesně 2 argumenty: URL a název CSV souboru
if len(sys.argv) != 3:
    print("Chyba: Musíš zadat 2 argumenty (odkaz a název výstupního souboru)!")
    print('Příklad: python projekt_3.py "https://url_adresa" "vysledky.csv"')
    sys.exit()

url_hlavni = sys.argv[1]
soubor_vystup = sys.argv[2]

# Kontrola, zda odkaz vede na správný web volby.cz
if "volby.cz" not in url_hlavni:
    print("Chyba: První argument musí být platný odkaz z volby.cz!")
    sys.exit()

print(f"ZÍSKÁVÁM DATA Z URL: {url_hlavni}")

# Stažení hlavní stránky okresu
odpoved = requests.get(url_hlavni)
soup_hlavni = BeautifulSoup(odpoved.text, "html.parser")

# Tady budeme ukládat řádky s daty pro CSV
vsechny_obce_data = []
hlavicka_csv = ["code", "location", "registered", "envelopes", "valid"]
nactena_hlavicka = False

# Najdeme všechny řádky tabulky s obcemi
radky_obci = soup_hlavni.find_all("tr")

# 2. PROCHÁZENÍ VŠECH OBCÍ
for radek in radky_obci:
    # Hledáme políčko s kódem obce (obsahuje odkaz křížku "X" nebo číslo)
    td_kod = radek.find("td", class_="cislo")
    if td_kod is None:
        continue
        
    # Získáme kód obce a název obce
    kod_obce = td_kod.text.strip()
    nazev_obce = radek.find("td", class_="overflow_name").text.strip()
    
    # Najdeme odkaz na detail obce (schovává se pod křížkem nebo číslem)
    odkaz_tag = td_kod.find("a")
    if odkaz_tag is None:
        continue
        
    # Poskládáme celou URL adresu pro detail konkrétní obce
    url_obec = "https://volby.cz/pls/ps2017nss/" + odkaz_tag["href"]
    print(f"ZÍSKÁVÁM DATA Z URL: {url_obec}")
    
    # Stáhneme detail obce
    odpoved_obec = requests.get(url_obec)
    soup_obec = BeautifulSoup(odpoved_obec.text, "html.parser")
    
    # 3. SCRAPOVÁNÍ DAT O VOLIČÍCH
    volici = soup_obec.find("td", {"headers": "sa2"}).text.strip().replace("\xa0", "")
    obalky = soup_obec.find("td", {"headers": "sa3"}).text.strip().replace("\xa0", "")
    hlasy = soup_obec.find("td", {"headers": "sa6"}).text.strip().replace("\xa0", "")
    
    # Základní data obce
    radek_data = [kod_obce, nazev_obce, volici, obalky, hlasy]
    
    # 4. SCRAPOVÁNÍ HLASŮ PRO STRANY
    strany_hlasy = []
    
    # Projdeme tabulky s politickými stranami (jsou tam dvě vedle sebe)
    for t_num in ["t1sa2", "t2sa2"]:
        radky_stran = soup_obec.find_all("tr")
        for r_strana in radky_stran:
            td_nazev = r_strana.find("td", {"headers": t_num + "r1"})
            td_hlasy = r_strana.find("td", {"headers": t_num + "r2"})
            
            if td_nazev and td_hlasy:
                nazev_strany = td_nazev.text.strip()
                pocet_hlasu = td_hlasy.text.strip().replace("\xa0", "")
                
                # Pokud ještě nemáme názvy stran v hlavičce, přidáme je tam
                if not nactena_hlavicka:
                    hlavicka_csv.append(nazev_strany)
                    
                strany_hlasy.append(pocet_hlasu)
                
    nactena_hlavicka = True
    # Spojíme základní data s hlasy stran
    vsechny_obce_data.append(radek_data + strany_hlasy)

# 5. ZÁPIS DO CSV SOUBORU
print(f"UKLÁDÁM DATA DO SOUBORU: {soubor_vystup}")
with open(soubor_vystup, mode="w", newline="", encoding="utf-8") as f:
    pisar = csv.writer(f)
    pisar.writerow(hlavicka_csv)
    pisar.writerows(vsechny_obce_data)

print("DOKONČUJI: hotovo")