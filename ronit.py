import discord
from discord.ext import commands
import random
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', case_insensitive=True, intents=intents)

@bot.event
async def on_ready():
    print(f"Loaded {bot.user}")
    await bot.change_presence(activity=discord.CustomActivity(name="❤️‍🩹 Kooding"))

@bot.group()
async def love(ctx: commands.Context):
    if not ctx.invoked_subcommand:
        await ctx.reply("`.love check <user1> <user2>`", mention_author=False)

@love.command(name='check')
async def love_check(ctx: commands.Context, user1: discord.Member, user2: discord.Member):
    love_percentage = random.randint(0, 100)

    url1 = str(user1.avatar.url if user1.avatar else user1.default_avatar.url)
    url2 = str(user2.avatar.url if user2.avatar else user2.default_avatar.url)

    response1 = requests.get(url1)
    response2 = requests.get(url2)

    img1 = Image.open(BytesIO(response1.content))
    img2 = Image.open(BytesIO(response2.content))

    img1 = img1.resize((100, 100))
    img2 = img2.resize((100, 100))

    mask1 = Image.new('L', (100, 100), 0)
    mask2 = Image.new('L', (100, 100), 0)
    draw1 = ImageDraw.Draw(mask1)
    draw2 = ImageDraw.Draw(mask2)
    draw1.ellipse((0, 0, 100, 100), fill=255)
    draw2.ellipse((0, 0, 100, 100), fill=255)

    img1.putalpha(mask1)
    img2.putalpha(mask2)

    new_img = Image.new('RGBA', (250, 100), (255, 255, 255, 0))
    new_img.paste(img1, (0, 0), mask1)
    new_img.paste(img2, (150, 0), mask2)

    heart = "❤️" if love_percentage > 30 else "💔"

    font_path = "C:\\Windows\\Fonts\\seguiemj.ttf"
    fnt = ImageFont.truetype(font_path, 32)
    d = ImageDraw.Draw(new_img)
    d.text((105, 35), heart, font=fnt, fill=(255, 0, 0, 255))

    with BytesIO() as image_binary:
        new_img.save(image_binary, 'PNG')
        image_binary.seek(0)

        embed = discord.Embed(
            description=f"## ❤️‍🩹 **{love_percentage}%** love detected!",
            color=colour
        )
        embed.set_author(name=f"Love Calculator", icon_url=bot.user.avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author}  |  Virtual love calculator", icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        embed.set_image(url="attachment://love.png")

        await ctx.reply(
            embed=embed,
            file=discord.File(image_binary, 'love.png'),
            mention_author=False
        )

colour=0x302c34
bot.run("MTI5NzI1NzY2NDQ4NDczNzAyNA.GFsjfE.9kemaJghRmIKC3oapHJqhE8J52qQva_4icx0bk")
