import os
import re
from dotenv import load_dotenv
import discord

from maker import Image, Sprite, Maker
import message as msg
import error_message as err_msg


load_dotenv(verbose=True)
client = discord.Client()


# TODO
# pow(**) 小数の時バグる
# 引数の変換やチェックをクラスにまとめる


def arg_manage(sub_cmd):
    args = {}
    eq_list = re.findall(r"eq\[(.*?)\]", sub_cmd)
    if eq_list != []:
        if eq_list[0] == "":
            args["error"] = "empty-eq"
            return args
        if ";" in eq_list[0]:
            args["error"] = "warn"
            return args
        
        eq = re.findall(r"([^,]*)(,*\s*)", eq_list[0])    
        args["eq"] = []
        for e in eq:
            if e[0] != "":
                args["eq"].append(e[0])
    
    var_list = re.findall(r"var\[(.*)\]", sub_cmd)
    if var_list != []:
        if var_list[0] == "":
            args["error"] = "empty-var"
            return args
        
        pair = re.findall(r"((\w+|\d+)+\s*=\s*(\d*))(,?\s*)", var_list[0])
        args["var"] = {}
        for p in pair:
            args["var"][p[1]] = float(p[2])

    times = re.findall(r"times\[(\d+)\]", sub_cmd)
    if times != []:
        if times[0] == "":
            args["error"] = "empty-times"
            return args
        args["times"] = int(times[0])

    self_range = re.findall(r"range\[(.*?)\]", sub_cmd)
    if self_range != []:
        if self_range[0] == "":
            args["error"] = "empty-range"
            return args
        args["range"] = self_range[0]

    return args


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

    # make
    if command.startswith("make"):
        sub_cmd = re.sub(r"make\s*", "", command)
        
        print("\ncommand: " + sub_cmd)
        args = arg_manage(sub_cmd)
        if "error" in list(args.keys()):
            err = args["error"]
            print(f"args-manage error\nerror code : {err}")
            empty = re.findall(r"^empty-(.*)", err)
            if err == "warn":
                await message.channel.send("[!] Error: わーん")
            elif empty != []:
                await message.channel.send(f"[!] Error: サブコマンド {empty[0]}[]の値が空です")
            else:
                await message.channel.send("予期せぬエラーが発生しました")
            return

        print("args : \n  ", end="")
        print(args)

        result = Maker.make(args)
        if result[0] == "comp":
            print(" - comp - ")
            await message.channel.send(file=discord.File('image/jump.gif'))
        elif result[0] == "error":
            print("\nerror code: " + result[1])
            if result[1] in list(err_msg.error.keys()):
                await message.channel.send("[!] エラー: " + err_msg.error[result[1]])
            else:
                await message.channel.send("[!] Error Code " + result[1])
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



if __name__ == "__main__":
    client.run(os.environ['TOKEN'])
