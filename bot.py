from playwright.sync_api import sync_playwright
import requests, os, re

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URLS = [
    "https://www.turismocity.com.ar/vuelos-baratos-region-Europa?currency=USD&flexDates=true&from=BUE&type=oneway",
    "https://www.turismocity.com.ar/vuelos-baratos-region-Europa?currency=USD&flexDates=true&from=COR&type=oneway"
]

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    prices = []

    for url in URLS:
        page.goto(url, timeout=60000)
        page.wait_for_timeout(8000)
        html = page.content()

        found = re.findall(r'USD\s?([\d,]+)', html)
        for f in found:
            price = int(f.replace(",", ""))
            if price <= 1500:
                prices.append(price)

    browser.close()

if prices:
    best = min(prices)
    send(f"✈️ VUELO BARATO A EUROPA\n💵 USD {best}\n🛫 Desde Argentina\n🌍 Fuente: Turismocity")
else:
    send("⚠️ Hoy no se encontraron vuelos a Europa por debajo de USD 1500.")
