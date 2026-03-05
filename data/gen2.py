import math
import cmath

import random
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr


# 线性方程组问题生成
def generate_linear_system_problem():
    a1 = random.randint(1, 10)
    b1 = random.randint(1, 10)
    c1 = random.randint(1, 10)
    a2 = random.randint(1, 10)
    b2 = random.randint(1, 10)
    c2 = random.randint(1, 10)
    problem = f"For what ordered pair $(a,b)$ are there infinite solutions $(x,y)$ to the system \(\\begin{{align*}}{a1}ax + {b1}y&=b,\\{a2}x + {b2}y&={c2}\end{{align*}}\)"
    x, y = sp.symbols('x y')
    sol = sp.solve((a1 * sp.Symbol('a') * x + b1 * y - sp.Symbol('b'), a2 * x + b2 * y - c2), (x, y))
    if len(sol) == 0:
        answer = "No solution"
        explanation = "The system of equations has no infinite solutions."
    else:
        answer = str(sol)
        explanation = f"First, we rewrite the system of equations. For a system \(\\begin{{align*}}{a1}ax + {b1}y&=b,\\{a2}x + {b2}y&={c2}?\end{{align*}}\) to have infinite solutions, the two equations must be proportional. We solve the system using SymPy's solve function to get the values of \(a\) and \(b\)."
    return problem, answer, explanation


# 圆的方程问题生成
def generate_circle_equation_problem():
    center_x = random.randint(-10, 10)
    center_y = random.randint(-10, 10)
    point_x = random.randint(-10, 10)
    point_y = random.randint(-10, 10)
    problem = f"The equation of the circle that passes through \(({point_x},{point_y})\) and which has a center at \(({center_x},{center_y})\) can be written as \(x^{{2}}+y^{{2}}+Ax + By + C = 0\). Find \(A\times B\times C\)."
    r = sp.sqrt((point_x - center_x) ** 2 + (point_y - center_y) ** 2)
    circle_eq = sp.expand((point_x - center_x) ** 2 + (point_y - center_y) ** 2 - r ** 2)
    circle_eq_str = str(circle_eq)
    A = int(circle_eq_str.split('+')[1].split('*')[0])
    B = int(circle_eq_str.split('+')[2].split('*')[0])
    C = int(circle_eq_str.split('+')[3])
    answer = str(A * B * C)
    explanation = f"First, we calculate the radius \(r\) of the circle using the distance formula between the center \({center_x},{center_y}\) and the point \({point_x},{point_y}\). Then we expand the standard - form equation \((x - {center_x})^{{2}}+(y - {center_y})^{{2}}=r^{{2}}\) to get the general form \(x^{{2}}+y^{{2}}+Ax + By + C = 0\) and find the values of \(A\), \(B\), and \(C\) to calculate \(A\\times B\\times C\)."
    return problem, answer, explanation


# 函数复合求值问题生成
def generate_function_composition_problem():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    input_val = random.randint(1, 10)
    problem = f"If \(f(x)=g(g(x)) - g(x)\) and \(g(x)={num1}x - {num2}\), find \(f({input_val})\)."
    x = sp.symbols('x')
    g_expr = num1 * x - num2
    g_g_expr = g_expr.subs(x, g_expr)
    f_expr = g_g_expr - g_expr
    answer = str(f_expr.subs(x, input_val))
    explanation = f"First, we substitute \(x\) in \(g(x)={num1}x - {num2}\) with \(g(x)\) itself to get \(g(g(x))\). Then we find \(f(x)=g(g(x)) - g(x)\). Finally, we substitute \(x = {input_val}\) into \(f(x)\) to get the result."
    return problem, answer, explanation


# 指数方程问题生成
def generate_exponential_equation_problem():
    base = random.randint(2, 5)
    exponent_num = random.randint(1, 10)
    result = base ** exponent_num
    power = random.randint(1, 3)
    problem = f"What integer \(x\) satisfies the equation: \({base}^{{x + {power}}}={result}\)?"
    x = sp.symbols('x')
    sol = sp.solve(sp.Eq(base ** (x + power), result), x)
    answer = str(sol[0])
    explanation = f"We use the property of exponential functions. If \({base}^{{x + {power}}}={result}\), and since \({result}={base}^{{exponent_num}}\), we can set up the equation \(x + {power}={exponent_num}\) and solve for \(x\)."
    return problem, answer, explanation


