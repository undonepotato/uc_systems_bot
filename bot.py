import os
import discord
import random
import asqlite
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot_version = "0.0.1"
intents = discord.Intents().all()
bot = commands.Bot(command_prefix=".", intents=intents)

dbconnect=asqlite.connect("uc_db")
dbcursor=dbconnect.cursor()

class NegotiationButton(discord.ui.View):
    @discord.ui.button(label="Open Channel", style=discord.ButtonStyle.primary)
    async def negotiate(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        ntcnameverify = True

        while ntcnameverify:
            newchannelname = f"trade-{random.randint(0,99999)}"
            for channel in bot.get_guild(824481238219620372).channels:
                if newchannelname == channel.name:
                    continue
                else:
                    ntcnameverify = False

        created_channel = await bot.get_guild(824481238219620372).create_text_channel(
            name=newchannelname,
            overwrites={  # TODO Change these IDs
                interaction.user: discord.PermissionOverwrite(
                    read_messages=True, send_messages=True
                )
            },
            category=bot.get_channel(1000099256998297681),
            position=500,
        )

        await interaction.response.send_message(
            f"Channel opened! {created_channel.mention}", ephemeral=True
        )

class TradeSendConfirmationButton(discord.ui.View):
    @discord.ui.button(label="Confirm and Send", style=discord.ButtonStyle.success)
    async def TradeSendConfirmation(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

@bot.command(name="buyoffer", help="Adds a buy offer to the channel and spreadsheet.")
async def buyoffer(
ctx,
item_to_buy,
buying_quantity,
item_to_pay,
payment_quantity,
org="",
additional_info="",
):

    embed_title = f"{org} Buy Offer"

    if org == "":
        org = ctx.author

    buyembed = discord.Embed(
        color=0x3498DB,
        title=embed_title,
        type="rich",
        description=f"""
        {org} is buying **{buying_quantity} {item_to_buy} for {payment_quantity} {item_to_pay}**.
        To claim this offer, press the button below to open a negotiation channel.
        
        """,
        timestamp=datetime.utcnow(),
    )

    buyembed.set_author(name=ctx.author)
    buyembed.set_thumbnail(url="https://i.imgur.com/DnKcqBt.png")
    buyembed.set_footer(text="Times are in UTC.")
    if additional_info != "":
        buyembed.add_field(
            name="Additional Info", value=additional_info, inline=True
        )  # makes the embed

    if len(buyembed) < 6000:
        await bot.get_channel(876620293249048666).send(
            embed=buyembed, view=NegotiationButton()
        )  # TODO Change channel ID
    else:
        await ctx.send(
            "Your embed is too long! The maximum limit is 6000 characters.",
            ephemeral=True,
        )


@bot.command(name="selloffer", help="Adds a sell offer to the channel and spreadsheet.")
async def selloffer(
    ctx,
    item_to_sell,
    selling_quantity,
    item_to_get,
    compensation_quantity,
    org="",
    additional_info="",
):

    embed_title = f"{org} Sell Offer"

    if org == "":
        org = ctx.author

    sellembed = discord.Embed(
        color=0x3498DB,
        title=embed_title,
        type="rich",
        description=f"""
        {org} is selling **{selling_quantity} {item_to_sell} for {compensation_quantity} {item_to_get}**.
        To claim this offer, press the button below to open a negotiation channel.
        
        """,
        timestamp=datetime.utcnow(),
    )

    sellembed.set_author(name=ctx.author)
    sellembed.set_thumbnail(url="https://i.imgur.com/DnKcqBt.png")
    sellembed.set_footer(text="Times are in UTC.")
    if additional_info != "":
        sellembed.add_field(
            name="Additional Info", value=additional_info, inline=True
        )  # makes the embed

    if len(sellembed) < 6000:
        await bot.get_channel(876620293249048666).send(
            embed=sellembed, view=NegotiationButton()
        )  # TODO Change channel ID
    else:
        await ctx.send(
            "Your embed is too long! The maximum limit is 6000 characters.",
            ephemeral=True,
        )


@bot.command(
    name="tradecomplete", help="Completes a trade, with all the information needed."
)
async def tradecomplete(
    ctx,
    selling_org,
    buying_org,
    selling_item,
    selling_quantity,
    compensation_item,
    compensation_quantity,
    delivery_method="ucl" or "selling" or "buying" or "both",
    secure_deliver=True,
):

    if delivery_method == "ucl":
        display_delivery_method = "UC Logistics Delivering"

    elif delivery_method == "buying":
        display_delivery_method = "Buying Party Delivering"

    elif delivery_method == "selling":
        display_delivery_method = "Selling Party Delivering"

    elif delivery_method == "both":
        display_delivery_method = "Both Parties Delivering"

    tradecompleteembed = discord.Embed(
        color=discord.Color.blurple(),
        title="Confirm Complete Trade",
        type="rich",
        description=f"""
    Selling Organization: {selling_org}
    Buying Organization: {buying_org}
    Selling Item: {selling_item.title()}
    Quantity Sold: {selling_quantity.title()}
    Compensation Item: {compensation_item.title()}
    Compensation Quantity: {compensation_quantity.title()}
    Delivery Method: {display_delivery_method}
    Secure Delivery: {secure_deliver}
    """,
        timestamp=datetime.utcnow(),
    )

    tradecompleteembed.set_author(name=ctx.author)
    tradecompleteembed.set_thumbnail(url="https://i.imgur.com/DnKcqBt.png")
    tradecompleteembed.set_footer(text="Times are in UTC.")

    if len(tradecompleteembed) < 6000:
        await bot.get_channel(876620293249048666).send(
            embed=tradecompleteembed
        )  # TODO Change channel ID
    else:
        await ctx.send(
            "Your embed is too long! The maximum limit is 6000 characters.",
            ephemeral=True,
        )


@bot.command(name="version", help="Returns version info.")
async def version(ctx):
    await ctx.send(f"Bot version {bot_version}, discord.py {discord.__version__}")


bot.run(TOKEN)
