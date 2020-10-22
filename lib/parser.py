import re
from lib.my_error import ParserFailed, SystemWarn
from lib.maker import Maker



class SubCommandParser:
    def __init__(self):
        #            default value
        self.eq    = ["y = 0.5*g*t*t - v0*t + ground"]
        self.var   = {
            "x": (Maker.stage.width - Maker.sprite.width) / 2,
            "y": Maker.stage.ground - Maker.sprite.height,
            "t": 0,
            "g": 9.8,
            "v0": 80,
            "ground": Maker.stage.ground - Maker.sprite.height
        }
        self.times = 50
        self.range = "default"

        # 警告はメッセージを送って、値はデフォルト値
        # warn には "eq", "var"などのサブコマンドの文字列を入れる
        self.warn = []


    def run(self, sub_cmd: str) -> None:
        print(">>> Parser running ...")
        print("  input:")
        self.parse_eq(sub_cmd)
        self.parse_var(sub_cmd)
        self.parse_times(sub_cmd)
        self.parse_range(sub_cmd)

        print("\n  result:")
        print("    eq    :", self.eq)
        print("    var   :", self.var)
        print("    times :", self.times)
        print("    range : '" + self.range + "'")
        print("<<< Parser complete!\n")


    def parse_eq(self, sub_cmd: str):
        if not re.search(r"(^|\s+)eq\[.*?\]", sub_cmd):
            return

        eq_list = re.findall(r"eq\[(.*?)\]", sub_cmd)
        print("    eq", eq_list)
        if eq_list != []:
            if eq_list[0] == "":
                self.warn.append("eq")
                print("warning << 'eq'")
                return
            if ";" in eq_list[0]:
                print("<<< Find System Warning")
                raise SystemWarn

            pair_list = re.findall(r"([^,]*)(,*\s*)", eq_list[0])
            # ','以外の文字列と','を探す
            # -> [('eq', ', '), ('eq2', '') ... ('', '')]
            # print("pair_list", pair_list)
            
            self.eq = []
            for _eq in pair_list:
                if _eq[0] != "":
                    target = re.findall(r"^(\w\d|\w)\s*=\s*(.+)\s*$", _eq[0])
                    target = target[0][0]
                    if target != "x" and target != "y": # x か y から始まるか
                        print("<<< ParserFaild")
                        raise ParserFailed("eq[] needs to start with 'x' or 'y'")
                    
                    self.eq.append(_eq[0])
        # replace eq
        # ex) sin() => math.sin()
        #     PI    => math.pi
        self.__eq_math_replace()


    def parse_var(self, sub_cmd: str):
        if not re.search(r"(^|\s+)var\[.*?\]", sub_cmd):
            return

        var_list = re.findall(r"var\[(.*)\]", sub_cmd)
        print("    var", var_list)
        if var_list != []:
            if var_list[0] == "":
                self.warn.append("var")
                print("warning << 'var'")
                return
            if ";" in var_list[0]:
                print("<<< Find System Warning")
                raise SystemWarn

            var_list = re.findall(r"([^,]*)(,*\s*)", var_list[0])
            for _var in var_list:
                if _var[0] != "":
                    pair = re.findall(r"(.*?)\s*=\s*(.*)(,?\s*)", _var[0])
                    pair = pair[0]
                    try:
                        self.var[pair[0]] = eval(pair[1])
                    except Exception:
                        print("<<< ParserFaild")
                        raise ParserFailed("var[] wrong argument")

        

    def parse_times(self, sub_cmd: str):
        if not re.search(r"(^|\s+)times\[.*?\]", sub_cmd):
            return
        
        times = re.findall(r"times\[(.*?)\]", sub_cmd)
        print("    times", times)
        if times != []:
            if times[0] == "":
                self.warn.append("times")
                print("warning << 'tiems'")
                return
            try:
                self.times = int(times[0])
            except Exception:
                print("<<< ParserFaild")
                raise ParserFailed("times[] wrong argument")


    def parse_range(self, sub_cmd: str):
        if not re.search(r"(^|\s+)range\[.*?\]", sub_cmd):
            return
        
        self_range = re.findall(r"range\[(.*?)\]", sub_cmd)
        print("    range", self_range)
        
        range_list = ["default", "free", "lock", "display"]

        if self_range != []:
            if self_range[0] == "":
                self.warn.append("range")
                print("warning << 'range'")
                return
            elif self_range[0] in range_list:
                self.range = self_range[0]
            else:
                print("<<< ParserFaild")
                raise ParserFailed(f"range[] '{self_range[0]}' is Not Found")


    def __eq_math_replace(self):
        print("      math replace")
        if type(self.eq) == str:
            self.eq = [self.eq]
        
        for i in range(len(self.eq)):
            print("        in  : " + self.eq[i])
            self.__replace_function(self.eq[i], [
                [r"deg\(",   "math.deg("],
                [r"rad\(",   "math.rad("],
                [r"sin\(",   "math.sin("],
                [r"cos\(",   "math.cos("],
                [r"tan\(",   "math.tan("],
                [r"asin\(",  "math.asin("],
                [r"acos\(",  "math.acos("],
                [r"atan\(",  "math.atan("],
                [r"atan2\(", "math.atan2("]
            ])
            self.__replace_const(self.eq[i], [
                [r"(pi|PI|π)", "math.pi"],
                ["e", "math.e"]
            ])

            # TODO replace pow function
            self.eq[i].replace("^", "**")

            log = re.findall(r"log([1-9]\d*)\((.*)\)", self.eq[i])
            if log != []:
                self.eq[i] = re.sub(r"log([1-9]\d*)\((.*)+\)", f"math.log({log[0][1]}, {log[0][0]})", self.eq[i])

            print("        out : " + self.eq[i])

            # TODO evalute eq and check


    # list [regex, after_str]
    def __replace_function(self, at: str, list: list):
        for i in range(len(list)):
            regex = list[i][0]
            after_str = list[i][1]
            if re.search(re.compile(r"\W+" + regex), at):
                at = re.sub(regex, after_str, at)


    # list [regex, after_str]
    def __replace_const(self, at: str, list: list):
        for i in range(len(list)):
            regex = list[i][0]
            after_str = list[i][1]
            if re.search(re.compile(r"\W+" + regex + r"\W+"), at):
                at = re.sub(regex, after_str, at)
