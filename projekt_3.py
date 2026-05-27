""" 
projekt_3.py: třetí projekt - Volební scraper
author: (Filip Jankovský)
email: (janko09063@mot.sps-dopravni.cz)
"""

import sys
import csv
import requests
from bs4 import BeautifulSoup

def main():
    # 1. KONTROLA ARGUMENTŮ [cite: 88, 92]
    if len(sys.argv) != 3:
        print("CHYBA: Zadal jsi špatný počet argumentů!")
        print("Spusť to takto: python3 projekt_3.py <odkaz> <soubor.csv>")
        sys.exit()

    url_okresu = sys.argv[1]
    jmeno_souboru = sys.argv[2]
    
    print(f"ZÍSKÁVÁM DATA Z URL: {url_okresu}")

    # 2. STAŽENÍ HLAVNÍ STRÁNKY
    odpoved = requests.get(url_okresu)
    soup = BeautifulSoup(odpoved.text, "html.parser")

    vsechna_data = []
    # Zde připravujeme hlavičku přesně podle zadání (body 1 až 5) [cite: 113-118]
    hlavicka = ["Kód obce", "Název obce", "Voliči v seznamu", "Vydané obálky", "Platné hlasy"]
    mame_nazvy_stran = False

    # 3. PROCHÁZENÍ OBCÍ
    for radek in soup.find_all("tr"):
        td_kod = radek.find("td", class_="cislo")
        td_nazev = radek.find("td", class_="overflow_name")
        
        if td_kod is None or td_nazev is None:
            continue
            
        kod_obce = td_kod.text.strip()
        nazev_obce = td_nazev.text.strip()
        odkaz_element = td_kod.find("a")
        
        if odkaz_element is None:
            continue
            
        url_obce = "https://volby.cz/pls/ps2017nss/" + odkaz_element["href"]
        print(f"Stahuji obec: {nazev_obce}")
        
        # 4. STAŽENÍ DETAILU OBCE
        odpoved_obce = requests.get(url_obce)
        soup_obce = BeautifulSoup(odpoved_obce.text, "html.parser")
        
        # Získání dat (body 3, 4, 5 ze zadání) [cite: 116-118]
        volici = soup_obce.find("td", {"headers": "sa2"}).text.replace("\xa0", "")
        obalky = soup_obce.find("td", {"headers": "sa3"}).text.replace("\xa0", "")
        platne_hlasy = soup_obce.find("td", {"headers": "sa6"}).text.replace("\xa0", "")
        
        radek_obce_data = [kod_obce, nazev_obce, volici, obalky, platne_hlasy]
        
        # 5. ZÍSKÁNÍ HLASŮ PRO STRANY (bod 6 ze zadání) [cite: 119]
        for cislo_tabulky in ["t1", "t2"]:
            for radek_strany in soup_obce.find_all("tr"):
                td_jmeno_strany = radek_strany.find("td", {"headers": f"{cislo_tabulky}sa1 {cislo_tabulky}sb2"})
                td_pocet_hlasu = radek_strany.find("td", {"headers": f"{cislo_tabulky}sa2 {cislo_tabulky}sb3"})
                
                if td_jmeno_strany and td_pocet_hlasu:
                    jmeno = td_jmeno_strany.text.strip()
                    hlasy = td_pocet_hlasu.text.replace("\xa0", "")
                    
                    if not mame_nazvy_stran:
                        hlavicka.append(jmeno) # Přidá stranu do hlavičky tabulky
                    
                    radek_obce_data.append(hlasy)
                    
        mame_nazvy_stran = True
        vsechna_data.append(radek_obce_data)

    # 6. ULOŽENÍ DO PŘEHLEDNÉHO CSV
    print(f"UKLÁDÁM DATA DO SOUBORU: {jmeno_souboru}")
    # Výchozí CSV formát oddělený čárkou, přesně jak vyžaduje ukázka v zadání
    with open(jmeno_souboru, mode="w", newline="", encoding="utf-8-sig") as soubor:
        zapisovac = csv.writer(soubor, delimiter=",")
        zapisovac.writerow(hlavicka)
        zapisovac.writerows(vsechna_data)

    print("DOKONČUJI: hotovo")

if __name__ == "__main__":
    main()