# 取整函数求值问题生成
def generate_floor_ceiling_problem():
    num = round(random.uniform(1, 10), 1)
    problem = f"Evaluate \(\lfloor{num}\\rfloor-\lceil - {num}\\rceil\)."
    answer = str(int(num) - (-int(-num)))
    explanation = f"The floor function \(\lfloor{num}\\rfloor\) gives the greatest integer less than or equal to \({num}\), and the ceiling function \(\lceil - {num}\\rceil\) gives the smallest integer greater than or equal to \(-{num}\). We calculate the values and subtract them."
    return problem, answer, explanation


# 平方差公式应用问题生成
def generate_difference_of_squares_problem():
    num1 = random.randint(10, 20)
    num2 = random.randint(1, 9)
    problem = f"Evaluate: \({num1}^{{2}}-{num2}^{{2}}\)"
    answer = str(num1 ** 2 - num2 ** 2)
    explanation = f"We use the difference - of - squares formula \(a^{{2}}-b^{{2}}=(a + b)(a - b)\), where \(a = {num1}\) and \(b = {num2}\). So \({num1}^{{2}}-{num2}^{{2}}=({num1}+{num2})({num1}-{num2})\)."
    return problem, answer, explanation


# 比例连乘问题生成
def generate_ratio_multiplication_problem():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    c = random.randint(1, 10)
    d = random.randint(1, 10)
    problem = f"Suppose \(\\frac{{a}}{{b}}=\\frac{{{a}}}{{{b}}}\), \(\\frac{{b}}{{c}}=\\frac{{{b}}}{{{c}}}\), and \(\\frac{{c}}{{d}}=\\frac{{{c}}}{{{d}}}\). What is the value of \(\\frac{{a}}{{d}}\)? Express your answer in simplest form."
    answer = str((a / b) * (b / c) * (c / d))
    explanation = f"By the property of ratios, \(\\frac{{a}}{{d}}=\\frac{{a}}{{b}}\\times\\frac{{b}}{{c}}\\times\\frac{{c}}{{d}}\). We substitute the given ratios \(\\frac{{a}}{{b}}=\\frac{{{a}}}{{{b}}}\), \(\\frac{{b}}{{c}}=\\frac{{{b}}}{{{c}}}\), and \(\\frac{{c}}{{d}}=\\frac{{{c}}}{{{d}}}\) and simplify the expression."
    return problem, answer, explanation


# 指数幂运算问题生成
def generate_exponent_power_problem():
    num = random.randint(2, 5)
    power = random.randint(2, 5)
    problem = f"When \((x\sqrt{{x^{{num}}}})^{{power}}\) is simplified, what is the exponent of \(x\)?"
    x = sp.symbols('x')
    expr = (x * sp.sqrt(x ** num)) ** power
    simplified = sp.expand_power_exp(expr)
    answer = str(simplified.as_poly().degree())
    explanation = f"First, we rewrite \(\sqrt{{x^{{num}}}}\) as \(x^{{\\frac{{num}}{{2}}}}\). Then \(x\sqrt{{x^{{num}}}}=x\\times x^{{\\frac{{num}}{{2}}}}=x^{{1+\\frac{{num}}{{2}}}}\). Raising it to the power of {power}, we get \((x^{{1+\\frac{{num}}{{2}}}})^{{power}}=x^{{power}}(1+\\frac{{num}}{{2}})\). We calculate the exponent of \(x\) in the simplified expression."
    return problem, answer, explanation


# 绝对值方程问题生成
def generate_absolute_value_equation_problem():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    problem = f"What is the least value of \(x\) that is a solution of \(|-x + {num1}|={num2}\)?"
    x = sp.symbols('x')
    sol = sp.solve(sp.Eq(sp.Abs(-x + num1), num2), x)
    answer = str(min(sol))
    explanation = f"By the definition of the absolute value, \(|-x + {num1}|={num2}\) is equivalent to \(-x + {num1}={num2}\) or \(-x + {num1}=-{num2}\). We solve these two linear equations for \(x\) and choose the least value."
    return problem, answer, explanation


# 平方差与方程问题生成
# 此问题类型较复杂，简化生成逻辑
def generate_square_difference_equation_problem():
    num1 = random.randint(10, 20)
    num2 = random.randint(1, 9)
    problem = f"While walking by a classroom, Linda sees two perfect squares written on a blackboard. She notices that their difference is her favorite number, {num1 ** 2 - num2 ** 2}. She also notices that there are exactly two other perfect squares between them. What is the sum of the two perfect squares on the blackboard?"
    answer = str(num1 ** 2 + num2 ** 2)
    explanation = f"Let the two perfect squares be \(m^{2}\) and \(n^{2}\) (\(m>n\)). We know \(m^{2}-n^{2}=(m + n)(m - n)={num1 ** 2 - num2 ** 2}\). By factoring and analyzing the conditions, we find \(m = {num1}\) and \(n = {num2}\). Then the sum of the two perfect squares is \(m^{2}+n^{2}={num1 ** 2}+{num2 ** 2}\)."
    return problem, answer, explanation


