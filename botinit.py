import asqlite
import asyncio


async def initialize_tables():
    async with asqlite.connect("uc_transactions.db") as conn:
        async with conn.cursor() as cursor:

            await cursor.execute(
                """CREATE TABLE buy_orders (
                                    OrderID INTEGER PRIMARY KEY, 
                                    OrderTime DATETIME DEFAULT CURRENT_TIMESTAMP, 
                                    OrderAuthor INTEGER, 
                                    BuyingOrg TEXT, 
                                    BuyingItem TEXT, 
                                    BuyingQuantity INTEGER, 
                                    CompensationItem TEXT, 
                                    CompensationQuantity INTEGER);
                                    """
            )

            await cursor.execute(
                """CREATE TABLE sell_orders (
                                    OrderID INTEGER PRIMARY KEY,
                                    OrderTime DATETIME DEFAULT CURRENT_TIMESTAMP,
                                    OrderAuthor INTEGER,
                                    SellingOrg TEXT,
                                    SellingItem TEXT,
                                    SellingQuantity INTEGER,
                                    CompensationItem TEXT,
                                    CompensationQuantity INTEGER);
                                    """
            )

            await cursor.execute(
                """CREATE TABLE completed_orders (
                                    OrderID INTEGER PRIMARY KEY,
                                    OrderTime DATETIME DEFAULT CURRENT_TIMESTAMP,
                                    OrderAuthor INTEGER,
                                    SellingOrg TEXT,
                                    SellingItem TEXT,
                                    SellingQuantity INTEGER,
                                    BuyingOrg TEXT,
                                    CompensationItem TEXT,
                                    CompensationQuantity INTEGER)
                                    """
            )

            await conn.commit()


asyncio.run(initialize_tables())
