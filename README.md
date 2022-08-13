# uc_systems_bot
The repository for the Discord bot of Unified Commerce.

# Commands
Command Prefix: "." (Period)

***__MAKE SURE TO PUT QUOTES IN MULTIWORD ARGUMENTS, FOR EXAMPLE:__***

![undonecarrot doing .buyoffer "Pumpkin Pie" (in quotes) 16 Diamond 1 UC](https://user-images.githubusercontent.com/79398813/184498591-8bfc8338-20b8-4f53-b581-61f6e31c9bba.png)

***__DO NOT DO:__***

![undonecarrot doing .buyoffer Pumpkin Pie (not in quotes) 16 Diamond 1 UC](https://user-images.githubusercontent.com/79398813/184498682-bc7eba0e-5029-4945-956e-938bdc3ed3cf.png)




## `.help`
Syntax: `.help [command]`

.help without any arguments returns a code block with all the commands and their uses. Pass a specific command to see more detailed information about it.
![.help returning a menu with all the commands](https://user-images.githubusercontent.com/79398813/184497884-e813038b-91a8-45dc-aff7-fa0dc69c965a.png)
![.help tradecomplete returning syntax information about the tradecomplete command](https://user-images.githubusercontent.com/79398813/184497924-3f3679bd-fb15-4dc2-bd4c-43678ffdfc15.png)

### Use Cases
Finding all commands and their syntax.

## `.version`
Syntax: `.version`

No arguments taken. Returns the bot version, the `discord.py` library version, and the git branch that it's using. Mostly for debugging.
![.version returning "Bot version 0.1.7, discord.py 2.0.0a. Main branch."](https://user-images.githubusercontent.com/79398813/184498116-5c7c3a13-ca7e-43ea-921c-ff87d564501d.png)

### Use Cases
Mostly just debugging.

## `.buyoffer`
Syntax: `.buyoffer <item_to_buy> <buying_quantity> <item_to_pay> <payment_quantity> <org> [additional_info]`

Posts a buy offer in #buy-offers and adds one to the database.

`item_to_buy`: The item you're offering to buy

`buying_quantity`: The amount of the item you want to buy. Whole numbers only, no letters.

`item_to_pay`: The item you're paying in

`payment_quantity`: The amount of payment you're giving. Whole numbers only, no letters.

`org`: The organization you're posting this order for. If it's a personal trade, just put your own username.

`additional_info`: An optional field if you want to put additional information, like "Delivery method must be ____, (non) negotiable, etc."
![undonecarrot doing .buyoffer Stone 64 Gold 1 UC and UC Systems Bot responding with "Listing successful!"](https://user-images.githubusercontent.com/79398813/184498532-83c9e6e8-ae70-4b3f-970b-ce5c404da440.png)

Returns:

![An embed by UC Systems Bot with the text: undonepotato#1584 |
UC Buy Offer |
UC is buying 64 Stone for 1 Gold. |
To claim this offer, press the button below to open a negotiation channel. |
Times are in UTC. • Today at 2:34 PM |, the UC flag, and a green button that says "Open Channel" on the bottom of the message.](https://user-images.githubusercontent.com/79398813/184498836-76bf42cc-6220-42d4-beda-4a89274cb8fe.png)


### Use Cases
If you want to post an offer for buying something, and you're not at the in-game market.






