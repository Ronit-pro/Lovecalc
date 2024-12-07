import discord
from discord.ext import commands
import random
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='love', help='Check the love percentage between two users')
async def love(ctx, user1: discord.Member, user2: discord.Member):
    love_percentage = random.randint(0, 100)
    avatar1_url = user1.avatar_url
    avatar2_url = user2.avatar_url

    response1 = requests.get(avatar1_url)
    response2 = requests.get(avatar2_url)

    avatar1_img = Image.open(BytesIO(response1.content))
    avatar2_img = Image.open(BytesIO(response2.content))

    heart_img = Image.new('RGBA', (400, 200), (255, 255, 255, 0))
    fnt = ImageFont.truetype('arial.ttf', 40)
    d = ImageDraw.Draw(heart_img)
    d.text((150, 50), '❤️', font=fnt, fill=(255, 0, 0, 255))

    heart_img.paste(avatar1_img, (50, 50))
    heart_img.paste(avatar2_img, (200, 50))
    d.text((150, 100), f"{love_percentage}%", font=fnt, fill=(0, 0, 0, 255))

    img_path = f"love_{user1.id}_{user2.id}.png"
    heart_img.save(img_path)

    file = discord.File(fp=img_path, filename=img_path)
    await ctx.send(file=file)
    await ctx.send("Made with ❤️ by @ronit_in")

bot.run('MTI5NzI1NzY2NDQ4NDczNzAyNA.GFsjfE.9kemaJghRmIKC3oapHJqhE8J52qQva_4icx0bk')
