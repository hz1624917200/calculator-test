#include <vector>
#include <stack>
#include <numeric>
#include <map>
#include <string>
#include <set>
#include <unordered_set>
#include <iostream>

#define FATAL printf
#define precision 1e-8L
#define MAX_EXPR_LENGTH 100

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

// power, return a ^ b
long double power(long double a, long double b);
// extract root
// return: squre root if b == 2; cube root if b == 3
long double root(long double a, long double b);


int main(int argc, char *argv[])
{
	//parseExpression("1.23_2*3+.2yz*(2^(4- 3)/1.5)x");
	std::string expr;
	if (argc != 2) {
		FATAL("Usage: calculator input_file");
		exit(-1);
	}

	freopen(argv[1], "r", stdin);
	std::getline(std::cin, expr);
	parseExpression(expr);
	// parseExpression("1.23*3+.2yz*(2+(4- 3)/1.5)x");
	// parseExpression("x_z");
	updateVarMap();
	printf("result is: %Lf\n", solve());
	// printf("%d\n", var.size());
	return 0;
}

void parseExpression(std::string expression)
{
	std::set<char> validop = { '!', '+', '-', '*', '/', '^', '_', '>', '=', '<', '&', '|', '(', ')' };     // valid operator
	std::stack<char> opstack;
	bool skip_num = false, has_point = false, auto_mut = false, valid_neg = true;

	for (int i = 0; i < expression.length(); i++) {
		char cur = expression[i];
		if (isblank(cur)) continue;
		if ((isdigit(cur) || cur == '.') && skip_num) {			// skip number
			if (cur == '.') {
				if (has_point) {
					FATAL("Error: extra digital point at %d\n", i);
					exit(-1);
				}
				else {
					has_point = true;
				}
			}
			continue;
		}
		has_point = false;
		skip_num = false;
		if (isdigit(cur) || cur == '.' || (cur == '-' && valid_neg)) {     // operand (immediate)
			if (auto_mut)	// add auto multiply
				push_op('*', opstack);
			immSequence.push_back(std::stold(expression.substr(i)));
			commandSequence.push_back('i');
			if (cur == '.')
				has_point = true;
			skip_num = true;
			auto_mut = true;
			valid_neg = false;
		}
		else if (validop.count(cur)) {  // valid operator
			if (cur == '(') {
				if (auto_mut)	// add auto multiply
					push_op('*', opstack);
				opstack.push(cur);
				auto_mut = false;
				valid_neg = true;
				continue;
			}
			if (cur == ')') {
				while (!opstack.empty() && opstack.top() != '(') {
					commandSequence.push_back(opstack.top());
					opstack.pop();
				}
				if (opstack.empty()) {
					FATAL("Error: unpaired bracket ')' at %d\n", i);
					exit(-1);
				}
				opstack.pop();
				auto_mut = true;
			}
			else {
				push_op(cur, opstack);
				auto_mut = false;
				valid_neg = true;
			}
		}
		else if (isalpha(cur)) {	// variants
			if (auto_mut)	// add auto multiply
				push_op('*', opstack);
			var[cur] = 0;
			varSequence.push_back(cur);
			commandSequence.push_back('v');
			auto_mut = true;
			valid_neg = false;
		}
		else {
			FATAL("Error: invalid character '%c' at %d\n", cur, i);
			exit(-1);
		}
	}
	while (!opstack.empty()) {
		if (opstack.top() == '(') {
			FATAL("Error: unpaired bracket '('\n");
			exit(-1);
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
		FATAL("opstk size check failed\n");
		exit(-1);
	}
	return (opstk.top());
fail_dataseq:
	FATAL("opdata size check failed\n");
	exit(-1);
fail_opstk:
	FATAL("opstk underflow detected\n");
	exit(-1);
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
	exit(-1);
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
			FATAL("divided by 0\n");
			exit(-1);
		}
		return (a / b);
	case '^':
		return power(a, b);
	case '_':
		return root(a, b);
	}
	FATAL("invalid OP %c\n", op);
	exit(-1);
}

long double calc(long double x, char op)
{
	switch (op)
	{
	case '!':
		return (!x);
	}
	FATAL("invalid OP %c\n", op);
	exit(-1);
}

void updateVarMap()
{
	for (auto &[k, v]: var) {
		// printf("value of %c: ", k);
		scanf("%Lf", &v);
	}
}

long double power(long double base, long double initPower)
{
	long double result = 1;
    long long nowPower = (long long)initPower;
	int isNegative = 0;
	if(nowPower != initPower)
	{
		FATAL("Error: exponent cannot be decimal\n");
		exit(-1);
	}
	if(nowPower < 0)
    {
        isNegative = 1;
        nowPower = -nowPower;
    }
    while (nowPower > 0) 
	{
        if (nowPower & 1)
        {
            result = result * base ;
        }
        nowPower >>= 1;
        base = base * base;
    }
	if(isNegative == 1)
    {
        result = 1 / result;
    }
    return result;
}

long double root(long double base, long double initPower)
{
	long double i = base / 2;
    long long nowPower = (long long)initPower;
	int isNegative = 0;
	if(nowPower != initPower)
	{
		FATAL("Error: exponent cannot be decimal\n");
		exit(-1);
	}
	if((base < 0) && (nowPower % 2 == 0))
	{
		FATAL("Error: base cannot be negative when exponent is even\n");
		exit(-1);
	}
	if(nowPower < 0)
    {
        isNegative = 1;
        nowPower = -nowPower;
		initPower = -initPower;
	}
    while (!equal(power(i,initPower),base))
    {
        i = i - ((power(i,initPower) - base) / (nowPower * power(i,initPower - 1)));
    }
    if(isNegative == 1)
    {
        i = 1 / i;
    }
    return i;
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