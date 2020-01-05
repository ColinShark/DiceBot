import re
from random import randint

from pyrogram import Client, Emoji, Filters, Message

RE_DICE = re.compile(r"(?P<count>\d*)d(?P<sides>\d+)")
START = """
Hi there {} {}

I can roll you any amount of dice with any amount of sides.
Just send /roll and pass a die format like `2d6` for two six-sided die.
Maybe just `d4` for a four-sided die. Or even `5d20` for five 20-sided die.

You can also [add me to groups](https://t.me/Rolling_Dice_Bot?startgroup=hi_there) \
so I can roll you a dice there :D
"""
DICE = "Your rolled dice " + Emoji.GAME_DIE

# App definition
app = Client(session_name="DiceBot")


@app.on_message(Filters.command("start"))
def start(app: Client, message: Message):
    message.reply_text(START.format(message.from_user.first_name, Emoji.GAME_DIE))


@app.on_message(Filters.command("roll") & ~Filters.edited)
def roll(app: Client, message: Message):
    if len(message.command) > 1:
        r = RE_DICE.match(message.command[1])
        if r:
            count = r.group("count") or 1
            sides = r.group("sides")
            die = []
            for i in range(int(count)):
                die.append(str(randint(1, int(sides))))
            message.reply_text(DICE + "\n`" + "`, `".join(die) + "`")

    else:
        message.reply_text(DICE + "\n`" + str(randint(1, 6)) + "`")


app.run()
