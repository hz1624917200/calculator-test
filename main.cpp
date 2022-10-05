#include <vector>
#include <stack>
#include <numeric>
#include <map>
#include <string>
#include <set>
#include <unordered_set>

#define FATAL printf
#define precision 1e-8L

// Commands:
// Math op: +-*/^_~		^: power; _: extract root
// Comparison >=<
// Logical op: &|!
// load op: var: v; immediate: i;
//
std::vector<char> commandSequence;
// immediate sequence
std::vector<long double> immSequence;
// variable symbol sequence
std::vector<char> varSequence;
// variable value map
std::map<char, long double> var;

// check whether operator is unary
bool isUnary(char op);
// binary operator calculate
long double calc(long double a, long double b, char op);
// Unary operator calculate
long double calc(long double x, char op);
// operator priority. the larger, the higher
int priority(char op);
// push operator by priority
void push_op(char op, std::stack<char> &opstack);
// parse expression to command sequence 
void parseExpression(std::string expression);
// update variables
void updateVarMap();
long double solve();

bool equal(long double a, long double b);

// TODO !!!!!!!
// power, return a ^ b
long double power(long double a, long double b);
// extract root
// return: squre root if b == 2; cube root if b == 3
long double root(long double a, long double b);


int main()
{
	//parseExpression("1.23_2*3+.2yz*(2^(4- 3)/1.5)x");
	parseExpression("1.23*3+.2yz*(2+(4- 3)/1.5)x");
	updateVarMap();
	printf("result is: %Lf\n", solve());
	// printf("%d\n", var.size());
	return 0;
}

void parseExpression(std::string expression)
{
	std::set<char> validop = { '!', '+', '-', '*', '/', '^', '_', '>', '=', '<', '&', '|', '(', ')' };     // valid operator
	std::stack<char> opstack;
	bool skip_num, has_point, auto_mut = false;

	for (int i = 0; i < expression.length(); i++) {
		char cur = expression[i];
		if (isblank(cur)) continue;
		if ((isdigit(cur) || cur == '.') && skip_num) {			// skip number
			if (cur == '.') {
				if (has_point) {
					FATAL("Error: extra digital point at %d\n", i);
					return;
				}
				else {
					has_point = true;
				}
			}
			continue;
		}
		has_point = false;
		skip_num = false;
		if (isdigit(cur) || cur == '.') {     // operand (immediate)
			if (auto_mut)	// add auto multiply
				push_op('*', opstack);
			immSequence.push_back(std::stold(expression.substr(i)));
			commandSequence.push_back('i');
			if (cur == '.')
				has_point = true;
			skip_num = true;
			auto_mut = true;
		}
		else if (validop.count(cur)) {  // valid operator
			if (cur == '(') {
				if (auto_mut)	// add auto multiply
					push_op('*', opstack);
				opstack.push(cur);
				auto_mut = false;
				continue;
			}
			if (cur == ')') {
				while (!opstack.empty() && opstack.top() != '(') {
					commandSequence.push_back(opstack.top());
					opstack.pop();
				}
				if (opstack.empty()) {
					FATAL("Error: unpaired bracket ')' at %d\n", i);
					return;
				}
				opstack.pop();
				auto_mut = true;
			}
			else {
				push_op(cur, opstack);
				auto_mut = false;
			}
		}
		else if (isalpha(cur)) {	// variants
			if (auto_mut)	// add auto multiply
				push_op('*', opstack);
			var[cur] = 0;
			varSequence.push_back(cur);
			commandSequence.push_back('v');
			auto_mut = true;
		}
		else {
			FATAL("Error: invalid character '%c' at %d\n", cur, i);
			return;
		}
	}
	while (!opstack.empty()) {
		if (opstack.top() == '(') {
			FATAL("Error: unpaired bracket '('\n");
			return;
		}
		commandSequence.push_back(opstack.top());
		opstack.pop();
	}
}

void push_op(char op, std::stack<char> &opstack)
{
	int cur_priority = priority(op);
	while (!opstack.empty() && priority(opstack.top()) >= cur_priority) {
		commandSequence.push_back(opstack.top());
		opstack.pop();
	}
	opstack.push(op);
}

long double solve()
{
	std::stack<long double> opstk{};
	auto imm_iter = immSequence.begin();
	auto var_iter = varSequence.begin();
	long double a = 0, b = 0;
	for (auto op: commandSequence) {
		switch (op)
		{
		case 'i':
			if (imm_iter == immSequence.end()) goto fail_dataseq;
			opstk.push(*(imm_iter++));
			break;
		case 'v':
			if (var_iter == varSequence.end()) goto fail_dataseq;
			opstk.push(var[*(var_iter++)]);
			break;
		default:
			if (isUnary(op)) {
				if (opstk.empty())
					goto fail_opstk;
				a = opstk.top();
				opstk.pop();
				opstk.push(calc(a, op));
			}
			else {
				if (opstk.size() < 2)
					goto fail_opstk;
				b = opstk.top();
				opstk.pop();
				a = opstk.top();
				opstk.pop();
				opstk.push(calc(a, b, op));
			}
		}
	}
	if (opstk.size() != 1) {
		FATAL("opstk size check failed");
		return -1;
	}
	return (opstk.top());
fail_dataseq:
	FATAL("opdata size check failed");
	return -1;
fail_opstk:
	FATAL("opstk underflow detected");
	return -1;
}

int priority(char op)
{
	switch (op)
	{
	case '(':
		return -1;
	case '|':
		return 1;
	case '&':
		return 2;
	case '=':
	case '<':
	case '>':
		return 3;
	case '+':
	case '-':
		return 4;
	case '*':
	case '/':
		return 5;
	case '^':
	case '_':
		return 6;
	case '!':
		return 7;
	}
	FATAL("Invalid op priority: %c\n", op);
	return 0;
}

long double calc(long double a, long double b, char op)
{
	switch (op)
	{
	case '&':
		return (a && b);
	case '|':
		return (a || b);
	case '=':
		return (equal(a, b));
	case '>':
		return (a > b);
	case '<':
		return (a < b);
	case '+':
		return (a + b);
	case '-':
		return (a - b);
	case '*':
		return (a * b);
	case '/':
		if (equal(b, 0)) {
			FATAL("divided by 0");
			return -1;
		}
		return (a / b);
	case '^':
		return power(a, b);
	case '_':
		return root(a, b);
	}
	FATAL("invalid OP %c\n", op);
	return 0;
}

long double calc(long double x, char op)
{
	switch (op)
	{
	case '!':
		return (!x);
	}
	FATAL("invalid OP %c\n", op);
	return 0;
}

void updateVarMap()
{
	for (auto &[k, v]: var) {
		printf("value of %c: ", k);
		scanf("%Lf", &v);
	}
}

long double power(long double a, long double b)
{
	return 0;
}

long double root(long double a, long double b)
{
	return 0;
}

inline bool isUnary(char op)
{
	const static std::unordered_set<char> unary_op {'!'};

	if (unary_op.count(op))
		return true;
	return false;
}

inline bool equal(long double a, long double b)
{
	if (((a - b) < precision) && ((b - a) < precision))
		return true;
	return false;
}