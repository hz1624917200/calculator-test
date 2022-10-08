from asyncore import write
import subprocess
import os
from validate import calc

PRECISION = 1e-6
def equal(a: float, b: float) -> bool:
	if abs(a - b) < PRECISION:
		return True
	return False


if __name__ == "__main__":
	valid_ind = 0
	correct_list = []
	# clean
	if not os.path.exists('./gcov-res'):
		os.mkdir('./gcov-res')
	else:
		os.system("/usr/bin/rm ./gcov-res/*")
	for infile in os.listdir("./testcase"):
		# infile is standalone filename
		# print(infile)
		# execute 
		proc = subprocess.Popen(
			["./calculator", "testcase/{}".format(infile)],
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
		)
		# print(proc.stdout.readline().decode("utf-8"), end='')
		res = proc.stdout.readline().decode("utf-8")


		# validate
		ans = calc(infile)
		# print("validate:", ans)

		valid = True
		correct = True
		if ans[0].isdigit() or ans[1].isdigit():	# no error occured
			# print(ans, res[11:])
			if len(res) > 7 and res[:6] == "result":
				res = eval(res[11:])
				ans = eval(ans)
				if equal(res, ans):
					# print("{} Passed".format(infile))
					correct = True
				else:
					correct = False
			else:
				correct = False
		else:
			valid = False
		if not correct:
			print(infile)
			print("res: {}\nans: {}".format(res, ans))
	
		if valid:
			os.system("llvm-cov-12 gcov -f -b calculator.gcda > /dev/null")
			os.system("/usr/bin/rm calculator.gcda")
			os.system("mv calculator.cpp.gcov gcov-res/{}.gcov".format(valid_ind))
			if correct:
				correct_list.append(valid_ind)
			valid_ind += 1
	
	# end
	correct_cnt = len(correct_list)
	print("Test Summary:\npassed {} in {} cases, {:.2f}%".format(correct_cnt, valid_ind + 1, correct_cnt / (valid_ind + 1) * 100))
	os.system("/usr/bin/rm *.gcov") 
	# os.remove("*.gcov")
	with open("correct_list.txt", "w") as f:
		f.write(str(correct_list))
