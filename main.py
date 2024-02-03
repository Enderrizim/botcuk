import discord
from discord.ext import commands
import datetime
import psutil
from flask import Flask
from threading import Thread
import os

app = Flask('')

@app.route('/')
def main():
    return "Your bot is alive!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

startup_time = datetime.datetime.utcnow()

@bot.event
async def on_ready():
    print(f'{bot.user} is ready to roll!')
    keep_alive()

@bot.command()
async def uptime(ctx):
    now = datetime.datetime.utcnow()
    uptime_delta = now - startup_time

    # Gün, saat, dakika ve saniye olarak ayrıştırma
    days, hours, minutes, seconds = uptime_delta.days, uptime_delta.seconds // 3600, (uptime_delta.seconds // 60) % 60, uptime_delta.seconds % 60

    # Sistem bilgilerini al
    cpu_usage = psutil.cpu_percent()
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    uptime_message = (
        f'Bot is up for: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds.\n'
        f'CPU Usage: {cpu_usage}%\n'
        f'RAM Usage: {ram.percent}% ({round(ram.used / (1024**3), 2)} GB used / {round(ram.total / (1024**3), 2)} GB total)\n'
        f'Disk Usage: {disk.percent}% ({round(disk.used / (1024**3), 2)} GB used / {round(disk.total / (1024**3), 2)} GB total)'
    )

    await ctx.send(uptime_message)


bot.run(os.environ.get('TOKEN'))
