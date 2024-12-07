@client.group()
async def love(ctx: commands.Context):
    if not ctx.invoked_subcommand:
        await ctx.reply("```js\n.love check <user1> <user2>```", mention_author=False)

@love.command(name='check')
async def love_check(ctx: commands.Context, user1: discord.Member, user2: discord.Member):
    love_percentage = random.randint(0, 100)

    url1 = str(user1.avatar.url if user1.avatar else user1.default_avatar.url)
    url2 = str(user2.avatar.url if user2.avatar else user2.default_avatar.url)

    response1 = requests.get(url1)
    response2 = requests.get(url2)

    img1 = Image.open(BytesIO(response1.content)).resize((100, 100))
    img2 = Image.open(BytesIO(response2.content)).resize((100, 100))

    mask = Image.new('L', (100, 100), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 100, 100), fill=255)

    img1.putalpha(mask)
    img2.putalpha(mask)

    new_img = Image.new('RGBA', (250, 100), (255, 255, 255, 0))
    new_img.paste(img1, (0, 0), mask)
    new_img.paste(img2, (150, 0), mask)

    heart = "❤️" if love_percentage > 30 else "💔"

    try:
        font_path = "C:\\Windows\\Fonts\\seguiemj.ttf"
        fnt = ImageFont.truetype(font_path, 32)
    except OSError:
        fnt = ImageFont.load_default()

    d = ImageDraw.Draw(new_img)
    d.text((105, 35), heart, font=fnt, fill=(255, 0, 0, 255))

    with BytesIO() as image_binary:
        new_img.save(image_binary, 'PNG')
        image_binary.seek(0)

        embed = discord.Embed(
            description=f"## <:love:1210833297979211796> **{love_percentage}%** love detected!",
            color=colour
        )
        embed.set_author(
            name="Love Calculator", 
            icon_url=client.user.avatar.url if client.user.avatar else client.user.default_avatar.url
        )
        embed.set_footer(
            text=f"Requested by {ctx.author}  |  Virtual love calculator", 
            icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
        )
        embed.set_image(url="attachment://love.png")

        await ctx.reply(
            embed=embed,
            file=discord.File(image_binary, 'love.png'),
            mention_author=False
        )

colour=0x302c34
client.run("MTE4NTk4Mjc2MTY4OTk0NDEwNQ.GPYnJi.u-sqy4d8OJFz9OPw4B0jBecBlH5RF170p5qxSQ")
