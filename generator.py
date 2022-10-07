import random
import os

# 生成的用例数
gen_num = 100
# file = open("./expressions.txt", "w")

# 后者为概率
binary_operator = {('+', '-', '*', '/'): 0.7, ('^', '_'): 0.2, ('>', '=', '<', '&', '|'): 0.1}
unary_operator = ['!']
# 期望
mu = 0
# 标准差
sigma = 10
# 出现小数的概率
prob_float = 0.1
# 小数的最大位数
max_decimal_place = 6


# 获取立即数
def imm_operand(allow_float: bool):
    num = str(int(random.gauss(mu, sigma)))
    # 随机生成小数
    if allow_float and not bool_rand(prob_float):
        num += '{:.{}f}'.format(random.random(), random.randint(0, max_decimal_place))[1:]  # 去掉最前面的0
    return num


var_operand = [chr(i) for i in range(ord('a'), ord('z') + 1)] + \
              [chr(i) for i in range(ord('A'), ord('Z') + 1)]
lbracket = '('
rbracket = ')'


def main():
    if not os.path.exists('./testcase'):
        os.mkdir('./testcase')
    for i in range(gen_num):
        file = open("./testcase/{}.in".format(i), "w")
        expression = ''
        lbracket_cnt = 0
        var_operand_list = []
        allow_float = True
        allow_bracket = True
        while bool_rand(0.9):
            # 随机插入括号
            if allow_bracket and bool_rand(0.1):
                expression += lbracket
                lbracket_cnt += 1
            allow_bracket = True
            # # 随机插入一元运算符
            if bool_rand(0.1):
                expression += random.choice(unary_operator)
            # 拼接运算数
            if bool_rand(0.9):
                s = imm_operand(allow_float)
            else:
                # 不允许重复
                s = random.choice(var_operand)
                while s in [i[0] for i in var_operand_list]:
                    s = random.choice(var_operand)
                var_operand_list.append((s, allow_float))
            allow_float = True
            expression += s
            # 随机闭合括号
            if lbracket_cnt and bool_rand(0.3):
                expression += rbracket
                lbracket_cnt -= 1
            # 拼接运算符
            for operators, probability in binary_operator.items():
                if bool_rand(probability):
                    expression += random.choice(operators)
                    break
            else:  # for-else骚操作
                expression += random.choice(list(binary_operator)[0])
            # 不允许生成小数开方
            if expression[-1] == '_':
                allow_float = False
                allow_bracket = False  # 防止括号里产生小数
        # # 随机插入一元运算符
        if bool_rand(0.1):
            expression += random.choice(unary_operator)
        if bool_rand(0.9):
            s = imm_operand(allow_float)
        else:
            # 不允许重复
            s = random.choice(var_operand)
            while s in [i[0] for i in var_operand_list]:
                s = random.choice(var_operand)
            var_operand_list.append((s, allow_float))
        allow_float = True
        expression += s
        # 闭合全部括号
        while lbracket_cnt:
            expression += rbracket
            lbracket_cnt -= 1
        file.write(expression + '\n')
        # print(expression)
        # 若有未知数，需插入几行赋值
        while var_operand_list:
            for var, _allow_float in var_operand_list:
                # 空格分割，x=1的形式
                file.write(str(imm_operand(_allow_float)) + ' ')
            file.write('\n')
            # 一行
            if 1 or bool_rand(0.1):
                break
    pass


def bool_rand(probability: float):
    """
    以probability的概率返回真
    """
    return random.random() < probability


if __name__ == "__main__":
    main()
