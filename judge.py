import subprocess
import os
from validate import calc

if __name__ == "__main__":
	for infile in os.listdir("./testcase"):
		# infile is standalone filename

		# execute 
		proc = subprocess.Popen(
			["./calculator", "testcase/{}".format(infile)],
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
		)
		print(infile, proc.stdout.readline().decode("utf-8"))

		# validate
		ans = calc(infile)
		print(infile, "validate:", ans)
