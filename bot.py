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

bot_version = "0.1.0"
intents = discord.Intents().all()


class Bot(commands.Bot):
    async def setup_hook(self):
        global conn, cursor
        conn = await asqlite.connect("uc_transactions.db")
        cursor = await conn.cursor()

bot = Bot(command_prefix=".", intents=intents)

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
            name = newchannelname,
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

class UCLButton(discord.ui.View):
    @discord.ui.button(label="Available", style=discord.ButtonStyle.success)
    async def ucl_take(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.style = discord.ButtonStyle.gray
        button.disabled = True
        button.label = "Taken"
        await interaction.response.edit_message(view=self)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send(f"Command threw an error; BadArgument. Make sure the `quantity` argument is always a number, and that the others are also appropriate.\n ```{error}```")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"```{error}```")
    if isinstance(error, commands.CommandNotFound):
        pass

@bot.command(name="buyoffer", help="Adds a buy offer to the channel and spreadsheet.")
async def buyoffer(
    ctx,
    item_to_buy: str,
    buying_quantity: int,
    item_to_pay: str,
    payment_quantity: int,
    org="",
    additional_info="",
):

    if org == "":
        org = ctx.author

    await cursor.execute(  # Insert into transactions database
        """INSERT INTO buy_orders (
            OrderAuthor,
            BuyingOrg,
            BuyingItem,
            BuyingQuantity,
            CompensationItem,
            CompensationQuantity
            )
            VALUES
            (?,?,?,?,?,?)
            """,
            (ctx.author.id,
            org,
            item_to_buy,
            buying_quantity,
            item_to_pay,
            payment_quantity))

    await conn.commit()  # Commit insert

    embed_title = f"{org} Buy Offer"

    buyembed = discord.Embed(  # Makes the embed to be sent in buy-offers
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


@bot.command(
    name="selloffer",
    help="Adds a sell offer to the channel and spreadsheet.",
)
async def selloffer(
    ctx,
    item_to_sell,
    selling_quantity,
    item_to_get,
    compensation_quantity,
    org="",
    additional_info="",
):

    if org == "":
        org = ctx.author

    embed_title = f"{org} Sell Offer"

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
    name="tradecomplete",
    help="Completes a trade, with all the information needed.",
)
async def tradecomplete(
    ctx,
    selling_org: str,
    buying_org: str,
    selling_item: str,
    selling_quantity: int,
    compensation_item: str,
    compensation_quantity: int,
    delivery_method="market" or "selling" or "buying" or "ucl" or "both",
    secure_deliver=True,
):  
    if delivery_method == "ucl":
        display_delivery_method = "UC Logistics Delivering"
        ucl_embed = discord.Embed(color = discord.Color.brand_green(), title="UCL Order", type="rich", description=f"""
        Transporting {selling_quantity} {selling_item} and {compensation_quantity} {compensation_item} between {selling_org} and {buying_org}.
        Secure Delivery: {secure_deliver}
        Press the button below to claim this order.
        """)
        await bot.get_channel(876620293249048666).send(embed=ucl_embed, view=UCLButton())

    elif delivery_method == "buying":
        display_delivery_method = "Buying Party Delivering"

    elif delivery_method == "selling":
        display_delivery_method = "Selling Party Delivering"

    elif delivery_method == "market":
        display_delivery_method = "Exchange Items at Market"

    elif delivery_method == "both":
        display_delivery_method = "Both Parties Deliver"

    else:
        await ctx.send("Command threw an error; BadArgument. Make sure the `quantity` argument is always a number, and that the others are also appropriate.\n ```delivery_method argument must be 'market', 'selling', 'buying', 'both', or 'ucl'.```")
        return

    await cursor.execute(  # Insert into transactions database
        """INSERT INTO completed_orders (
            OrderAuthor,
            SellingOrg,
            SellingItem,
            SellingQuantity,
            BuyingOrg,
            CompensationItem,
            CompensationQuantity
            )
            VALUES
            (?,?,?,?,?,?,?)
            """,
            (ctx.author.id,
            selling_org,
            selling_item,
            selling_quantity,
            buying_org,
            compensation_item,
            compensation_quantity))

    await conn.commit()  # Commit insert

    tradecompleteembed = discord.Embed(
        color=discord.Color.green(),
        title="Trade Success",
        type="rich",
        description=f"""
    Selling Organization: {selling_org}
    Buying Organization: {buying_org}
    Selling Item: {selling_item.title()}
    Quantity Sold: {selling_quantity}
    Compensation Item: {compensation_item.title()}
    Compensation Quantity: {compensation_quantity}
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
            "Embed character limit exceeded. Trade has successfully gone through.",
            ephemeral=True,
        )


@bot.command(name="version", help="Returns version info.")
async def version(ctx):
    await ctx.send(f"Bot version {bot_version}, discord.py {discord.__version__}")


bot.run(TOKEN)
