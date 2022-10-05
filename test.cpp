#include <iostream>
#include <string>

int main() {
	std::string s = ".123456.321";
	long double a = std::stold(s);
	printf("%Lf;", 1e-8L);
	return 0;
}