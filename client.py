import os
import re
from dotenv import load_dotenv
import discord

import lib.my_error as err
from lib.maker import Maker
from lib.parser import SubCommandParser
import message as msg
# import error_message as err_msg


load_dotenv(verbose=True)
client = discord.Client()


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
        except err.SystemWarn:
            await message.channel.send("わーん")
        except Exception as e:
            print(e)
        else: # clear parser  
            try:
                Maker.make(parser.eq, parser.var, parser.times, parser.range)
            except Exception as e:
                print("maker error")
                print(e)
                await message.channel.send("make error")
            else: # complete image
                print(" :: send gif image :: \n")
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
    client.run(os.environ['TOKEN'])
