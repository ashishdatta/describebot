from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv
import os
import replicate
from PIL import Image
from io import BytesIO
import requests


load_dotenv()

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    description="Describebot!",
    intents=intents,
)


@bot.command(aliases=["sd"])
async def stable_diffusion(ctx, *, prompt):
    """Generate an image from a text prompt using the stable-diffusion model"""
    msg = await ctx.send(f"“{prompt}”\n> Generating...")

    model = replicate.models.get("stability-ai/stable-diffusion")
    version = model.versions.get("db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf")
    image = version.predict(prompt=prompt)[0]

    await msg.edit(content=f"“{prompt}”\n{image}")


def describe(image):
    #msg = await ctx.send(f">Generating...")
    output = replicate.run(
        "yorickvp/llava-13b:6bc1c7bb0d2a34e413301fee8f7cc728d2d4e75bfab186aa995f63292bda92fc",
        input={"image": image,#open("./owen.png", "rb"),
            "prompt": "this is a picture of owen, describe to me what owen is doing and what is going on in this picture"}
    )
    res = ""
    for item in output:
        res += item
    return res

@bot.listen()
async def on_message(message):
    if 'describebot' not in message.channel.name: return
    if len(message.attachments) > 0:
         if "jpg" in message.attachments[0].filename or "png" in message.attachments[0].filename or "jpeg" in message.attachments[0].filename:
            res = requests.get(message.attachments[0].url)
            img = BytesIO(res.content)#Image.open(BytesIO(res.content)).convert("RGB")
            res = describe(img)
            await message.reply(res)



bot.run(os.environ["DISCORD_TOKEN"])