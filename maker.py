from PIL import Image
import re
import math



class Stage:
    def __init__(self, width = 100, height = 100, color = (255, 255, 255), ground = None):
        self.width = width
        self.height = height
        self.color = color
        if ground is None:
            self.ground = self.height * 0.8
        else:
            self.ground = ground

        self.image = Image.new("RGB", (self.width, self.height), self.color)


    def info(self):
        print(f"width: {self.width}")
        print(f"height: {self.height}")
        print(f"ground: {self.ground}")



class Sprite:
    def __init__(self, mode: str, path="", width=0, height=0, color=(0,0,0), resize=(0, 0)):
        if mode == "load":
            self.mode = mode
            if type(path) == str:
                self.path = [path]
            else:
                self.path = path

            self.images = []
            for p in range(len(self.path)):
                self.images.append(Image.open(self.path[p]))
                if resize[0] > 0 and resize[1] > 0:
                    self.images[p] = self.images[p].resize((resize[0], resize[1]))

            self.image = self.images[0]
            self.width, self.height = self.image.size[0], self.image.size[1]
        elif mode == "make":
            self.mode = mode
            self.width = width
            self.height = height
            self.color = color
            self.image = Image.new("RGB", (self.width, self.height), self.color)
        else:
            print("error")



"""
ステージ, スプライト, 式, 描画回数(TODO 自動判定)
式(str)を評価して、それをもとにgif画像を作る
"""
class Maker:
    stage = Stage(width=360, height=640, color=(160, 161, 254))
    sprite = Sprite("load", path=["image/ichiyo00.png", "image/ichiyo01.png"], resize=(100, 100))
    
    # put block
    block = Sprite("load", path="image/block.png")
    __resize_h = int((stage.height - stage.ground) / 2)
    __resize_w =  int(block.width * __resize_h / block.height)
    block.image = block.image.resize((__resize_w, __resize_h))
    __x, __y = 0, 0
    for __y in range(2):
        for __x in range(int(stage.width / __resize_w) + 1):
            stage.image.paste(block.image, (__x*__resize_w, int(stage.ground) + __y*__resize_h))
        

    @classmethod
    def make(cls, args, stage = stage, sprite = sprite) -> list:
        gif = []
        
        eq = cls.__in_default_args(args, "eq", "y = 0.5*g*t*t - v0*t + ground")
        var = cls.__in_default_args(args, "var", {})
        times = cls.__in_default_args(args, "times", 50)
        self_range = cls.__in_default_args(args, "range", "above-ground")

        var = cls.__default_var_set(stage, sprite, var)
        result = cls.__eq_converter(eq)
        if result[0] == "error":
            return result
        else:
            eq = result

        # GIF画像作成のメイン部分
        for var["t"] in range(times):
            for i in range(len(eq)):
                try:
                    exec("import math; " + eq[i], {}, var)
                except ArithmeticError:
                    return ["error", "exec-arithmetic-error"]
                except NameError:
                    return ["error", "exec-name-error"]
                except SyntaxError:
                    return ["error", "exec-syntax-error"]
                else:
                    return ["error", "exec-exception"]

            # print(f"t: {var['t']} y : {var['y']} type: {type(var['y'])}")

            if self_range == "above-ground": # 地面より上 xの制限はなし
                var["y"] = min([stage.ground - sprite.height, var["y"]])
            elif self_range == "lock": # 画面内かつ地面より上
                var["x"] = min([stage.width - sprite.width, max([var["x"], 0])])
                var["y"] = min([stage.ground - sprite.height, max([var["y"], 0])])
            elif self_range == "display": # 画面内
                var["x"] = min([stage.width - sprite.width, max([var["x"], 0])])
                var["y"] = min([stage.height - sprite.height, max([var["y"], 0])])
            elif self_range == "free": # 制限なし
                pass
            else:
                return ["error", "has not range", self_range]
                
            back = stage.image.copy()

            splited_y = int(int(var["y"]) * len(sprite.images) / int(stage.ground)) # 表示する画像を変える
            splited_y = max([0, min(splited_y, len(sprite.images))])
            img = sprite.images[len(sprite.images) - 1 - splited_y]
            back.paste(img, (int(var["x"]), int(var["y"])), img)
            
            gif.append(back)

        gif[0].save("image/jump.gif", save_all=True, append_images=gif[1:], optimize=False, duration=60, loop=0, quaulity=100)
        return ["comp"]


    # 変数のデフォルトの設定
    # make()の引数varで、既に定義されている変数はそっちを優先する
    @classmethod
    def __default_var_set(cls, stage, sprite, var):
        if "x" not in list(var.keys()):
            var["x"] = (stage.width - sprite.width) / 2
        if "y" not in list(var.keys()):
            var["y"] = stage.ground - sprite.height
        if "t" not in list(var.keys()):
            var["t"] = 0
        if "g" not in list(var.keys()):
            var["g"] = 9.8
        if "v0" not in list(var.keys()):
            var["v0"] = 80
        if "ground" not in list(var.keys()):
            var["ground"] = stage.ground - sprite.height
        return var


    @classmethod
    def __in_default_args(cls, args: dict, key_name: str, default_value):
        if key_name in list(args.keys()):
            return args[key_name]
        else:
            return default_value
    
            
    @classmethod
    def __my_replace(cls, changing, after_val, string):
        if re.search(re.compile(r"\W+" + changing), string):
            string = re.sub(changing, after_val, string)
        return string

    @classmethod
    def __my_replace_const(cls, changing, after_val, string):
        if re.search(re.compile(r"\W+" + changing + r"\W+"), string):
            string = re.sub(changing, after_val, string)
        return string
    
    @classmethod
    def __my_replace_pow(cls, string):
        # TODO replace pow function
        return string.replace("^", "**")
    
    @classmethod
    def __my_replace_log(cls, string):
        log = re.findall(r"log([1-9]\d*)\((.*)\)", string)
        if log != []:
            string = re.sub(r"log([1-9]\d*)\((.*)+\)", f"math.log({log[0][1]}, {log[0][0]})", string)
        return string

    
    @classmethod
    def __eq_converter(cls, eq):
        if type(eq) == str:
            eq = [eq]
        for i in range(len(eq)):
            print("       in : " + eq[i])

            # replace eq
            eq[i] = cls.__my_replace(r"deg\(", "math.deg(", eq[i])
            eq[i] = cls.__my_replace(r"rad\(", "math.rad(", eq[i])
            eq[i] = cls.__my_replace(r"sin\(", "math.sin(", eq[i])
            eq[i] = cls.__my_replace(r"cos\(", "math.cos(", eq[i])
            eq[i] = cls.__my_replace(r"tan\(", "math.tan(", eq[i])
            eq[i] = cls.__my_replace(r"asin\(", "math.asin(", eq[i])
            eq[i] = cls.__my_replace(r"acos\(", "math.acos(", eq[i])
            eq[i] = cls.__my_replace(r"atan\(", "math.atan(", eq[i])
            eq[i] = cls.__my_replace(r"atan2\(", "math.atan2(", eq[i])
            eq[i] = cls.__my_replace_const(r"(pi|PI|π)", "math.pi", eq[i])
            eq[i] = cls.__my_replace_const("e", "math.e", eq[i])
            eq[i] = cls.__my_replace_pow(eq[i]) # TODO
            eq[i] = cls.__my_replace_log(eq[i])
            
            print("converted : " + eq[i])

            # 'x =' か 'y = ' から始まらないとエラー
            target = re.findall(r"^(\w\d|\w)\s*=\s*(.+)\s*$", eq[i]) # [!] タプルで返ってくる
            if target[0][0] != "x" and target[0][0] != "y":
                print(f"[!] Error: {target[0][0]} is Not found")
                return ["error", f"{target[0][1]} is cannot change"]

            # kata = type(eval(target[0][1], {}, var))
            # if kata != int and kata != float:
            #     print(f"[!] Error: please number ({target[0][1]})")
            #     return ["error", "plz-num"]
        
        return eq



# Maker.make()
