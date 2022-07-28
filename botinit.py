import asqlite

dbconnect=asqlite.connect("uc_db")
dbcursor=dbconnect.cursor()

async def initialize_tables():
    await dbcursor.execute("""CREATE TABLE buy_orders
                        OrderID int NOT NULL AUTO_INCREMENT,
                        OrderTime timestamp DEFAULT GETDATE(),
                        OrderAuthor text,
                        BuyingOrg text,
                        BuyingItem text,
                        BuyingQuantity int,
                        CompensationItem text,
                        CompensationQuantity int
                        """)

    await dbcursor.execute("""CREATE TABLE sell_orders
                        OrderID int NOT NULL AUTO_INCREMENT,
                        OrderTime timestamp DEFAULT GETDATE(),
                        OrderAuthor text,
                        SellingOrg text,
                        SellingItem text,
                        SellingQuantity int,
                        CompensationItem text,
                        CompensationQuantity int
                        """)

    await dbcursor.execute("""CREATE TABLE completed_orders
                        OrderID int NOT NULL AUTO_INCREMENT,
                        OrderTime timestamp DEFAULT GETDATE(),
                        OrderAuthor text,
                        SellingOrg text,
                        SellingItem text,
                        SellingQuantity int,
                        BuyingOrg text,
                        CompensationItem text,
                        CompensationQuantity int
                        """)

    await dbconnect.commit()
