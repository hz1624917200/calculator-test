# Calculator demo for software test

> 软件缺陷定位示例项目

## Project Structure

* `calculator.cpp` 主程序，带有符号解析功能的科学计算器
* `generator.py` 测试样例生成器
* `judge.py` 测评系统（演示用）
    * `judge-old.py` 正式开发测试用测评系统，与Python `eval`解析器进行对开
    * `validate.py` 正式测试系统的依赖项

## Run

```python
python generator.py
<num_of_testcases>
# output in ./testcase/

python judge.py
# generate .gcov coverage info statistics in ./gcov-res

python data_extract.py
# extract data from gcov info
```



## Todo

* `data_extract` 将数据抽出到`global_stat`，与Jupiter notebook中格式一致
    * 增加用数据生成四种算法图表的功能（hq）
    * 选取位置进行修改，测试定位效果（hz）