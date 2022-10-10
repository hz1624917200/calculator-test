from io import TextIOWrapper
import os
import re
import pandas as pd
from matplotlib import pyplot as plt
import csv
from typing import Dict, List

# global exec info static data
# [N_cf, N_cs, N_uf, N_us]
global_stat: Dict[int, List[int]] = {}

with open("correct_list.txt", "r") as f:
	passed_test: List[int] = eval(f.read())

def stat_exec(f: TextIOWrapper) -> Dict[int, bool]:
	stat_dict = {}
	for line in f.readlines():
		if "-:" in line:
			continue
		if (lno := re.search(r":\s*?(\d+):", line)) is not None:
			# print(lno.group(0))
			stat_dict[int(lno.group(1))] = "#####" not in line
	return stat_dict


def update_global(single_dict: Dict[int, bool], passed: bool) -> None:
	offset = 1 if passed else 0
	for lno in single_dict:
		value_list = global_stat.get(lno, [0, 0, 0, 0])
		if single_dict[lno]:
			value_list[offset] += 1
		else:
			value_list[2 + offset] += 1
		global_stat[lno] = value_list
			
def generator_csv():
	df = pd.DataFrame.from_dict(global_stat,
								orient='index',
								columns=['N_cf', 'N_cs', 'N_uf', 'N_us'] )
	df['N_f'] = df['N_cf'] + df['N_uf']
	df['N_s'] = df['N_cs'] + df['N_us']
	n = len(global_stat)
	df['Tarantula'] = (df['N_cf']/df['N_f']) / (df['N_cf']/df['N_f'] + df['N_cs']/df['N_s'])
	df['Zoltar'] = (df['N_cf'])/(df['N_cf'] + df['N_uf'] + df['N_cs'] + (10000 * df['N_uf'] * df['N_cs'])/(df['N_cf']))
	df['Sokal'] = (2 * (df['N_cf'] + df['N_us']))/(2 * (df['N_cf'] + df['N_us']) + df['N_uf'] + df['N_cs'])
	df['Fossum'] = (n * ((df['N_cf'] - 0.5) ** 2))/((df['N_cf'] + df['N_cs']) * (df['N_cf'] + df['N_uf']))
	df.to_csv('output.csv')

def draw_bar():
	data = pd.read_csv('output.csv',usecols=['Tarantula','Zoltar','Sokal','Fossum'])
	tarantula = list(data['Tarantula'])
	zoltar = list(data['Zoltar'])
	sokal = list(data['Sokal'])
	fossum = list(data['Fossum'])
	with open('./output.csv','r') as fp:
		reader = csv.DictReader(fp)
		index = [row[''] for row in reader]
	
	for list_name in ['tarantula','zoltar','sokal','fossum']:
		fig = plt.figure(figsize=(12,6),dpi=100)
		plt.bar(range(len(index[:50])),eval("{}[:50]".format(list_name)))
		plt.xticks(range(len(index[:50])),index[:50])
		plt.title(list_name)
	plt.show()

if __name__ == "__main__":
	# extract execution info of lines
	for fname in os.listdir("./gcov-res"):
		with open("./gcov-res/{}".format(fname), "r") as f:
			update_global(stat_exec(f), int(fname[:-5]) in passed_test)
	generator_csv()
	draw_bar()
	# TODO: Start From param calculate
