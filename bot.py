import re
from random import randint

from pyrogram import Client, Emoji, Filters, Message
from pyrogram.errors import MessageTooLong

RE_DICE = re.compile(r"(?P<count>\d*)d(?P<sides>\d+)")
START = (
    "Hi there {} {}\n\n"
    + "I can roll you any amount of dice with any amount of sides. "
    + "Just send /roll and pass a die format like `2d6` for two six-sided die. "
    + "Maybe just `d4` for a four-sided die. Or even `5d20` for five 20-sided die.\n\n"
    + "You can also [add me to groups](https://t.me/Rolling_Dice_Bot?startgroup=yeet) "
    + "so I can roll you a dice there :D"
)
START_GROUP = (
    "Thanks for adding me to your group {0}\n"
    + "You can either just /roll for a standard six-sided die, or use the [Dice "
    + "Notation](https://en.wikipedia.org/wiki/Dice_notation#Standard_notation) to "
    + "roll more die with more sides.\n"
    + "Use `/roll d10` for a ten-sided dice, or `/roll 4d20` for four 20-sided die. "
    + "It's that easy {0}"
)
DICE = "Your rolled dice " + Emoji.GAME_DIE

# App definition
app = Client(session_name="DiceBot")


@app.on_message(Filters.command("start") & Filters.private)
def start(app: Client, message: Message):
    message.reply_text(
        START.format(message.from_user.first_name, Emoji.GAME_DIE),
        disable_web_page_preview=True,
    )


@app.on_message(Filters.new_chat_members)
def added(app: Client, message: Message):
    if app.get_me().id in [i.id for i in message.new_chat_members]:
        app.send_message(
            message.chat.id,
            START_GROUP.format(Emoji.GAME_DIE), disable_web_page_preview=True
        )


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
            try:
                message.reply_text(DICE + "\n`" + "`, `".join(die) + "`")
            except MessageTooLong:  # Handle messages that are >4096 characters long.
                message.reply_text("Please try with less dice.")

    else:
        message.reply_text(DICE + "\n`" + str(randint(1, 6)) + "`")


app.run()
