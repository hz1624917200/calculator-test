import subprocess
import os

PRECISION = 1e-6
def equal(a: float, b: float) -> bool:
	if abs(a - b) < PRECISION:
		return True
	return False


if __name__ == "__main__":
	correct_list = []
	# clean
	if not os.path.exists('./gcov-res'):
		os.mkdir('./gcov-res')
	else:
		os.system("/usr/bin/rm ./gcov-res/*")
	
	file_cnt = 0
	for infile in os.listdir("./testcase"):
		file_cnt += 1
		ind = infile[:-3]
		# infile is standalone filename

		# execute exp group
		proc = subprocess.Popen(
			["./calculator", "testcase/{}".format(infile)],
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
		)
		res_exp = proc.stdout.readline().decode("utf-8")

		# execute control group
		proc = subprocess.Popen(
			["./calculator-ctrl", "testcase/{}".format(infile)],
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
		)
		res_ctrl = proc.stdout.readline().decode("utf-8")

		# validate
		if res_exp == res_ctrl:
			print("{} Passed".format(infile))
			correct_list.append(int(ind))
		else:
			print(infile)
			print("res: {}\nans: {}".format(res_exp, res_ctrl))
	
		os.system("llvm-cov-12 gcov -f -b calculator.gcda > /dev/null")
		os.system("/usr/bin/rm calculator.gcda")
		os.system("mv calculator.cpp.gcov gcov-res/{}.gcov".format(ind))
	
	# end
	correct_cnt = len(correct_list)
	print("Test Summary:\npassed {} in {} cases, {:.2f}%".format(correct_cnt, file_cnt, correct_cnt / file_cnt * 100))
	os.system("/usr/bin/rm *.gcov") 
	# os.remove("*.gcov")
	with open("correct_list.txt", "w") as f:
		f.write(str(correct_list))
