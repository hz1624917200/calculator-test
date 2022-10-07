#include <iostream>
#include <string>

int main() {
	std::string s = "5.123456e+6";
	long double a = std::stold(s);
	printf("%lld", (long long)a);
	return 0;
}