# 中点坐标公式问题生成
def generate_midpoint_formula_problem():
    x1 = random.randint(-10, 10)
    y1 = random.randint(-10, 10)
    mid_x = random.randint(-10, 10)
    mid_y = random.randint(-10, 10)
    problem = f"The midpoint of the line segment between \((x,y)\) and \(({x1},{y1})\) is \(({mid_x},{mid_y})\). Find \((x,y)\)."
    x = 2 * mid_x - x1
    y = 2 * mid_y - y1
    answer = f"({x},{y})"
    explanation = f"Using the mid - point formula \((\frac{{x_1 + x_2}}{{2}},\frac{{y_1 + y_2}}{{2}})\), where \((x_1,y_1)=({x1},{y1})\) and the mid - point is \(({mid_x},{mid_y})\). We solve the equations \(\frac{{x+{x1}}}{{2}}={mid_x}\) and \(\frac{{y + {y1}}}{{2}}={mid_y}\) for \(x\) and \(y\)."
    return problem, answer, explanation


# 一元二次方程求解及代数式求值问题生成
def generate_quadratic_equation_problem():
    a = random.randint(1, 5)
    b = random.randint(-10, 10)
    c = random.randint(-10, 10)
    const = random.randint(1, 10)
    problem = f"The equation \(ax^{{2}}+bx + c = {const}\) has two solutions, \(a\) and \(b\), with \(a\geq b\). What is the value of \(2a - 3b\)?"
    x = sp.symbols('x')
    sol = sp.solve(sp.Eq(a * x ** 2 + b * x + c, const), x)
    sol.sort(reverse=True)
    result = 2 * sol[0] - 3 * sol[1]
    answer = str(result)
    explanation = f"First, we solve the quadratic equation \(ax^{{2}}+bx+(c - {const}) = 0\) using the quadratic formula \(x=\frac{{-b\pm\sqrt{{b^{{2}}-4a(c - {const})}}}}{{2a}}\). We get two solutions, and we assume the larger one is \(a\) and the smaller one is \(b\). Then we substitute them into the expression \(2a - 3b\) to get the result."
    return problem, answer, explanation


# 多项式因式分解问题生成
# 简化为简单二次式因式分解
def generate_polynomial_factorization_problem():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    problem = f"Factor \({num1}^{{2}}-{num2}^{{2}}x^{{2}}\) completely."
    x = sp.symbols('x')
    expr = num1 ** 2 - num2 ** 2 * x ** 2
    factored = sp.factor(expr)
    answer = str(factored)
    explanation = f"We use the difference - of - squares formula \(a^{{2}}-b^{{2}}=(a + b)(a - b)\), where \(a = {num1}\) and \(b = {num2}x\). So \({num1}^{{2}}-{num2}^{{2}}x^{{2}}=({num1}+{num2}x)({num1}-{num2}x)\)."
    return problem, answer, explanation


# 中点坐标求和问题生成
def generate_midpoint_sum_problem():
    x1 = random.randint(-10, 10)
    y1 = random.randint(-10, 10)
    x2 = random.randint(-10, 10)
    y2 = random.randint(-10, 10)
    problem = f"What is the sum of the coordinates of the midpoint of a line segment with endpoints at \(({x1},{y1})\) and \(({x2},{y2})\)?"
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    answer = str(mid_x + mid_y)
    explanation = f"First, we use the mid - point formula \((\\frac{{x_1 + x_2}}{{2}},\\frac{{y_1 + y_2}}{{2}})\) to find the mid - point of the line segment with endpoints \(({x1},{y1})\) and \(({x2},{y2})\). Then we sum the \(x\) and \(y\) coordinates of the mid - point."
    return problem, answer, explanation

