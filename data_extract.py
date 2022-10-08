from io import TextIOWrapper
import os
import re
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
			



if __name__ == "__main__":
	# extract execution info of lines
	for fname in os.listdir("./gcov-res"):
		with open("./gcov-res/{}".format(fname), "r") as f:
			update_global(stat_exec(f), int(fname[:-5]) in passed_test)
	
	# TODO: Start From param calculate