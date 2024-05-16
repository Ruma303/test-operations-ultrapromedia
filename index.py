import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.firewalls.com/licensing/sonicwall-firewalls.html"
headers = {'User-Agent': 'Mozilla/5.0'}

prodotti = []

def estrai_dati_prodotto(prodotto):
    nome = prodotto.find('a', class_='product-item-link').text.strip() if prodotto.find('a', class_='product-item-link') else "Nome non disponibile"
    codice = prodotto.find('span', style="font-size:inherit;").text.strip() if prodotto.find('span', style="font-size:inherit;") else "Codice non disponibile"

    descrizione_div = prodotto.find('div', class_='product-item-description')
    descrizione_items = descrizione_div.find_all('li') if descrizione_div else []
    descrizione = " | ".join([item.text.strip() for item in descrizione_items]) if descrizione_items else "Descrizione non disponibile"

    prezzo_tag = prodotto.find('span', class_='price')
    prezzo = prezzo_tag.text.strip() if prezzo_tag else "Prezzo non disponibile"

    img_tag = prodotto.find('img', class_='product-image-photo')
    link_foto = img_tag['src'] if img_tag else "Immagine non disponibile"

    disponibilita_tag = prodotto.find('p', class_='in-stock_add_cart')
    disponibilita = disponibilita_tag.text.strip() if disponibilita_tag else "Prodotto non disponibile"

    """ disponibilita_tag = prodotto.find('div', class_='availibility')
    if disponibilita_tag:
        p_tags = disponibilita_tag.find_all('p')
        disponibilita_texts = [p.text.strip() for p in p_tags]
        disponibilita = " | ".join(disponibilita_texts)
    else:
        disponibilita = "Disponibilità non disponibile" """

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
    prodotti_html = soup.find_all('div', class_='product-item-info')
    for prodotto in prodotti_html:
        prodotti.append(estrai_dati_prodotto(prodotto))
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