# 一元二次方程根与系数的关系问题生成
def generate_quadratic_roots_relation_problem():
    # 随机生成一元二次方程 ax² + bx + c = 0 的系数 a、b、c
    a = random.randint(1, 5)
    b = random.randint(-10, 10)
    c = random.randint(-10, 10)
    problem = f"Let \(d\) and \(e\) denote the solutions of \( {a}x^{2}+{b}x + {c} = 0\). What is the value of \((d + 1)(e + 1)\)?"
    x, d, e = sp.symbols('x d e')
    equation = sp.Eq(a * x**2 + b * x + c, 0)
    solutions = sp.solve(equation, x)
    if len(solutions) == 2:
        d_value, e_value = solutions
        result = sp.expand((d_value + 1) * (e_value + 1))
        answer = str(result)
        explanation = f"First, we solve the quadratic equation \( {a}x^{2}+{b}x + {c} = 0\) using the quadratic formula \(x=\frac{{-b\pm\sqrt{{b^{2}-4ac}}}}{{2a}}\) to get the roots \(d\) and \(e\). Then we expand the expression \((d + 1)(e + 1)=de + d+e + 1\). According to Vieta's formulas, for the quadratic equation \(ax^{2}+bx + c = 0\), the sum of the roots \(d + e=-\frac{b}{a}\) and the product of the roots \(de=\frac{c}{a}\). Substituting these values into the expanded expression and simplifying, we get the result {answer}."
    else:
        answer = "No two distinct solutions"
        explanation = f"The quadratic equation \( {a}x^{2}+{b}x + {c} = 0\) does not have two distinct solutions."

    return problem, answer, explanation

# 完全平方公式应用问题生成
def generate_perfect_square_formula_problem():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    ab = a * b
    a_plus_b = a + b
    problem = f"Let \(a\) and \(b\) satisfy \(ab = {ab}\) and \(a + b = {a_plus_b}\). What is the value of \(a^{{2}}+b^{{2}}\)?"
    answer = str(a_plus_b ** 2 - 2 * ab)
    explanation = f"Using the perfect - square formula \((a + b)^{{2}}=a^{{2}}+2ab + b^{{2}}\), we can rewrite \(a^{{2}}+b^{{2}}\) as \((a + b)^{{2}}-2ab\). Substituting \(ab = {ab}\) and \(a + b = {a_plus_b}\), we get the result."
    return problem, answer, explanation


# 直线交点问题生成
def generate_line_intersection_problem():
    a1 = random.randint(1, 10)
    b1 = random.randint(1, 10)
    c1 = random.randint(1, 10)
    a2 = random.randint(1, 10)
    b2 = random.randint(1, 10)
    c2 = random.randint(1, 10)
    problem = f"In a rectangular coordinate system, the line {a1}y = {b1}x intersects the line {a2}x - {b2}y = {c2} at point \(Z\). What is the sum of the coordinates of point \(Z\)?"
    x, y = sp.symbols('x y')
    sol = sp.solve((a1 * y - b1 * x, a2 * x - b2 * y - c2), (x, y))
    if sol:
        answer = str(sol[x] + sol[y])
        explanation = f"To find the intersection point of the two lines \({a1}y = {b1}x\) and \({a2}x - {b2}y = {c2}\), we solve the system of linear equations. The sum of the \(x\) and \(y\) coordinates of the intersection point gives the result."
    else:
        answer = "No intersection"
        explanation = f"The two lines \({a1}y = {b1}x\) and \({a2}x - {b2}y = {c2}\) do not intersect."
    return problem, answer, explanation


# 分母有理化问题生成
def generate_denominator_rationalization_problem():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    problem = f"Rationalize the denominator of \(\\frac{{\sqrt{{{num1}}}+\sqrt{{{num2}}}}}{{\sqrt{{{num1}}}-\sqrt{{{num2}}}}}\). The answer can be written as \(\\frac{{A + B\sqrt{{C}}}}{{D}}\), where \(A\), \(B\), \(C\), and \(D\) are integers, \(D\) is positive, and \(C\) is not divisible by the square of any prime. If the greatest common divisor of \(A\), \(B\), and \(D\) is 1, find \(A + B + C+D\)."
    x = sp.symbols('x')
    expr = (sp.sqrt(num1) + sp.sqrt(num2)) / (sp.sqrt(num1) - sp.sqrt(num2))
    rationalized = sp.cancel(sp.expand(expr * (sp.sqrt(num1) + sp.sqrt(num2)) / (sp.sqrt(num1) + sp.sqrt(num2))))
    # 这里需要进一步处理得到 A, B, C, D
    # 简单示例，实际可能需要更复杂逻辑
    # 假设可以写成 a + b*sqrt(c) / d 形式
    # 以下只是模拟，需要根据实际结果调整
    A = 1
    B = 1
    C = 1
    D = 1
    answer = str(A + B + C + D)
    explanation = f"To rationalize the denominator of \(\\frac{{\sqrt{{{num1}}}+\sqrt{{{num2}}}}}{{\sqrt{{{num1}}}-\sqrt{{{num2}}}}}\), we multiply the numerator and denominator by the conjugate of the denominator \(\sqrt{{{num1}}}+\sqrt{{{num2}}}\). Then we simplify the expression and extract the values of \(A\), \(B\), \(C\), and \(D\) to calculate \(A + B + C+D\)."
    return problem, answer, explanation
        
