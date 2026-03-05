import random
import math
import cmath

# 函数用于生成垂直渐近线问题及答案
def generate_vertical_asymptote_problem():
    # 随机生成二次方程的系数
    a = random.randint(1, 5)
    b = random.randint(-10, 10)
    c = random.randint(-20, 20)
    denominator = f"{a}x^2 + {b}x + {c}"
    problem = f"How many vertical asymptotes does the graph of $y = \\frac{2}{ {denominator} }$ have?"
    # 计算判别式判断根的情况
    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        answer = 0
    elif discriminant == 0:
        answer = 1
    else:
        answer = 2
    return problem, answer

# 函数用于生成百分比差值问题及答案
def generate_percentage_difference_problem():
    num1 = random.randint(10, 50)
    num2 = random.randint(10, 50)
    percent1 = random.randint(110, 150)
    percent2 = random.randint(110, 150)
    problem = f"What is the positive difference between {percent1}% of {num1} and {percent2}% of {num2}?"
    value1 = num1 * (percent1 / 100)
    value2 = num2 * (percent2 / 100)
    answer = abs(value1 - value2)
    return problem, answer

# 函数用于生成关于天花板函数的问题及答案
def generate_ceiling_function_problem():
    numerator = random.randint(20, 30)
    denominator = random.randint(3, 7)
    fraction = f"\\frac{{{numerator}}}{{{denominator}}}"
    problem = f"Find $x$ such that $\\lceil x \\rceil + x = {fraction}$. Express $x$ as a common fraction."
    # 设 x = n + r，n 为整数部分，0 <= r < 1
    total = numerator / denominator
    n = math.floor((total - 1) / 2)
    r = total - 2 * n - 1
    answer = f"{int((n + r) * denominator)}/{denominator}"
    return problem, answer

# 函数用于生成复数幂运算问题及答案
def generate_complex_power_problem():
    power1 = random.randint(5, 15)
    power2 = random.randint(-30, -15)
    power3 = random.randint(40, 50)
    problem = f"Evaluate $i^{ {power1} }+i^{ {power2} }+i^{ {power3} }$."
    def power_of_i(p):
        remainder = p % 4
        if remainder == 0:
            return 1
        elif remainder == 1:
            return 1j
        elif remainder == 2:
            return -1
        elif remainder == 3:
            return -1j

    result = power_of_i(power1) + power_of_i(power2) + power_of_i(power3)
    if result.imag == 0:
        answer = str(int(result.real))
    elif result.real == 0:
        answer = f"{int(result.imag)}i"
    else:
        answer = f"{int(result.real)}+{int(result.imag)}i"
    return problem, answer

# 函数用于生成指数方程问题及答案
def generate_exponential_equation_problem():
    base = random.randint(2, 5)
    power = random.randint(6, 10)
    new_base = base ** 2
    problem = f"If ${base}^{ {power} } = {new_base}^x$, what is the value of $x$?"
    answer = power / 2
    return problem, answer

# 函数用于生成等差数列问题及答案
def generate_arithmetic_sequence_problem():
    first_term = random.randint(2, 10)
    common_difference = random.randint(2, 6)
    term_number = random.randint(80, 120)
    problem = f"What is the {term_number}th term of the arithmetic sequence {first_term}, {first_term + common_difference}, {first_term + 2 * common_difference}, {first_term + 3 * common_difference}, ...?"
    answer = first_term + (term_number - 1) * common_difference
    return problem, answer

# 函数用于生成二次不等式问题及答案
def generate_quadratic_inequality_problem():
    a = random.randint(1, 3)
    b = random.randint(-10, 10)
    c = random.randint(-20, 20)
    constant = random.randint(5, 15)
    quadratic = f"{a}x^2 + {b}x + {c}"
    problem = f"For what values of $x$ is it true that ${quadratic} \\le {constant}$? Express your answer in interval notation."
    new_c = c - constant
    discriminant = b ** 2 - 4 * a * new_c
    if discriminant < 0:
        if a > 0:
            answer = "No solution"
        else:
            answer = "(-∞, +∞)"
    elif discriminant == 0:
        root = -b / (2 * a)
        if a > 0:
            answer = f"[{root}, {root}]"
        else:
            answer = "(-∞, +∞)"
    else:
        root1 = (-b - math.sqrt(discriminant)) / (2 * a)
        root2 = (-b + math.sqrt(discriminant)) / (2 * a)
        if a > 0:
            answer = f"[{min(root1, root2)}, {max(root1, root2)}]"
        else:
            answer = f"(-∞, {min(root1, root2)}] ∪ [{max(root1, root2)}, +∞)"
    return problem, answer

