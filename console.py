import lib.my_error as err
from lib.maker import Maker
from lib.parser import SubCommandParser


"""
サブコマンドのテスト用
"""

if __name__ == "__main__":
    print("console.py> ", end="")
    content = input()
    while content != "exit":
        parser = SubCommandParser()
        try:
            parser.run(content)
        except err.SystemWarn:
            print("わーん")
        except Exception as e:
            print(e)
        else: # clear parser  
            try:
                Maker.make(parser.eq, parser.var, parser.times, parser.range)
            except Exception as e:
                print("maker error")
                print(e)
                print("make error")
            else: # complete image
                print(" :: send gif image :: \n")
        print("console.py> ", end="")
        content = input()
