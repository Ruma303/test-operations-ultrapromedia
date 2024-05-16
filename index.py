import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.firewalls.com/licensing/sonicwall-firewalls.html"
headers = {'User-Agent': 'Mozilla/5.0'}

prodotti = []

def estrai_dati_prodotto(prodotto_html):
    nome = prodotto_html.find('a', class_='product-item-link').text.strip() if prodotto_html.find('a', class_='product-item-link') else "Nome non disponibile"
    codice = prodotto_html.find('span', style="font-size:inherit;").text.strip() if prodotto_html.find('span', style="font-size:inherit;") else "Codice non disponibile"

    descrizione_div = prodotto_html.find('div', class_='product-item-description')
    descrizione_items = descrizione_div.find_all('li') if descrizione_div else []
    descrizione = " | ".join([item.text.strip() for item in descrizione_items]) if descrizione_items else "Descrizione non disponibile"

    prezzo = "Informazione non disponibile"  # Se il prezzo non è disponibile nel tuo HTML di esempio
    img_tag = prodotto_html.find('img', class_='product-image-photo')
    link_foto = img_tag['src'] if img_tag else "Immagine non disponibile"
    disponibilita = prodotto_html.find('span', class_='virtual-product-delivery').text.strip() if prodotto_html.find('span', class_='virtual-product-delivery') else "Disponibilità non disponibile"

    return {
        'Codice': codice,
        'Nome': nome,
        'Descrizione': descrizione,
        'Prezzo': prezzo,
        'Link Foto': link_foto,
        'Disponibilità': disponibilita
    }

def scrape_page(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    prodotti_html = soup.find_all('div', class_='product details product-item-details')
    for prodotto_html in prodotti_html:
        prodotti.append(estrai_dati_prodotto(prodotto_html))
    next_page = soup.find('a', class_='action next')
    if next_page and 'href' in next_page.attrs:
        scrape_page(next_page['href'])

scrape_page(url)

with open('sonicwall_products.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Codice', 'Nome', 'Descrizione', 'Prezzo', 'Link Foto', 'Disponibilità']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for prodotto in prodotti:
        writer.writerow(prodotto)

print("Dati salvati in sonicwall_products.csv")