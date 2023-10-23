import requests
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
import discord
import json
import time
from datetime import datetime


with open('data.json') as file:
   # reading the json file
   data = json.load(file)

alert_price = data["alert_price"]
api_url = data["eth_price_api"]
wait_time = data["wait_time_in_seconds_after_success"]
time_after_no_result = data["wait_time_in_seconds_after_fail"]
log_file_path = data["log_file_path"]
bot_token = data["discord_bot_token"]

def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"{timestamp} - {message}\n"
    with open(log_file_path, "a") as log_file:
        log_file.write(log_message)

def discord_hook(eth_rate, currency):
    # discord webhook setup
    webhook = DiscordWebhook(url=data["discord_hook_url"])
    embed = DiscordEmbed(title='ETH Price Alert :loudspeaker:', color='17bf44')
    embed.set_thumbnail(url = data["image"])
    embed.set_footer(text= "ETH Price Monitoring by Picooo")
    embed.set_timestamp()
    embed.add_embed_field(name='Current Ethereum Price', value=f'{eth_rate} {currency}')
    embed.add_embed_field(name='Your Alert', value=f'{alert_price} {currency}')
    embed.add_embed_field(name='Absolute Savings', value=f'{round(float(difference),2)} {currency}')
    embed.add_embed_field(name='Relative Savings', value=f'{round(float(percentage_saving),2)} {"%"}')
    webhook.add_embed(embed)
    response = webhook.execute()

while True:
    response = requests.get(api_url, headers={"Accept": "application/json"})
    output = response.json()
    EUR = output['EUR']
    eth_rate_eur = float(EUR)
    currency = 'EUR'  # You can replace this with the currency you want to display
    difference = alert_price - eth_rate_eur
    percentage_saving = (difference / alert_price) * 100


    if eth_rate_eur < alert_price:
        try:
            discord_hook(eth_rate_eur, currency)
            log(message="ETH Price Alert happened. Script will sleep for " + str(wait_time) + " seconds")
            time.sleep(wait_time)
        except:
            log(message="An error occurred. Please check")
    else:
        log(message="No ETH Price Alert happened. Script will wait for " + str(time_after_no_result) + " seconds before it starts monitoring again.")
        time.sleep(time_after_no_result)



