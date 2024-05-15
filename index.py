import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.firewalls.com/licensing/sonicwall-firewalls.html"
headers = {'User-Agent': 'Mozilla/5.0'}

prodotti = []

def estrai_dati_prodotto(prodotto_html):
    nome = prodotto_html.find('a', class_='product-item-link').text.strip() if prodotto_html.find('a', class_='product-item-link') else "Nome non disponibile"
    codice = prodotto_html.get('data-product-sku', 'Codice non disponibile')
    descrizione_div = prodotto_html.find('div', class_='product description')
    descrizione = descrizione_div.text.strip() if descrizione_div else "Descrizione non disponibile"
    prezzo = prodotto_html.find('span', class_='price').text.strip() if prodotto_html.find('span', class_='price') else "Prezzo non disponibile"
    img_tag = prodotto_html.find('img', class_='product-image-photo')
    link_foto = img_tag['src'] if img_tag else "Immagine non disponibile"
    disponibilita = "In Stock"

    return {
        'Codice': codice,
        'Nome': nome,
        'Descrizione': descrizione,
        'Prezzo': prezzo,
        'Link Foto': link_foto,
        'Disponibilità': disponibilita
    }

while True:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    prodotti_html = soup.find_all('li', class_='item product product-item')
    for prodotto_html in prodotti_html:
        prodotti.append(estrai_dati_prodotto(prodotto_html))
    next_page = soup.find('a', class_='action next')
    if next_page:
        url = next_page['href']
    else:
        break

with open('sonicwall_products.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Codice', 'Nome', 'Descrizione', 'Prezzo', 'Link Foto', 'Disponibilità']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for prodotto in prodotti:
        writer.writerow(prodotto)

print("Dati salvati in sonicwall_products.csv")