# 函数用于生成复利问题及答案
def generate_compound_interest_problem():
    principal = random.randint(500, 2000)
    amount = random.randint(principal + 200, principal + 1000)
    years = random.randint(2, 5)
    problem = f"Mr. Smith invests {principal} dollars in a fund that compounds annually at a constant interest rate. After {years} years, his investment has grown to {amount} dollars. What is the annual interest rate, as a percentage? (Round your answer to the nearest integer.)"
    rate = ((amount / principal) ** (1 / years) - 1) * 100
    answer = round(rate)
    return problem, answer

# 函数用于生成整数配对求和问题及答案
def generate_integer_pair_sums_problem():
    sums = sorted([random.randint(10, 30) for _ in range(6)])
    problem = f"Four distinct integers $a$, $b$, $c$ and $d$ have the property that when added in pairs, the sums {', '.join(map(str, sums))} are obtained. What are the four integers in increasing order? (place a comma and then a space between each integer)"
    # 假设 a < b < c < d，则 a + b 最小，c + d 最大
    a_plus_b = sums[0]
    c_plus_d = sums[5]
    a_plus_c = sums[1]
    b_plus_d = sums[4]
    total = (a_plus_b + c_plus_d)
    d = total - a_plus_b - a_plus_c + sums[2]
    c = c_plus_d - d
    b = b_plus_d - d
    a = a_plus_b - b
    answer = f"{a}, {b}, {c}, {d}"
    return problem, answer

# 函数用于生成绝对值方程问题及答案
def generate_absolute_value_equation_problem():
    a = random.randint(3, 7)
    b = random.randint(1, 5)
    c = random.randint(2, 6)
    d = random.randint(1, 4)
    left = f"{a}x - {b}"
    right = f"{c}x + {d}"
    problem = f"What is the smallest value of $x$ such that $|{left}| = |{right}|$? Express your answer as a common fraction."
    # 分两种情况求解
    case1 = (b + d) / (a - c) if a != c else float('inf')
    case2 = (b - d) / (a + c)
    answer = min(case1, case2)
    if answer.is_integer():
        answer = str(int(answer))
    else:
        answer = f"{answer:.2f}"
    return problem, answer

# 函数用于生成函数复合与反函数问题及答案
def generate_function_composition_inverse_problem():
    f_coefficient = random.randint(3, 9)
    f_constant = random.randint(1, 5)
    g_coefficient = random.randint(1, 3)
    g_constant = random.randint(-3, 3)
    f_function = f"{f_coefficient}x + {f_constant}"
    g_function = f"{g_coefficient}x + {g_constant}"
    problem = f"Let $f(x) = {f_function}$ and $g(x) = {g_function}$. If $h(x)=f(g(x))$, then what is the inverse of $h(x)$?"
    # 先求 h(x)，再求其反函数
    h_coefficient = f_coefficient * g_coefficient
    h_constant = f_coefficient * g_constant + f_constant
    answer = f"(x - {h_constant}) / {h_coefficient}"
    return problem, answer

