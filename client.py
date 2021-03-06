import os
import re

import discord

import message as msg
from lib.maker import Maker
from lib.my_error import MakerFailed, ParserFailed, SystemWarn
from lib.parser import SubCommandParser

# test
# from dotenv import load_dotenv



client = discord.Client()

# test
# load_dotenv(verbose=True)


# TODO
# pow(**) 小数の時バグる  : lib.parser



@client.event
async def on_ready():
    print(f"starting ... {client.user}\n")


@client.event
async def on_message(message):
    # botのメッセージは除く
    if message.author.bot:
        return

    content = re.sub(r"```", "", message.content) # コードブロックを消す

    if content.startswith('hello'):
        await message.channel.send('Hello!')

    if not content.startswith("jump"):
        return

    command = re.sub(r"jump\s*", "", content)


    if command.startswith("make"):
        sub_cmd = re.sub(r"make\s*", "", command)
        print("sub_cmd:", sub_cmd, "\n")
        
        # parser
        parser = SubCommandParser()
        try:
            parser.run(sub_cmd)
            if len(parser.warn) > 0:
                text = ""
                for w in parser.warn:
                    text += f"\n:issue_icon: `{w}`に、なにも入ってないよ！"
                await message.channel.send(text + " (デフォルト値で実行中...)")
        except SystemWarn:
            await message.channel.send("わーん")
        except ParserFailed as e:
            await message.channel.send(f":WA: `<Parser>` `{e.args[0]}`")
        except Exception as e:
            await message.channel.send(f"`<Parser>` <@{admin_id}>\ntype {type(e)}\nargs{e.args}")
        else: # clear parser
            # test
            # Maker.make(parser.eq, parser.var, parser.times, parser.range)
            # await message.channel.send(file=discord.File('image/jump.gif'))
            
            try:
                Maker.make(parser.eq, parser.var, parser.times, parser.range)
            except MakerFailed as e:
                await message.channel.send(f":WA: `<Maker>` `{e.args[0]}`")
            except Exception as e:
                await message.channel.send(f"`<Maker>` <@{admin_id}>\ntype {type(e)}\nargs{e.args}")
            else: # complete image
                print("=== Send gif image ===\n")
                await message.channel.send(":AC:")
                await message.channel.send(file=discord.File('image/jump.gif'))
        return

    if command.startswith("last"):
        await message.channel.send(file=discord.File('image/jump.gif'))
        return

    if command.startswith("help"):
        more_help = re.sub(r"help\s*", "", command)
        if more_help in list(msg.help_list.keys()):
            await message.channel.send(msg.help_list[more_help])
        elif more_help == "":
            await message.channel.send(msg.about)
        else:
            await message.channel.send(f"help '{more_help}' は見つかりません")
        return

    if command.startswith("info"):
        await message.channel.send(msg.info)
        return

    if command == "":
        await message.channel.send(msg.about)
        return

    await message.channel.send("コマンド : `" + command + "` が見つかりません")



if __name__ == "__main__":
    admin_id = "603591881317810207"
    client.run(os.environ['DISCORD_BOT_TOKEN'])
