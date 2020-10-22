from lib.my_error import MakerFailed, ParserFailed, SystemWarn
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
        except SystemWarn:
            print("わーん")
        except ParserFailed as e:
            print(f"ParserFaild {e.args[0]}")
        except Exception as e:
            print(f"Parser Error {e.args}")
            print(f"type {type(e)}")
            print(f"args {e.args}")
        else: # clear parser
            # test
            # Maker.make(parser.eq, parser.var, parser.times, parser.range)
            
            try:
                Maker.make(parser.eq, parser.var, parser.times, parser.range)
            except Exception as e:
                print(f"Maker Error")
                print(f"type {type(e)}")
                print(f"args {e.args}")
            else: # complete image
                print("=== Send gif image ===\n")
        
        print("console.py> ", end="")
        content = input()
