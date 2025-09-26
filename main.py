"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Jan Koppan
email: jan.koppan@seznam.cz
popis: Skript stahuje volební výsledky z roku 2017 pro vybraný okres (územní celek)
       a ukládá je do CSV souboru. Výstup obsahuje seznam obcí, počty voličů,
       vydané obálky, platné hlasy a hlasy pro všechny kandidující strany.
"""

import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd


BASE = "https://www.volby.cz/pls/ps2017nss/"


def fetch_html(url: str) -> BeautifulSoup:
    """Stáhne HTML stránku a vrátí BeautifulSoup objekt."""
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Chyba při načítání URL: {e}")
        sys.exit(1)
    return BeautifulSoup(r.text, "html.parser")


def get_obec_links(soup: BeautifulSoup) -> dict:
    """
    Najde odkazy na stránky obcí (ps33?xobec=...).
    Klíčem je kód obce (číslo ve sloupci 'číslo'), hodnotou je plná URL.
    """
    links = {}
    for a in soup.find_all("a"):
        href = a.get("href")
        if href and "xobec=" in href:          # odkaz vede na stránku obce
            code_text = a.text.strip()          # v tabulce je zobrazen kód obce
            links[code_text] = BASE + href
    return links


def parse_obec(soup: BeautifulSoup, code: str) -> dict:
    """Vyparsuje výsledky jedné obce do dictu."""
    tables = soup.find_all("table")

    # Najdi správné <h3> - pouze ten, který začíná na "Obec:"
    name = "Neznámá obec"
    for h3 in soup.find_all("h3"):
        txt = h3.get_text(strip=True)
        if txt.startswith("Obec:"):
            name = txt.split(":", 1)[1].strip()
            break

    # Základní údaje z první tabulky
    t0_cells = tables[0].find_all("td")
    registered = t0_cells[3].get_text(strip=True).replace("\xa0", "")
    envelopes  = t0_cells[4].get_text(strip=True).replace("\xa0", "")
    valid      = t0_cells[7].get_text(strip=True).replace("\xa0", "")

    # Hlasy pro strany – v následujících tabulkách (může jich být víc)
    results = {}
    for table in tables[1:]:
        rows = table.find_all("tr")[2:]  # přeskočit hlavičky
        for row in rows:
            tds = row.find_all("td")
            if len(tds) >= 3:
                party = tds[1].get_text(strip=True)
                votes = tds[2].get_text(strip=True).replace("\xa0", "")
                if party:  # ignoruj prázdné řádky
                    results[party] = votes

    return {
        "code": code,
        "location": name,   # teď už tam bude správně jméno obce
        "registered": registered,
        "envelopes": envelopes,
        "valid": valid,
        **results
    }


def main():
    # Kontrola argumentů
    if len(sys.argv) != 3:
        print("Použití: python main.py <URL_okresu_ps32> <vystupni_soubor.csv>")
        sys.exit(1)

    url = sys.argv[1].strip('"').strip("'")
    output_file = sys.argv[2]

    if not url.startswith(BASE + "ps32"):
        print("❌ Neplatný odkaz. Očekávám URL na okres (ps32).")
        sys.exit(1)

    # Stažení seznamu obcí
    soup_okres = fetch_html(url)
    obce = get_obec_links(soup_okres)
    if not obce:
        print("❌ Na stránce okresu se nepodařilo najít žádné obce.")
        sys.exit(1)

    print(f"➡️ Nalezeno {len(obce)} obcí. Stahuji výsledky...")

    data = []
    for code, href in obce.items():
        soup_obec = fetch_html(href)
        data.append(parse_obec(soup_obec, code))

    # Export pro český Excel: oddělovač středník
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False, sep=";", encoding="utf-8-sig")
    print(f"✅ Hotovo! Data uložena do {output_file}")


if __name__ == "__main__":
    main()

