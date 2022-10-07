import copy
import os

var_operand = [chr(i) for i in range(ord('a'), ord('z') + 1)] + \
              [chr(i) for i in range(ord('A'), ord('Z') + 1)]

if not os.path.exists('./result'):
    os.mkdir('./result')

for infile in os.listdir('./testcase'):
    expressions = open('./testcase/' + infile)
    output = open('./result/' + infile.replace('.', '_res.'), 'w')
    expression = expressions.readline()
    # '+0'防止最后一个运算是开方，导致加右括号失败
    expression = expression.strip() + '+0'
    # 先处理开方
    # 先在_的后一个运算数的后面加右括号
    tmp = ''
    root = False
    # 顺便看看有哪些字母
    _vars = []
    for index, c in enumerate(expression):
        if c in var_operand:
            assert(c not in _vars)
            _vars.append(c)
        # 允许_后面立即出现负号，需考虑_!-的情况
        if root and expression[index - 1] != '_'and expression[index - 2: index] != '_!' and c in '+-*/^_>=<&|':
            tmp += ')'
            root = False
        tmp += c
        if c == '_':
            root = True
    # 替换
    expression = tmp.replace('_', '**(1/')
    while True:
        assign = expressions.readline().strip().split(' ')
        # ''.split(' ')会变成['']
        if '' in assign:
            assign = []
        if any([i in expression for i in var_operand]) and not assign:
            break
        expression_cpy = copy.copy(expression)
        assert(len(assign or []) == len(_vars))
        for index, var_value in enumerate(assign or []):
            expression_cpy = expression_cpy.replace(_vars[index], var_value)
        # 要先代入再替换运算符，不然会把比如not中的t代掉
        # 处理!，在!的后一个运算数或右括号的后面加右括号
        tmp = ''
        status = ""  # 标记!后的状态
        for index, c in enumerate(expression_cpy):
            # 允许!后面立即出现负号
            if status != '' and expression_cpy[index - 1] != '!':
                if (status == '(' and c == ')') or (status == 'imm' and c in '+-*/^_>=<&|'):
                    tmp += ')'
                    status = ''
            tmp += c
            if c == '!':
                if expression_cpy[index + 1] == '(':
                    status = '('
                else:
                    status = 'imm'
        expression_cpy = tmp.replace('!', '(not ')
        # 替换
        expression_cpy = expression_cpy \
            .replace('^', '**') \
            .replace('=', '==') \
            .replace('&', ' and ') \
            .replace('|', ' or ')
        # print(expression_cpy)
        try:
            res = str(eval(expression_cpy))
            if 'j' in res:
                raise TypeError("complex!")
            elif res == 'False':
                res = '0'
            elif res == 'True':
                res = '1'
            elif res == '0.0':
                res = '0'
            output.write(res + '\n')
        except ZeroDivisionError as e:
            output.write(str(e) + '\n')
        except TypeError as e:
            # 若出现虚数比较大小会触发此异常
            output.write(str(e) + '\n')
        except OverflowError as e:
            # 太大了，溢出了
            output.write(str(e) + '\n')
        # 无变量
        if not any([i in expression for i in var_operand]):
            break
