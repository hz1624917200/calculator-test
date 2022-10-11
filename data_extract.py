
from io import TextIOWrapper
import os
import re
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib
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

def draw_bar(filename):
	data = pd.read_csv(filename,usecols=['Tarantula','Zoltar','Sokal','Fossum'])
	tarantula = list(data['Tarantula'])
	zoltar = list(data['Zoltar'])
	sokal = list(data['Sokal'])
	fossum = list(data['Fossum'])
	with open(filename,'r') as fp:
		reader = csv.DictReader(fp)
		index = [row[''] for row in reader]

	
	for list_name in ['tarantula','zoltar','sokal','fossum']:
		fig = plt.figure(figsize=(12,6),dpi=100)
		plt.bar(range(len(index)),eval("{}".format(list_name)))
		plt.xticks(range(len(index)),index)
		plt.title(list_name)
	plt.show()

def draw_top10(filename,algorithm):
	data = pd.read_csv(filename,usecols=['Tarantula','Zoltar','Sokal','Fossum'])
	tarantula = data.sort_values('Tarantula',ascending=False)['Tarantula']
	zoltar = data.sort_values('Zoltar',ascending=False)['Zoltar']
	sokal = data.sort_values('Sokal',ascending=False)['Sokal']
	fossum = data.sort_values('Fossum',ascending=False)['Fossum']
	print(eval(algorithm)[:10])

if __name__ == "__main__":
	# extract execution info of lines
	for fname in os.listdir("./gcov-res"):
		with open("./gcov-res/{}".format(fname), "r") as f:
			update_global(stat_exec(f), int(fname[:-5]) in passed_test)
	generator_csv()
	draw_bar('output-success.csv')
	draw_top10('output-success.csv','tarantula')
	# TODO: Start From param calculate
