from io import BytesIO
import discord
from PIL import Image, ImageDraw, ImageFont

class ImageClient:

    def __init__(self, bot):
        self.bot = bot
        self.robotURL = "https://robohash.org/"

    async def getAvatar(self, user, size=128):
        """Fetch the avatar of a user."""

        avatar_url = user.avatar_url_as(static_format="png", format="png", size=size)
        async with self.bot.session.get(avatar_url) as resp:
            imageBytes = await resp.read()
        return imageBytes

    async def getRobotImage(self, text, setNumber):
        """Fetch the robot image from robohash.org"""
        compoundURL = f"{self.robotURL}{text}.png"
        async with self.bot.session.get(compoundURL, params={"ignoreext": "false", "set": f"set{setNumber}"}) as resp:
            image = await resp.read()
        return BytesIO(image)

    def beautify(self, avatar_bytes):
        with Image.open("Assets/Images/plate_beautiful.png") as plate:
            with Image.open(BytesIO(avatar_bytes)) as avatar:
                with Image.new("RGB", (497, 559)) as canvas:
                    canvas.paste(avatar, (335, 35), mask=avatar)
                    canvas.paste(avatar, (337, 315), mask=avatar)
                    canvas.paste(plate, (0, 0), mask=plate)
                    buffer = BytesIO()
                    canvas.save(buffer, "PNG")
        buffer.seek(0)
        return buffer

    def deletify(self, avatar_bytes, name):
        with Image.open("Assets/Images/plate_delet.png") as plate:
            with Image.open(BytesIO(avatar_bytes)) as avatar:
                with Image.new("RGB", (400, 201)) as canvas:
                    avatar = avatar.resize((69, 69))
                    canvas.paste(avatar, (50, 80), mask=avatar)
                    canvas.paste(plate, (0, 0), mask=plate)
                    font = ImageFont.truetype("Assets/Fonts/Raleway-Bold.ttf", 10)
                    canvasDraw = ImageDraw.Draw(canvas)
                    canvasDraw.text((215, 81), name, font=font, fill=(0, 0, 0))
                    del canvasDraw
                    buffer = BytesIO()
                    canvas.save(buffer, "PNG")
        buffer.seek(0)
        return buffer

    def welcomeImage(self, avatar_bytes, name, tag, guild):
        with Image.open("Assets/Images/plate_welcome.png") as plate:
            with Image.open(BytesIO(avatar_bytes)) as avatar:
                with Image.new("RGB", (1024, 450)) as canvas:
                    enjoyText = f"Enjoy here in \"{guild.name}\""
                    font = ImageFont.truetype("Assets/Fonts/Raleway-Bold.ttf", 48)
                    canvas.paste(plate, (0, 0))
                    bigsize = (avatar.size[0] * 3, avatar.size[1] * 3)
                    with Image.new("L", bigsize, 0) as mask:
                        draw = ImageDraw.Draw(mask)
                        draw.ellipse((0, 0) + bigsize, fill=255)
                        mask = mask.resize(avatar.size, Image.ANTIALIAS)
                        avatar.putalpha(mask)
                        canvas.paste(avatar, (58, 95), avatar)
                        canvasDraw = ImageDraw.Draw(canvas)
                        canvasDraw.text((360, 157), name, font=font, fill=(255, 255, 255, 255))
                        canvasDraw.text((400, 225), tag, font=font, fill=(255, 255, 255, 255))
                        font = ImageFont.truetype("Assets/Fonts/Raleway-Bold.ttf", 32)
                        canvasDraw.text((320, 350), enjoyText, font=font, fill=(255, 255, 255, 255))
                        font = ImageFont.truetype("Assets/Fonts/Raleway-Bold.ttf", 24)
                        canvasDraw.text((40, 375), f"- {guild.member_count}th Member", font=font, fill=(255, 255, 255, 255))
                        del canvasDraw
                        buffer = BytesIO()
                        canvas.save(buffer, "PNG")
        buffer.seek(0)
        return buffer
    
    def goodbyeImage(self, avatar_bytes, name, tag):
        with Image.open("Assets/Images/plate_goodbye.png") as plate:
            with Image.open(BytesIO(avatar_bytes)) as avatar:
                with Image.new("RGB", (1024, 450)) as canvas:
                    font = ImageFont.truetype("Assets/Fonts/Raleway-Bold.ttf", 48)
                    canvas.paste(plate, (0, 0))
                    bigsize = (avatar.size[0] * 3, avatar.size[1] * 3)
                    with Image.new("L", bigsize, 0) as mask:
                        draw = ImageDraw.Draw(mask)
                        draw.ellipse((0, 0) + bigsize, fill=255)
                        mask = mask.resize(avatar.size, Image.ANTIALIAS)
                        avatar.putalpha(mask)
                        canvas.paste(avatar, (58, 95), avatar)
                        canvasDraw = ImageDraw.Draw(canvas)
                        canvasDraw.text((360, 157), name, font=font, fill=(255, 255, 255, 255))
                        canvasDraw.text((400, 225), tag, font=font, fill=(255, 255, 255, 255))
                        del canvasDraw
                        buffer = BytesIO()
                        canvas.save(buffer, "PNG")
        buffer.seek(0)
        return buffer
