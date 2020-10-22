import re
import lib.my_error as err
from lib.maker import Maker


# TODO replace pow function  (L.124)
# TODO eval eq and check     (L.133)


class SubCommandParser:
    def __init__(self):
        #            default value
        self.eq    = ["y = 0.5*g*t*t - v0*t + ground"]
        self.var   = {}
        self.times = 50
        self.range = "default"


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
        eq_list = re.findall(r"eq\[(.*?)\]", sub_cmd)
        print("    eq", eq_list)
        if eq_list != []:
            if eq_list[0] == "":
                raise err.WarnEmptyEQ
            if ";" in eq_list[0]:
                raise err.SystemWarn

            pair_list = re.findall(r"([^,]*)(,*\s*)", eq_list[0])
            # ','以外の文字列と','を探す
            # -> [('eq', ', '), ('eq2', '') ... ('', '')]
            # print("pair_list", pair_list)
            
            self.eq = []
            for _eq in pair_list:
                if _eq[0] != "":
                    self.eq.append(_eq[0])
        # replace eq
        # ex) sin() => math.sin()
        #     PI    => math.pi
        self.__eq_math_replace()


    def parse_var(self, sub_cmd: str):
        var_list = re.findall(r"var\[(.*)\]", sub_cmd)
        print("    var", var_list)
        if var_list != []:
            if var_list[0] == "":
                raise err.WarnEmptyVAR

            pair_list = re.findall(r"((\w+|\d+)+\s*=\s*(\d*))(,?\s*)", var_list[0])
            # -> [('y = 100', 'y', '100', ', '), ('x = 100', 'x', '100', '')]
            # print("pair_list", pair_list)

            self.var = {}
            for _var in pair_list:
                self.var[_var[1]] = float(_var[2])
        
        # 変数のデフォルトの設定
        self.__input_undefined_value(self.var, {
            "x": (Maker.stage.width - Maker.sprite.width) / 2,
            "y": Maker.stage.ground - Maker.sprite.height,
            "t": 0,
            "g": 9.8,
            "v0": 80,
            "ground": Maker.stage.ground - Maker.sprite.height
        })


    def parse_times(self, sub_cmd: str):
        times = re.findall(r"times\[(\d+)\]", sub_cmd)
        print("    times", times)
        if times != []:
            if times[0] == "":
                raise err.WarnEmptyTIMES
            self.times = int(times[0])


    def parse_range(self, sub_cmd: str):
        self_range = re.findall(r"range\[(.*?)\]", sub_cmd)
        print("    range", self_range)
        # TODO can use that range?
        if self_range != []:
           if self_range[0] == "":
               raise err.WarnEmptyRANGE
           self.range = self_range[0]



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

            # TODO eval eq and check

            # 'x =' か 'y = ' から始まらないとエラー
            target = re.findall(r"^(\w\d|\w)\s*=\s*(.+)\s*$", self.eq[i]) # [!] タプルで返ってくる
            if target[0][0] != "x" and target[0][0] != "y":
                print(f"[!] Error: {target[0][0]} is Not found")
                return ["error", f"{target[0][1]} is cannot change"]

            # kata = type(eval(target[0][1], {}, var))
            # if kata != int and kata != float:
            #     print(f"[!] Error: please number ({target[0][1]})")
            #     return ["error", "plz-num"]


    # list [func_regex, after_str]
    def __replace_function(self, at: str, list: list):
        for i in range(len(list)):
            regex = list[i][0]
            after_str = list[i][1]
            if re.search(re.compile(r"\W+" + regex), at):
                at = re.sub(regex, after_str, at)


    # list [func_regex, after_str]
    def __replace_const(self, at: str, list: list):
        for i in range(len(list)):
            regex = list[i][0]
            after_str = list[i][1]
            if re.search(re.compile(r"\W+" + regex + r"\W+"), at):
                at = re.sub(regex, after_str, at)


    # dictのkeyが存在しない場合はdictのvalueを代入する
    def __input_undefined_value(self, at_dict, cf_dict: dict):
        for key, val in cf_dict.items():
            if key not in list(at_dict.keys()):
                at_dict[key] = val

