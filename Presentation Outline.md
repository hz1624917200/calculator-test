## Features

* 符号解析
* 鲁棒性
* 解释器结构
    * 解析成指令序列
* 特殊运算 - 任意次
    * 快速幂
    * 开方
    * 逻辑运算符
    * 缺省符号
* 适用范围广



## Testcase Generator

* 结构
    * op opand 相错



## Bugs

* 没有增加`var_iter`
* 快速幂
    * L313: `isNegative = 0;`
    * data in output-success.csv