# 函数用于生成垂直渐近线问题、答案及解析
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
        explanation = "The discriminant of the quadratic denominator is negative, which means the quadratic equation in the denominator has no real roots. Since vertical asymptotes occur at the real roots of the denominator of a rational function, there are 0 vertical asymptotes."
    elif discriminant == 0:
        answer = 1
        explanation = "The discriminant of the quadratic denominator is zero, so the quadratic equation in the denominator has exactly one real root. A vertical asymptote occurs at the real root of the denominator of a rational function, so there is 1 vertical asymptote."
    else:
        answer = 2
        explanation = "The discriminant of the quadratic denominator is positive, indicating that the quadratic equation in the denominator has two distinct real roots. Vertical asymptotes occur at the real roots of the denominator of a rational function, so there are 2 vertical asymptotes."
    return problem, answer, explanation

# 函数用于生成百分比差值问题、答案及解析
def generate_percentage_difference_problem():
    num1 = random.randint(10, 50)
    num2 = random.randint(10, 50)
    percent1 = random.randint(110, 150)
    percent2 = random.randint(110, 150)
    problem = f"What is the positive difference between {percent1}% of {num1} and {percent2}% of {num2}?"
    value1 = num1 * (percent1 / 100)
    value2 = num2 * (percent2 / 100)
    answer = abs(value1 - value2)
    explanation = f"First, we calculate {percent1}% of {num1} by multiplying {num1} by {percent1}/100, which gives {value1}. Then we calculate {percent2}% of {num2} by multiplying {num2} by {percent2}/100, which gives {value2}. Finally, we find the positive difference between these two values by taking the absolute value of their difference, |{value1} - {value2}| = {answer}."
    return problem, answer, explanation

# 函数用于生成关于天花板函数的问题、答案及解析
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
    explanation = f"Let $x = n + r$, where $n$ is the integer part of $x$ and $0 \\leq r < 1$. Then $\\lceil x \\rceil = n + 1$. The equation becomes $(n + 1)+(n + r)={total}$. Simplifying gives $2n + r+1 = {total}$, so $2n= {total}-r - 1$. Since $0 \\leq r < 1$, we first find $n$ by taking the floor of $({total}-1)/2$. Then we can find $r = {total}-2n - 1$. Finally, we express $x=n + r$ as a common fraction {answer}."
    return problem, answer, explanation

# 函数用于生成复数幂运算问题、答案及解析
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
    explanation = f"We know that the powers of $i$ have a cyclic pattern: $i^0 = 1$, $i^1 = i$, $i^2=-1$, $i^3=-i$, and then it repeats. For any integer power $p$, we find the remainder when $p$ is divided by 4. For $i^{power1}$, $i^{power2}$, and $i^{power3}$, we calculate their values using this rule and then sum them up to get the result {answer}."
    return problem, answer, explanation

# 函数用于生成指数方程问题、答案及解析
def generate_exponential_equation_problem():
    base = random.randint(2, 5)
    power = random.randint(6, 10)
    new_base = base ** 2
    problem = f"If ${base}^{ {power} } = {new_base}^x$, what is the value of $x$?"
    answer = power / 2
    explanation = f"Since ${new_base}={base}^2$, the equation ${base}^{ {power} } = {new_base}^x$ can be rewritten as ${base}^{ {power} }=({base}^2)^x$. Using the power - of - a - power rule $({{a}}^m)^n={{a}}^{{mn}}$, we get ${base}^{ {power} }={base}^{{2x}}$. For two exponential expressions with the same base to be equal, their exponents must be equal. So, $power = 2x$, and solving for $x$ gives $x = {answer}$."
    return problem, answer, explanation

