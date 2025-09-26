# Python-projekt-3---Elections-Scraper
# Třetí projekt – Engeto Online Python Akademie

## Autor
- **Jméno:** Jan Koppan  
- **E-mail:** jan.koppan@seznam.cz  

---

## Popis projektu
Skript stahuje volební výsledky z roku 2017 pro vybraný okres (územní celek) a ukládá je do CSV souboru.  
Výstupní soubor obsahuje:  
1. kód obce  
2. název obce  
3. počet voličů v seznamu  
4. počet vydaných obálek  
5. počet platných hlasů  
6. hlasy pro jednotlivé kandidující strany (každá strana má vlastní sloupec)  

---

## Postup

1. Vytvoření virtuálního prostředí
```powershell
python -m venv venv

2. Aktivace virtuálního prostředí (Windows PowerShell)
venv\Scripts\Activate

3. Instalace závislostí
pip install -r requirements.txt

4. Spuštění programu
Program se spouští pomocí 2 argumentů:
odkaz na okres (URL ve formátu ps32?...)
název výstupního CSV souboru

Ukázka spuštění pro okres Česká Lípa:
Výsledky hlasování pro okres Česká Lípa
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=7&xnumnuts=5101" vysledky_ceska_lipa.csv

První argument: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=7&xnumnuts=5101
Druhý argument: vysledky_ceska_lipa.csv

Po spuštění se vytvoří soubor vysledky_ceska_lipa.csv ve stejné složce.


| code   | location   | registered | envelopes | valid | Občanská demokratická strana | Řád národa | ... |
| 561398 | Bezděz     | 299        | 169       | 169   | 24                           | 0          | ... |
| 561401 | Blatce     | 109        | 78        | 76    | 12                           | 0          | ... |
| 561410 | Blíževedly | 491        | 215       | 215   | 26                           | 0          | ... |

Použité knihovny

Soubor requirements.txt obsahuje seznam knihoven a jejich verzí:

beautifulsoup4==4.13.5
certifi==2025.8.3
charset-normalizer==3.4.3
idna==3.10
numpy==2.3.3
pandas==2.3.2
python-dateutil==2.9.0.post0
pytz==2025.2
requests==2.32.5
six==1.17.0
soupsieve==2.8
typing_extensions==4.15.0
tzdata==2025.2
urllib3==2.5.0