# 函数用于生成绝对值不等式问题及答案
def generate_absolute_value_inequality_problem():
    a = random.randint(5, 10)
    b = random.randint(1, 5)
    c = random.randint(3, 7)
    d = random.randint(1, 4)
    left_inequality = f"|{a}x - {b}| > {c}"
    right_inequality = f"|{a}x + {d}| \\le {c}"
    problem = f"Find the sum of all integers that satisfy these conditions: \\[ {left_inequality} \\text{{ and }} {right_inequality} \\]"
    left_solutions1 = []
    left_solutions2 = []
    right_solutions = []
    if a > 0:
        left_solutions1 = [i for i in range(math.ceil((b + c) / a), 100) if isinstance(i, int)]
        left_solutions2 = [i for i in range(-100, math.floor((b - c) / a) + 1) if isinstance(i, int)]
        right_solutions = [i for i in range(math.ceil((-c - d) / a), math.floor((c - d) / a) + 1) if isinstance(i, int)]
    all_left_solutions = left_solutions1 + left_solutions2
    common_solutions = [i for i in all_left_solutions if i in right_solutions]
    answer = sum(common_solutions)
    return problem, answer

# 函数用于生成距离公式问题及答案
def generate_distance_formula_problem():
    x = random.randint(-10, -1)
    y = random.randint(1, 10)
    point = f"({x},{y})"
    problem = f"What is the number of units in the distance from the origin to the point {point} in a coordinate system?"
    answer = math.sqrt(x ** 2 + y ** 2)
    return problem, answer

# 函数用于生成中点坐标问题及答案
def generate_midpoint_problem():
    x1 = random.randint(1, 5)
    y1 = random.randint(2, 8)
    x2 = random.randint(6, 10)
    y2 = random.randint(9, 15)
    point1 = f"({x1},{y1})"
    point2 = f"({x2},{y2})"
    problem = f"The two endpoints of a segment are at {point1} and {point2}. What is the sum of the coordinates of the midpoint of the segment?"
    midpoint_x = (x1 + x2) / 2
    midpoint_y = (y1 + y2) / 2
    answer = midpoint_x + midpoint_y
    return problem, answer

# 函数用于生成风筝面积问题及答案
def generate_kite_area_problem():
    a_x = random.randint(0, 5)
    a_y = random.randint(5, 10)
    b_x = random.randint(1, 6)
    b_y = random.randint(0, 3)
    c_x = random.randint(8, 15)
    c_y = random.randint(-5, -1)
    d_x = random.randint(6, 12)
    d_y = random.randint(6, 10)
    a = f"({a_x},{a_y})"
    b = f"({b_x},{b_y})"
    c = f"({c_x},{c_y})"
    d = f"({d_x},{d_y})"
    problem = f"Kite $ABCD$ (a quadrilateral with two pairs of adjacent equal sides) has coordinates $A\\ {a},\\ B\\ {b},\\ C\\ {c},$ and $D\\ {d}.$ What is the area of $ABCD,$ given that the area of a kite is equal to half the product of its diagonals?"
    # 计算对角线长度
    diagonal1 = math.sqrt((a_x - c_x) ** 2 + (a_y - c_y) ** 2)
    diagonal2 = math.sqrt((b_x - d_x) ** 2 + (b_y - d_y) ** 2)
    answer = 0.5 * diagonal1 * diagonal2
    return problem, answer

# 生成问题的函数列表
problem_generators = [
    generate_vertical_asymptote_problem,
    generate_percentage_difference_problem,
    generate_ceiling_function_problem,
    generate_complex_power_problem,
    generate_exponential_equation_problem,
    generate_arithmetic_sequence_problem,
    generate_quadratic_inequality_problem,
    generate_compound_interest_problem,
    generate_integer_pair_sums_problem,
    generate_absolute_value_equation_problem,
    generate_function_composition_inverse_problem,
    generate_absolute_value_inequality_problem,
    generate_distance_formula_problem,
    generate_midpoint_problem,
    generate_kite_area_problem
]

# 生成指定数量的问题及答案
def generate_problems(num_problems):
    problems_and_answers = []
    for _ in range(num_problems):
        # 随机选择一个问题生成函数
        generator = random.choice(problem_generators)
        problem, answer = generator()
        problems_and_answers.append((problem, answer))
    return problems_and_answers

# 示例：生成10个问题及答案
generated_problems = generate_problems(10)
for i, (problem, answer) in enumerate(generated_problems, 1):
    print(f"Problem {i}: {problem}")
    print(f"Answer {i}: {answer}")
    print()