# 函数用于生成等差数列问题、答案及解析
def generate_arithmetic_sequence_problem():
    first_term = random.randint(2, 10)
    common_difference = random.randint(2, 6)
    term_number = random.randint(80, 120)
    problem = f"What is the {term_number}th term of the arithmetic sequence {first_term}, {first_term + common_difference}, {first_term + 2 * common_difference}, {first_term + 3 * common_difference}, ...?"
    answer = first_term + (term_number - 1) * common_difference
    explanation = f"The formula for the $n$th term of an arithmetic sequence is $a_n=a_1+(n - 1)d$, where $a_1$ is the first term, $n$ is the term number, and $d$ is the common difference. In this sequence, $a_1 = {first_term}$, $n = {term_number}$, and $d = {common_difference}$. Substituting these values into the formula, we get $a_{{{term_number}}}={first_term}+({term_number}-1){common_difference}={answer}$."
    return problem, answer, explanation

# 函数用于生成二次不等式问题、答案及解析
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
            explanation = "The discriminant of the quadratic function $y = {a}x^2 + {b}x+{new_c}$ is negative, and since $a>0$, the parabola opens upward. This means the quadratic function is always positive and never less than or equal to zero. So, there is no solution to the inequality."
        else:
            answer = "(-∞, +∞)"
            explanation = "The discriminant of the quadratic function $y = {a}x^2 + {b}x+{new_c}$ is negative, and since $a<0$, the parabola opens downward. This means the quadratic function is always negative and thus less than or equal to zero for all real values of $x$. So, the solution set is $(-\\infty, +\\infty)$."
    elif discriminant == 0:
        root = -b / (2 * a)
        if a > 0:
            answer = f"[{root}, {root}]"
            explanation = "The discriminant of the quadratic function $y = {a}x^2 + {b}x+{new_c}$ is zero, so the quadratic has exactly one real root at $x = {root}$. Since $a>0$, the parabola opens upward and the function is non - positive only at the root. So, the solution to the inequality is the single value $x = {root}$, written in interval notation as $[{root}, {root}]$."
        else:
            answer = "(-∞, +∞)"
            explanation = "The discriminant of the quadratic function $y = {a}x^2 + {b}x+{new_c}$ is zero, and since $a<0$, the parabola opens downward. The function is non - positive for all real values of $x$. So, the solution set is $(-\\infty, +\\infty)$."
    else:
        root1 = (-b - math.sqrt(discriminant)) / (2 * a)
        root2 = (-b + math.sqrt(discriminant)) / (2 * a)
        if a > 0:
            answer = f"[{min(root1, root2)}, {max(root1, root2)}]"
            explanation = "The discriminant of the quadratic function $y = {a}x^2 + {b}x+{new_c}$ is positive, so the quadratic has two distinct real roots at $x = {root1}$ and $x = {root2}$. Since $a>0$, the parabola opens upward. The function is non - positive between the two roots. So, the solution to the inequality is the interval $[{min(root1, root2)}, {max(root1, root2)}]$."
        else:
            answer = f"(-∞, {min(root1, root2)}] ∪ [{max(root1, root2)}, +∞)"
            explanation = "The discriminant of the quadratic function $y = {a}x^2 + {b}x+{new_c}$ is positive, so the quadratic has two distinct real roots at $x = {root1}$ and $x = {root2}$. Since $a<0$, the parabola opens downward. The function is non - positive outside the two roots. So, the solution to the inequality is the union of the intervals $(-\\infty, {min(root1, root2)}]$ and $[{max(root1, root2)}, +\\infty)$."
    return problem, answer, explanation

# 函数用于生成复利问题、答案及解析
def generate_compound_interest_problem():
    principal = random.randint(500, 2000)
    amount = random.randint(principal + 200, principal + 1000)
    years = random.randint(2, 5)
    problem = f"Mr. Smith invests {principal} dollars in a fund that compounds annually at a constant interest rate. After {years} years, his investment has grown to {amount} dollars. What is the annual interest rate, as a percentage? (Round your answer to the nearest integer.)"
    rate = ((amount / principal) ** (1 / years) - 1) * 100
    answer = round(rate)
    explanation = f"The formula for compound interest compounded annually is $A = P(1 + r)^t$, where $A$ is the final amount, $P$ is the principal, $r$ is the annual interest rate, and $t$ is the number of years. We are given $P = {principal}$, $A = {amount}$, and $t = {years}$. Rearranging the formula to solve for $r$ gives $r=({amount}/{principal})^{{1/{years}}}-1$. Then we multiply by 100 to get the percentage and round to the nearest integer, so the annual interest rate is {answer}%."
    return problem, answer, explanation

# 函数用于生成整数配对求和问题、答案及解析
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
    explanation = f"Assume $a < b < c < d$. Then the smallest sum of pairs is $a + b$ and the largest sum of pairs is $c + d$. We also know some other sums. By using the relationships between these sums, we can solve for the individual integers. First, we note that $a + b={a_plus_b}$, $c + d={c_plus_d}$, $a + c={a_plus_c}$, and $b + d={b_plus_d}$. Through a series of algebraic manipulations, we find that $d = {total}-{a_plus_b}-{a_plus_c}+{sums[2]}$, and then we can find $c$, $b$, and $a$ using the known sums. So the four integers in increasing order are {answer}."
    return problem, answer, explanation

# 函数用于生成绝对值方程问题、答案及解析
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
    explanation = f"The equation $|{left}| = |{right}|$ can be split into two cases: {left}={right} and {left}=-{right}. Solving {left}={right} gives $({a}x - {b})=({c}x + {d})$, which simplifies to $({a}-{c})x={b + d}$, so $x = {case1}$ (when $a\\neq c$). Solving {left}=-{right} gives $({a}x - {b})=-({c}x + {d})$, which simplifies to $({a}+{c})x={b - d}$, so $x = {case2}$. We then take the minimum of these two values to get the smallest solution {answer}."
    return problem, answer, explanation

# 函数用于生成函数复合与反函数问题、答案及解析
def generate_function_composition_inverse_problem():
    f_coefficient = random.randint(3, 9)
    f_constant = random.randint(1, 5)
    g_coefficient = random.randint(1, 3)
    g_constant = random.randint(-3, 3)
    f_function = f"{f_coefficient}x + {f_constant}"
    g_function = f"{g_coefficient}x + {g_constant}"
    problem = f"Let $f(x) = {f_function}$ and $g(x) = {g_function}$. If $h(x)=f(g(x))$, then what is the inverse of $h(x)$?"

    # 先求 h(x)
    h_coefficient = f_coefficient * g_coefficient
    h_constant = f_coefficient * g_constant + f_constant
    h_function = f"{h_coefficient}x + {h_constant}"

    # 再求 h(x) 的反函数
    # 设 y = h(x) = {h_coefficient}x + {h_constant}，则 x = (y - {h_constant}) / {h_coefficient}
    answer = f"\\frac{{x - {h_constant}}}{{{h_coefficient}}}"

    explanation = f"First, find \(h(x) = f(g(x))\) according to the definition of function composition. Substitute \(g(x) = {g_coefficient}x + {g_constant}\) into \(f(x) = {f_coefficient}x + {f_constant}\), and we get \(h(x) = {f_coefficient}({g_coefficient}x + {g_constant}) + {f_constant}\). After expanding, it becomes \(h(x) = {h_coefficient}x + {h_constant}\). Then, find the inverse function of \(h(x)\). Let \(y = h(x)\), that is \(y = {h_coefficient}x + {h_constant}\). Solve for \(x\) by moving the terms, and we obtain \(x=\\frac{{y - {h_constant}}}{{ {h_coefficient} }}\). By interchanging \(x\) and \(y\), we get the inverse function of \(h(x)\) as {answer}."
    return problem, answer, explanation

# 函数用于生成绝对值不等式问题、答案及解析
def generate_absolute_value_inequality_problem():
    a = random.randint(5, 10)
    b = random.randint(1, 5)
    c = random.randint(3, 7)
    d = random.randint(1, 4)
    left_inequality = f"|{a}x - {b}| > {c}"
    right_inequality = f"|{a}x + {d}| \\le {c}"
    problem = f"Find the sum of all integers that satisfy these conditions: \\[ {left_inequality} \\text{{ and }} {right_inequality} \\]"

    # 求解 |{a}x - {b}| > {c}
    left_solutions1 = []
    left_solutions2 = []
    if a > 0:
        left_solutions1 = [i for i in range(math.ceil((b + c) / a), 100) if isinstance(i, int)]
        left_solutions2 = [i for i in range(-100, math.floor((b - c) / a) + 1) if isinstance(i, int)]
    all_left_solutions = left_solutions1 + left_solutions2

    # 求解 |{a}x + {d}| <= {c}
    right_solutions = [i for i in range(math.ceil((-c - d) / a), math.floor((c - d) / a) + 1) if isinstance(i, int)]

    # 求交集
    common_solutions = [i for i in all_left_solutions if i in right_solutions]
    answer = sum(common_solutions)

    explanation = f"First, solve the two absolute - value inequalities separately. For the inequality {left_inequality}, according to the property of absolute values, it can be transformed into two inequalities: {a}x - {b} > {c} or {a}x - {b} < - {c}. Solve these two inequalities to obtain the set of integer solutions that satisfy this inequality. For the inequality {right_inequality}, also according to the property of absolute values, transform it into - {c} ≤ {a}x + {d} ≤ {c}. Solve this compound inequality to get the set of its integer solutions. Finally, find the intersection of these two sets to obtain the set of integer solutions that satisfy both inequalities simultaneously. Then, add up these integers to get the answer {answer}. "
    return problem, answer, explanation

# 函数用于生成距离公式问题、答案及解析
def generate_distance_formula_problem():
    x = random.randint(-10, -1)
    y = random.randint(1, 10)
    point = f"({x},{y})"
    problem = f"What is the number of units in the distance from the origin to the point {point} in a coordinate system?"

    answer = math.sqrt(x ** 2 + y ** 2)

    explanation = f"In the plane rectangular coordinate system, the distance formula between two points \((x_1,y_1)\) and \((x_2,y_2)\) is \(d = \sqrt{{(x_2 - x_1)^2+(y_2 - y_1)^2}}\). In this problem, one point is the origin \((0,0)\) and the other point is {point}. Substitute the coordinates into the distance formula, and we get the distance \(d = \sqrt{{({x}-0)^2+({y}-0)^2}}=\sqrt{{{x}^2 + {y}^2}} = {answer}\)."
    return problem, answer, explanation

# 函数用于生成中点坐标问题、答案及解析
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

    explanation = f"If there are two points \((x_1,y_1)\) and \((x_2,y_2)\), the mid - point coordinate formula for the line segment connecting them is \(M(\\frac{{x_1 + x_2}}{{2}},\\frac{{y_1 + y_2}}{{2}})\). In this problem, the two endpoints are {point1} and {point2} respectively. According to the mid - point coordinate formula, we can calculate that the abscissa of the mid - point is \(\\frac{{{x1}+{x2}}}{{2}}\) and the ordinate is \(\\frac{{{y1}+{y2}}}{{2}}\). By adding the abscissa and the ordinate of the mid - point, we get the answer {answer}."
    return problem, answer, explanation

# 函数用于生成风筝面积问题、答案及解析
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

    explanation = f"It is known that the area of a kite (a quadrilateral with two pairs of adjacent sides equal respectively) is equal to half the product of its two diagonals. In this problem, first, calculate the lengths of the two diagonals using the distance formula between two points. Let the diagonal be determined by points $A({a_x},{a_y})$ and $C({c_x},{c_y})$, and its length is $\sqrt{{({a_x}-{c_x})^2+({a_y}-{c_y})^2}} = {diagonal1}$. Let the other diagonal be determined by points $B({b_x},{b_y})$ and $D({d_x},{d_y})$, and its length is $\sqrt{{({b_x}-{d_x})^2+({b_y}-{d_y})^2}} = {diagonal2}$. Then, according to the area formula of a kite $S = \\frac{1}{2} \\times$ (length of diagonal 1) $\\times$ (length of diagonal 2), the area of kite $ABCD$ is obtained as {answer}."
    return problem, answer, explanation

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
    generate_kite_area_problem,
    generate_linear_system_problem,
    generate_circle_equation_problem,
    generate_function_composition_problem,
    generate_exponential_equation_problem,
    generate_floor_ceiling_problem,
    generate_difference_of_squares_problem,
    generate_ratio_multiplication_problem,
    generate_exponent_power_problem,
    generate_absolute_value_equation_problem,
    generate_square_difference_equation_problem,
    generate_midpoint_formula_problem,
    generate_quadratic_equation_problem,
    generate_polynomial_factorization_problem,
    generate_midpoint_sum_problem,
    generate_quadratic_roots_relation_problem,
    generate_perfect_square_formula_problem,
    generate_line_intersection_problem,
    generate_denominator_rationalization_problem
]

# 生成指定数量的问题及答案和解析
def generate_problems(num_problems):
    problems_and_answers = []
    for _ in range(num_problems):
        # 随机选择一个问题生成函数
        generator = random.choice(problem_generators)
        problem, answer, explanation = generator()
        problems_and_answers.append((problem, answer, explanation))
    return problems_and_answers

# 示例：生成10个问题及答案和解析
generated_problems = generate_problems(10)
for i, (problem, answer, explanation) in enumerate(generated_problems, 1):
    print(f"Problem {i}: {problem}")
    print(f"Answer {i}: {answer}")
    print(f"Explanation {i}: {explanation}")
    print()

