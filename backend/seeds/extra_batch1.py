"""扩展教程数据：第 1 批（运算符与流程控制细节）。

本文件只定义 LESSONS 与 EXERCISES 两个列表，供 seed.py 汇总导入使用。
"""

LESSONS = [
    {
        "slug": "operator-detail",
        "title": "Python 运算符",
        "summary": "系统掌握各类运算符与运算优先级。",
        "order_index": 13,
        "duration_min": 10,
        "content_md": """# Python 运算符

## 什么是运算符与表达式
运算符是用来对数据执行某种操作的符号，被操作的数据叫做操作数。由操作数和运算符组成的式子称为表达式，表达式计算后会得到一个结果。例如 `3 + 5` 中，`+` 是加法运算符，`3` 和 `5` 是操作数，整个式子的结果是 8。Python 内置了非常丰富的运算符，把它们分类系统掌握，能让你写出更简洁、更高效的代码。本篇会按功能把运算符分成算术、比较、逻辑、赋值、成员和身份等几大类逐一讲解，并重点说明运算符优先级，帮助初学者建立完整的知识框架。

## 算术运算符
算术运算符用于完成数学计算。`+` 加法、`-` 减法、`*` 乘法、`/` 普通除法（结果一定是浮点数）、`//` 整除（向下取整）、`%` 取余（求余数）、`**` 幂运算（乘方）。例如 `9 // 4` 的结果是 2，`9 % 4` 的结果是 1，`2 ** 3` 表示 2 的 3 次方，结果是 8。普通除法 `6 / 3` 的结果是 2.0 而不是 2，这是初学者容易困惑的地方。整除和取余经常搭配使用，比如判断一个数是奇数还是偶数，只需要看 `n % 2` 是否等于 0。

## 比较运算符
比较运算符用来比较两个值，结果总是布尔值 True 或 False。`>` 大于、`<` 小于、`>=` 大于等于、`<=` 小于等于、`==` 等于、`!=` 不等于。要特别区分赋值符号 `=` 和判断相等的 `==`：前者是把右边的值存到左边变量里，后者才是比较两个值是否相等。把 `==` 写成 `=` 是初学者最常犯的错误之一，轻则结果错误，重则直接报语法错误。

## 逻辑运算符
逻辑运算符用于把多个条件组合起来。`and` 表示“并且”，只有两边都为真时结果才为真；`or` 表示“或者”，只要一边为真结果就为真；`not` 表示“取反”，把真变假、假变真。例如 `age >= 18 and score > 60` 表示同时满足成年且分数及格。逻辑运算遵循短路规则：`and` 左边为假时右边不再计算，`or` 左边为真时右边不再计算，这在编写条件时能保护后面的表达式。

## 赋值运算符与复合赋值
`=` 是最基本的赋值运算符。把算术运算符和 `=` 组合起来就得到复合赋值运算符：`x += 1` 等价于 `x = x + 1`，`x -= 2`、`x *= 3`、`x /= 2`、`x %= 2` 依此类推。复合赋值让代码更紧凑，是实际开发中非常常见的写法，务必要熟悉。

## 成员与身份运算符
成员运算符 `in` 和 `not in` 用来判断一个元素是否存在于序列中，例如 `'a' in 'abc'` 的结果是 True。身份运算符 `is` 和 `is not` 用来判断两个变量是否指向同一个对象，它与比较值是否相等的 `==` 不同，初学者了解即可，后续深入时再体会区别。

## 运算符优先级
当一个表达式里有多个运算符时，Python 按优先级决定计算顺序：括号 `()` 最高，其次是幂运算 `**`，再是乘除整除取余 `* / // %`，然后是加减 `+ -`，接着是比较运算符，最后是 `not`、`and`、`or`。拿不准时最好用括号明确顺序，既避免出错，也让代码更容易读懂，这是被强烈推荐的好习惯。

## 常见错误
常见错误有三类：一是把判断相等的 `==` 写成 `=`；二是忽略优先级导致结果和预期不符，例如 `2 + 3 * 4` 的结果是 14 而不是 20；三是对整数使用 `/` 后以为得到整数，其实得到的是浮点数 2.0。

## 要点提示
- `/` 总是返回浮点数，需要整数商请用 `//`。
- 判断相等用 `==`，赋值用 `=`，两者不可混用。
- 不确定优先级时就加括号，代码清晰又安全。
- `and` / `or` 具有短路特性，可用来保护后面的表达式。""",
        "code_example": """# 算术运算符
a, b = 9, 4
print("加法：", a + b)
print("普通除法：", a / b)
print("整除：", a // b)
print("取余：", a % b)
print("幂运算：", 2 ** 3)

# 比较运算符
x = 10
print("x > 5：", x > 5)
print("x == 10：", x == 10)
print("x != 3：", x != 3)

# 逻辑运算符
print("并且：", x > 5 and x < 20)
print("或者：", x < 0 or x > 5)
print("取反：", not (x > 5))

# 复合赋值
n = 7
n %= 2
print("7 对 2 取余：", n)

# 成员运算
print("成员判断：", 'a' in 'abc')

# 优先级
print("2 + 3 * 4 =", 2 + 3 * 4)
print("(2 + 3) * 4 =", (2 + 3) * 4)""",
    },
    {
        "slug": "condition-detail",
        "title": "Python 条件语句",
        "summary": "深入理解条件分支、真值判断与条件表达式。",
        "order_index": 14,
        "duration_min": 10,
        "content_md": """# Python 条件语句

## 条件语句的作用
程序默认按顺序一行行往下执行，而条件语句让程序能根据不同情况走不同的分支，这就是“做选择”的能力。生活里到处都是选择：如果考试成绩及格就通过，否则补考；如果今天是周末就休息，否则上班。把这种逻辑写进程序，靠的就是 if 系列语句。本篇在基础用法之上，更细致地讲解条件的本质、分支的执行顺序和几个容易被忽略的细节。

## if 语句的基本语法
最简单的形式是 `if 条件:`，条件后面必须写英文冒号 `:`，下一行用缩进写下条件成立时才执行的代码。缩进通常是 4 个空格，同一个代码块内的缩进必须一致。例如 `if score >= 60:` 后面缩进的语句只有在 score 大于等于 60 时才会运行。在 Python 中缩进不是可有可无的格式，而是用来划分代码块的关键语法，写错缩进程序就无法正常工作。

## else 与 elif 的执行逻辑
当 if 的条件不成立时，程序会跳到 `else:` 分支执行另一段代码。如果有多种情况依次判断，就用 `elif:`（else if 的缩写）连接多个分支。整个结构从上往下逐个检查条件，一旦某个条件成立就执行对应分支，执行完立刻跳出整个判断结构，剩下的分支不再检查。因此把范围更小、更具体的条件写在前面非常重要，否则可能被前面宽泛的条件“截胡”。例如先判断 `score >= 90` 再判断 `score >= 60`，顺序颠倒就会导致高分也被判成及格。

## 条件的真值与假值
条件位置并不只能写比较表达式，任何值都能当成条件来判断。Python 把某些值看作“假”，包括 `False`、`0`、空字符串、空列表 `[]`、空字典和 `None`；其余大多数值都被看作“真”。所以 `if name:` 可以简洁地判断字符串是否为空，`if items:` 可以判断列表里有没有元素。理解真值判断能让你写出更地道、更简洁的代码。

## 嵌套条件
if 语句内部还能再写 if，形成嵌套结构，用来处理多层次的判断。但嵌套层级太深会让代码难以阅读，很多情况可以用 elif 平铺或者用逻辑运算符组合来替代。一个简单的原则是：能用一层解决的，就不要用两层，保持代码扁平清晰。

## 条件表达式（三元运算符）
Python 提供一种简洁的条件表达式：`结果1 if 条件 else 结果2`。条件成立取结果1，否则取结果2。例如 `label = "通过" if score >= 60 else "补考"` 一行就能完成原本需要四行的判断，特别适合简单的二选一赋值场景，既紧凑又易读。

## 常见错误
第一，忘记写条件后的冒号；第二，分支代码块没缩进或缩进不一致；第三，把判断相等的 `==` 写成赋值的 `=`；第四，混淆 `if` 与 `elif` 的判断顺序导致逻辑错误。这些都能通过仔细阅读报错信息和逐行检查来定位解决。

## 要点提示
- if / elif / else 后都要加英文冒号 `:`。
- 只有第一个满足的分支会被执行，条件顺序会影响结果。
- 0、空字符串、空列表、`None` 都被当作假值。
- 简单的二选一赋值可用条件表达式一行搞定。""",
        "code_example": """# 基本 if / else
score = 85
if score >= 60:
    print("及格")
else:
    print("不及格")

# 多分支 elif，注意从具体到宽泛
if score >= 90:
    print("优秀")
elif score >= 80:
    print("良好")
elif score >= 60:
    print("及格")
else:
    print("不及格")

# 真值判断
name = ""
if name:
    print("名字不为空")
else:
    print("名字是空的")

# 条件表达式
result = "通过" if score >= 60 else "补考"
print("结果：", result)

# 嵌套条件
if score >= 60:
    if score >= 90:
        print("成绩优异")""",
    },
    {
        "slug": "loop-overview",
        "title": "Python 循环语句",
        "summary": "认识两种循环语句的区别。",
        "order_index": 15,
        "duration_min": 9,
        "content_md": """# Python 循环语句

## 为什么需要循环
想象一下要打印 1 到 100 的每个数字，如果一行行写 `print` 要写一百遍，既低效又容易出错。循环语句的出现就是为了让一段代码重复执行多次。Python 提供两种循环：`for` 循环和 `while` 循环。本篇带你从整体上认识它们，理解各自的适用场景和基本结构，为后面逐篇深入学习打下基础。

## for 循环概览
for 循环用于“次数已知”或者“遍历一个序列”的场景。它会依次取出序列中的每个元素，每取一个就执行一次循环体。最常见的搭配是 `range()` 函数，`range(5)` 会产生 0、1、2、3、4 这五个整数（包含起点 0，不包含终点 5）。写法 `for i in range(5):` 中，变量 i 会依次拿到这些值。除了 range，for 还能直接遍历字符串、列表等任何序列，例如 `for ch in "abc":` 会让 ch 依次等于 a、b、c。

## while 循环概览
while 循环用于“只要条件成立就一直重复”的场景。写法是 `while 条件:`，每一轮开始时先检查条件，为真就执行循环体，为假就结束循环。例如 `while i < 5:` 会在 i 小于 5 时持续执行。使用 while 时必须在循环体内修改条件变量（比如 `i += 1`），让条件最终变为假，否则会陷入永远停不下来的死循环，这是使用 while 时最需要警惕的一点。

## for 与 while 怎么选
两者的核心区别在于：for 循环的次数通常事先确定，或者由序列长度决定；while 循环的次数事先不确定，由条件何时变为假决定。打印 1 到 10 适合用 for，因为次数明确；而“一直读取用户输入直到输入 q 退出”适合用 while，因为不知道用户会输入几次。一个简单的判断标准是：如果循环次数能数得清，用 for；如果说不清、取决于条件，用 while。

## 循环控制语句
在循环过程中，有时需要改变正常的执行流程。`break` 用来立刻跳出整个循环，`continue` 用来跳过本次循环剩余代码直接进入下一轮，`pass` 表示什么都不做、仅作占位。这三个语句都常和 if 配合使用，用来处理循环中的特殊情况，后面会有专门的篇章逐一深入讲解。

## 循环中的 else
Python 的 for 和 while 都可以带一个 `else` 分支：当循环自然执行完毕、没有被 break 打断时，会执行 else 里的代码。这个特性初学者了解即可，实际使用频率不高，但读懂别人的代码时可能会遇到。

## 常见错误
初学者常犯的错误包括：漏写循环条件后的冒号；循环体忘记缩进；使用 while 时忘了更新条件变量导致死循环；误以为 `range(5)` 包含 5。其中死循环会让程序卡住，一旦发生可以用 Ctrl+C 强制停止。

## 要点提示
- `range(n)` 产生 0 到 n-1，不含 n。
- for 适合次数已知，while 适合条件驱动。
- while 一定要更新条件变量，防止死循环。
- 循环体必须缩进，冒号不能漏写。""",
        "code_example": """# for 遍历 range
for i in range(5):
    print("第", i, "次")

# for 遍历字符串
for ch in "Python":
    print(ch)

# while 条件循环
i = 0
while i < 3:
    print("i =", i)
    i += 1

# break 提前结束
for n in range(10):
    if n == 3:
        break
    print("n =", n)""",
    },
    {
        "slug": "while-loop",
        "title": "Python While 循环语句",
        "summary": "专讲 while 循环细节与死循环防范。",
        "order_index": 16,
        "duration_min": 10,
        "content_md": """# Python While 循环语句

## while 循环的核心思想
while 是“当……的时候”的意思。while 循环会不断检查一个条件，只要条件成立（结果为 True），就重复执行循环体；一旦条件不成立，循环立刻结束。它和 for 循环最大的不同是：for 通常知道要循环多少次，而 while 事先不知道次数，只关心条件什么时候不满足。这就让 while 特别适合处理“一直做到某件事发生为止”的任务，例如猜数字游戏、读取用户输入直到输入指定指令等。

## 基本语法
while 语句的形式是 `while 条件:`，条件后面加英文冒号，下一行缩进写循环体。每执行完一轮，程序会回到 while 行重新判断条件。来看最经典的计数器例子：先令 `i = 0`，再写 `while i < 5:`，循环体内打印 i 并写上 `i += 1`。这样 i 会从 0 逐渐增加到 4，循环执行 5 次后 i 变成 5，条件不再成立，循环结束。

## 死循环及其防范
使用 while 时最危险的问题是死循环：如果循环体内没有改变条件变量，或者改变的方向不对，条件会永远成立，程序就卡在循环里出不来。例如 `while i < 5:` 里如果忘了写 `i += 1`，i 始终是 0，循环永不停止。防范方法是：动手写 while 之前先问自己“这个条件什么时候会变成假”，并确保循环体里真的有语句在朝那个方向推进条件变量。万一不小心写出死循环，可以在终端按 Ctrl+C 强制中断程序。

## 用 break 结束 while
有些循环很难用条件自然结束，比如“让用户一直输入，直到输入 quit”。这时可以把条件写成 `while True:`（永远成立），再在循环体内部用 `if ...: break` 在合适时机跳出。这种“无限循环 + break”是非常常见的写法，既灵活又清晰。不过要注意 break 必须真的有机会被执行到，否则同样会变成死循环，写完后要仔细检查退出条件。

## while 与 else 搭配
while 循环后面可以跟一个 else 分支。当循环因为条件变为假而自然结束时，else 里的代码会执行；但如果是被 break 提前跳出的，else 就不会执行。这个特性可以用来区分循环是“正常做完”还是“中途跳出”，虽然日常用得不多，但了解它能帮你读懂别人写的复杂代码。

## 常见错误
第一，忘记在循环体里更新条件变量，造成死循环；第二，把循环条件写反，导致一次都不执行或停不下来；第三，缩进错误，把本该在循环体内的语句写到了外面，结果条件永远不变；第四，漏写冒号。这些都是写 while 时反复要检查的地方，养成写完就模拟执行几轮的习惯很有帮助。

## 要点提示
- while 条件为 True 时重复执行，为 False 时结束。
- 循环体内必须更新条件变量，否则会死循环。
- `while True:` 配合 `break` 是处理不确定次数的常用套路。
- 死循环可用 Ctrl+C 强制停止，写完 while 要先确认能退出。""",
        "code_example": """# 基本计数循环
i = 0
while i < 5:
    print("当前 i =", i)
    i += 1  # 别忘了更新条件变量

# 累加求和
total = 0
n = 1
while n <= 10:
    total += n
    n += 1
print("1 到 10 的和：", total)

# while True 配合 break（输入 quit 结束）
while True:
    answer = input("输入 quit 结束程序：")
    if answer == "quit":
        break
    print("你输入的是：", answer)

# while 与 else
count = 0
while count < 3:
    print("count =", count)
    count += 1
else:
    print("循环自然结束")""",
    },
    {
        "slug": "for-loop",
        "title": "Python for 循环语句",
        "summary": "for 循环与 range 用法详解。",
        "order_index": 17,
        "duration_min": 11,
        "content_md": """# Python for 循环语句

## for 循环的本质
for 循环叫做“遍历循环”，它的工作方式是：依次从某个序列中取出一个元素，把这个元素赋值给循环变量，然后执行一遍循环体，直到序列里的元素全部取完为止。这里的“序列”可以是字符串、列表，也可以是 range 生成的整数序列。和 while 相比，for 循环不需要你手动维护计数器，取元素和推进都由 Python 自动完成，因此更不容易出错，是日常使用频率最高的循环。

## 基本语法
for 语句的形式是 `for 变量 in 序列:`，后面加英文冒号，下一行缩进写循环体。例如 `for i in range(3):` 会让 i 依次等于 0、1、2，循环体执行三次。循环变量 i 在每一轮都会被赋予新的值，即便循环结束后，i 仍然保留最后一次取到的值，这一点在循环后使用 i 时很有用。

## range() 的三种用法
range 是 for 循环最忠实的搭档，它有三种常见写法。第一种 `range(n)`，从 0 到 n-1，例如 `range(5)` 产生 0、1、2、3、4。第二种 `range(start, end)`，从 start 到 end-1，例如 `range(2, 6)` 产生 2、3、4、5。第三种 `range(start, end, step)`，step 是步长，例如 `range(1, 10, 2)` 产生 1、3、5、7、9；步长还可以是负数，用来倒着数，例如 `range(5, 0, -1)` 产生 5、4、3、2、1。记住一个要点：终点永远不包含在内。

## 遍历各种序列
for 不只配 range 使用，它能直接遍历任何可迭代对象。遍历字符串时，循环变量依次是每个字符，例如 `for ch in "abc":`。遍历列表时，循环变量依次是每个元素，例如 `for item in [10, 20, 30]:`。如果遍历字典，默认拿到的是一个个键。这种“直接遍历元素”的方式比用下标去取更简洁，也更符合 Python 的风格，是推荐初学者养成的习惯。

## 同时拿到下标和值
有时既想要元素又想要它的位置下标，可以用 `enumerate()`。写法是 `for i, ch in enumerate("abc"):`，其中 i 是下标（从 0 开始），ch 是对应的字符。enumerate 会帮你把下标和值配对，免去了手动维护计数器的麻烦，在需要知道元素位置的场景下非常方便。

## 常见错误
第一，误以为 `range(5)` 包含 5，结果少循环一次；第二，在循环体内修改循环变量，试图改变循环次数——for 每轮都会重新给变量赋值，手动改它通常不起作用；第三，忘记冒号或循环体缩进；第四，步长写成 0 导致报错，因为步长不能为 0。

## 要点提示
- `range(n)` 产生 0 到 n-1，永远不包含终点。
- `range(start, end, step)` 可指定起点、终点和步长。
- for 能直接遍历字符串、列表、字典等可迭代对象。
- 需要下标和值同时出现时用 `enumerate()`。""",
        "code_example": """# range(n)：0 到 n-1
for i in range(5):
    print(i, end=" ")
print()

# range(start, end)
for i in range(2, 6):
    print(i, end=" ")
print()

# range(start, end, step) 步长
for i in range(1, 10, 2):
    print(i, end=" ")
print()

# 倒着数
for i in range(5, 0, -1):
    print(i, end=" ")
print()

# 遍历字符串
for ch in "Python":
    print(ch, end="-")
print()

# enumerate 同时拿下标和值
for i, ch in enumerate("abc"):
    print(i, ch)""",
    },
    {
        "slug": "nested-loop",
        "title": "Python 循环嵌套",
        "summary": "学会循环嵌套，打印二维表格与图案。",
        "order_index": 18,
        "duration_min": 12,
        "content_md": """# Python 循环嵌套

## 什么是循环嵌套
在一个循环体内再写一个完整的循环，就叫做循环嵌套，也叫双重循环或多重循环。外层循环每执行一次，内层循环就会从头到尾完整地跑一遍。打个比方：外层循环像时钟的时针，内层循环像分针，时针走一格，分针要转满一整圈。嵌套循环是处理二维数据、打印表格和图案的强大工具，掌握它之后你能写出非常有趣的程序。

## 基本结构
嵌套循环的形式就是把一个 for 循环缩进着放进另一个 for 循环里。例如外层 `for i in range(3):`，内层 `for j in range(2):`，内层缩进写具体要做的事。执行过程是这样的：i 取 0 时，j 依次取 0、1 跑完内层循环；接着 i 取 1，j 又从 0、1 跑一遍；i 取 2 时同理。所以内层总共执行 3 × 2 = 6 次。外层决定“行数”，内层决定“每行的列数”，这个对应关系非常重要。

## 打印矩形图案
嵌套循环最常见的用途是打印由符号组成的二维图案。比如想打印一个 3 行 5 列的星号矩形，就让外层循环控制 3 行，内层循环控制每行打印 5 个星号。内层用 `print("*", end="")` 让星号连在一行不换行，等内层这一行打印完后，外层再执行一次 `print()` 换行。这里 end 参数控制 print 结尾的字符，默认是换行，设为空字符串就不换行，这是打印图案的关键技巧。

## 打印三角形与九九乘法表
如果把内层次数写成与外层变量相关，就能打印三角形。例如 `for j in range(i + 1):` 会让第 i 行打印 i+1 个符号。著名的九九乘法表也是嵌套循环的经典案例：外层 `for i in range(1, 10):` 控制行，内层 `for j in range(1, i + 1):` 控制每行的算式，用 `print(f"{j}×{i}={i*j}", end="\\t")` 打印，一行结束再换行。

## 执行次数与效率
嵌套循环的总执行次数等于各层循环次数的乘积，层数越多、次数增长越快。三重循环如果每层 100 次，就要执行一百万次。所以写嵌套循环时要留意规模，避免不必要的多层嵌套导致程序运行缓慢，在数据量大的时候尤其要谨慎。

## 常见错误
第一，分不清内外层变量，把 i 和 j 用混，导致图案错乱；第二，内层该用 `end=""` 的地方忘了写，结果每个符号都换了行；第三，内层循环结束后忘了换行，所有内容挤在一行；第四，缩进层级写错，导致内层循环没有真正嵌套进去。调试嵌套循环时，可以在循环里打印 i 和 j 的值，观察它们的组合变化。

## 要点提示
- 外层循环每走一步，内层循环完整跑一遍。
- 外层通常控制行，内层控制每行的列数。
- `print(..., end="")` 可让输出不换行，方便拼成一行。
- 总执行次数是各层次数的乘积，注意控制规模。""",
        "code_example": """# 打印 3 行 5 列的星号矩形
for i in range(3):
    for j in range(5):
        print("*", end="")
    print()  # 一行结束后换行

print("---")

# 打印直角三角形
for i in range(1, 6):
    for j in range(i):
        print("*", end="")
    print()

print("---")

# 九九乘法表
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}×{i}={i*j}", end="\t")
    print()""",
    },
    {
        "slug": "break-statement",
        "title": "Python break 语句",
        "summary": "用 break 提前跳出当前循环。",
        "order_index": 19,
        "duration_min": 8,
        "content_md": """# Python break 语句

## break 的作用
break 的意思是“打破、中断”，在 Python 里它用来立刻终止当前所在的循环。一旦执行到 break，程序会马上跳出循环体，不再执行本轮循环剩下的代码，也不再进行后续次数，直接接着执行循环后面的语句。break 常和 if 搭配，用来在满足某个特殊条件时提前结束循环，比如“找到目标就不再继续找了”，能有效提升效率。

## 基本用法
break 只能写在循环体内部，也就是 for 或 while 的缩进代码块里，写在外面会报错。它最常见的搭档是 if：`for i in range(10):` 循环里写 `if i == 3: break`，那么当 i 等于 3 时就跳出循环，输出只会到 2，后面的 4、5 根本不会执行。注意 break 会跳过本轮循环体中 break 之后的所有语句，所以要把 break 放在合适的位置，避免把还需要执行的代码挡在它后面。

## break 跳出的是哪一层
在嵌套循环里，break 只会跳出“离它最近的那一层”循环，外层循环不受影响，会继续执行下一轮。例如外层循环 3 次、内层循环里有一个 break，那么每一轮外层循环都会执行内层，内层碰到 break 就跳出自己，然后外层进入下一轮，如此重复 3 次。如果想一次性跳出所有层，需要额外的标志变量或其他技巧，这是初学者需要留意的细节。

## break 与 while True 的配合
break 最经典的用武之地是和 `while True:` 搭配。`while True` 的条件永远成立，单靠它自己会无限循环，但配合循环体里的 `if 条件: break`，就能实现“满足条件就退出”的灵活控制。比如让程序反复让用户输入内容，直到输入 quit 才 break 退出。这种写法把退出条件写在循环内部，逻辑清晰，非常实用。

## break 影响循环的 else
前面学过循环可以带 else 分支。需要记住：如果循环是被 break 提前跳出的，那么 else 分支不会执行；只有循环自然结束（条件为假或序列遍历完）时，else 才会运行。因此可以用 else 是否被跳过来判断循环中途有没有 break，这是 break 与 else 配合的一个巧妙用法。

## 常见错误
第一，把 break 写在循环外面，导致语法错误；第二，在嵌套循环里误以为 break 能跳出所有层，结果外层还在继续；第三，break 的条件永远不成立，等于没写；第四，在 `while True` 循环里忘了写 break 或 break 条件无法触发，造成死循环。写 break 时一定要想清楚“它跳出哪一层”和“条件到底能不能满足”。

## 要点提示
- break 立刻结束最近的那一层循环。
- break 之后本轮循环的其余代码不会执行。
- `while True:` 配合 `if ...: break` 是常用套路。
- 被 break 打断的循环不会执行它的 else 分支。""",
        "code_example": """# for 循环中用 break 提前结束
for i in range(10):
    if i == 5:
        break
    print(i)
print("循环结束，i =", i)

# while True 配合 break
count = 0
while True:
    print("count =", count)
    count += 1
    if count >= 3:
        break
print("退出 while True")

# 嵌套循环中 break 只跳出内层
for i in range(3):
    for j in range(5):
        if j == 2:
            break
        print(f"({i},{j})", end=" ")
    print()""",
    },
    {
        "slug": "continue-statement",
        "title": "Python continue 语句",
        "summary": "用 continue 跳过本次循环。",
        "order_index": 20,
        "duration_min": 8,
        "content_md": """# Python continue 语句

## continue 的作用
continue 的意思是“继续”，它用来跳过当前这一轮循环中剩下的代码，直接进入下一轮循环。和 break 直接结束整个循环不同，continue 只是“这一轮我不干了，赶紧开始下一轮”。循环本身还会继续，只是本轮循环体里写在 continue 后面的语句不会被执行。它常配合 if 使用，用来过滤掉某些不需要处理的情况。

## 基本用法
continue 同样只能写在循环体内部。来看一个典型例子：遍历 1 到 10，只想打印奇数。写法是 `for i in range(1, 11):`，循环体里先判断 `if i % 2 == 0: continue`，意思是遇到偶数就跳过，于是下面的 `print(i)` 在偶数时不会执行，最终只输出奇数。这里 continue 起到了“跳过偶数”的过滤作用，让代码逻辑非常清晰。

## continue 与 break 的区别
这是初学者最容易混淆的两个语句。break 是“彻底结束循环，后面的次数全都不跑了”；continue 是“只跳过当前这一次，后面的次数照常跑”。打个比方：跑步比赛里，break 相当于退赛不跑了，continue 相当于这一圈偷懒直接跑到下一圈的起点。用一个例子对比：循环 1 到 5，遇到 3 时 break 只会输出 1、2；遇到 3 时 continue 则会输出 1、2、4、5，只少了 3。

## 在 while 循环中使用 continue
continue 在 while 循环里要格外小心。因为 continue 会直接跳到下一轮，while 循环开头会重新检查条件，如果更新条件变量的语句写在 continue 后面，就可能被跳过，导致条件永远不变而陷入死循环。正确的做法是在 continue 之前先更新计数器，或者把更新语句放在循环体开头。这是 while 加 continue 最需要警惕的陷阱。

## continue 与嵌套循环
和 break 一样，continue 也只作用于离它最近的那一层循环，它只会跳过内层循环的本轮，外层循环照常推进。理解这一点有助于在复杂循环里准确控制流程，不至于因为一处 continue 而打乱整个程序的节奏。

## 常见错误
第一，把 continue 写在循环外，导致语法错误；第二，在 while 循环里把更新条件变量的语句写在 continue 之后，造成死循环；第三，把 continue 和 break 的作用搞混，导致该跳过时却结束了整个循环；第四，以为 continue 会结束循环，其实它只是跳过一轮。

## 要点提示
- continue 跳过本轮剩余代码，直接进入下一轮。
- break 结束整个循环，continue 只跳过一次。
- while 中用 continue 要先更新计数器，防止死循环。
- continue 只作用于最近的那一层循环。""",
        "code_example": """# 只打印 1 到 10 的奇数
for i in range(1, 11):
    if i % 2 == 0:
        continue
    print(i)

print("---")

# 跳过包含字母 a 的单词
words = ["apple", "banana", "cat", "dog"]
for w in words:
    if "a" in w:
        continue
    print(w)

print("---")

# while 中使用 continue：先更新计数器
i = 0
while i < 5:
    i += 1
    if i == 3:
        continue
    print(i)""",
    },
    {
        "slug": "pass-statement",
        "title": "Python pass 语句",
        "summary": "用 pass 作为空语句实现语法占位。",
        "order_index": 21,
        "duration_min": 8,
        "content_md": """# Python pass 语句

## pass 是什么
pass 是一个特殊的语句，它的作用用四个字概括就是“什么都不做”。当 Python 遇到 pass 时，会直接跳过它，继续执行后面的代码。既然什么都不做，为什么还需要它呢？这是因为 Python 的语法要求某些位置必须有语句：比如 if 分支后面、函数体里、类定义里，不能空着。当你还没想好这里要写什么，但又必须让代码先能跑起来时，pass 就派上用场了，它起到“占位”的作用。

## 为什么需要占位语句
假设你在规划一个程序，先搭好框架：`if 条件:` 后面暂时不知道写什么。如果这里什么都不写，Python 会报语法错误，因为缩进代码块不能为空。这时写一句 pass，程序就能正常运行（只是这个分支什么都不做）。等以后想好了具体实现，再把 pass 替换成真正的代码。这种“先搭骨架、再填内容”的做法在开发中非常常见，能让你先把整体结构跑通。

## pass 的常见使用场景
第一，占位空分支。比如 `if score >= 60: print("及格") else: pass`，表示及格时打印，不及格时暂时什么都不做。第二，定义空函数或空类。写 `def my_func(): pass` 可以先占住一个函数的位置，让调用它的代码不报错，等以后再补充功能。第三，在编写大型程序时标记待办的地方，常配合注释使用，例如写一句 TODO 注释，下面跟一句 pass。

## pass 与注释的区别
注释（以 # 开头）是给人看的说明文字，Python 完全不理会它；而 pass 是一条真正的语句，只是执行时什么都不做。虽然两者表面上都“没效果”，但意义不同：注释是说明，pass 是语法上的占位。在需要一条语句来满足语法要求的地方，写注释是行不通的，必须用 pass，这一点初学者要分清。

## pass 与 continue、break 的区别
这三个都是流程控制相关的语句，但作用完全不同。pass 什么都不做，只是占位；continue 跳过本轮循环进入下一轮；break 结束整个循环。pass 不会改变循环或程序的执行流程，它纯粹是为了“让这里合法地空着”，理解这一点就不会把它和另外两个语句混淆。

## 常见错误
第一，在该写语句的地方什么都不写，导致缩进错误或语法错误，正确做法是用 pass 占位；第二，误以为 pass 能像 continue 一样跳过循环，其实它毫无影响；第三，在 pass 后面又写了永远用不到的代码却没有删掉占位，造成逻辑混乱。记住 pass 是临时占位符，真正实现写好后要及时替换它。

## 要点提示
- pass 表示空语句，执行时什么都不做。
- 它用于语法上需要语句但暂时没内容的地方，起占位作用。
- 可用于空的 if 分支、空函数和空类。
- pass 不改变执行流程，和 continue、break 有本质区别。""",
        "code_example": """# 用 pass 占位空分支
score = 55
if score >= 60:
    print("及格")
else:
    pass  # 暂时什么都不做

# 用 pass 定义空函数
def todo_function():
    pass  # 以后再补充功能

print("空函数调用结果：", todo_function())

# 用 pass 定义空类
class EmptyClass:
    pass

obj = EmptyClass()
print("空类对象：", obj)

# 遍历时暂时跳过某些情况
for i in range(5):
    if i % 2 == 1:
        pass  # 以后在这里处理奇数
    else:
        print("偶数：", i)""",
    },
]

EXERCISES = [
    # 第 13 篇：Python 运算符
    {
        "lesson_slug": "operator-detail",
        "title": "取余运算",
        "description": "请使用 print() 输出 10 对 3 取余的结果，只写出这一行代码（取余运算符用 %）。",
        "starter_code": "# 在这里写一行代码，输出 10 % 3 的结果\n",
        "expected_answer": "print(10 % 3)",
        "difficulty": "easy",
        "order_index": 25,
    },
    {
        "lesson_slug": "operator-detail",
        "title": "幂运算",
        "description": "请使用 print() 输出 2 的 10 次方的结果，只写出这一行代码（幂运算符用两个星号 **）。",
        "starter_code": "# 在这里写一行代码，输出 2 的 10 次方\n",
        "expected_answer": "print(2 ** 10)",
        "difficulty": "medium",
        "order_index": 26,
    },
    # 第 14 篇：Python 条件语句
    {
        "lesson_slug": "condition-detail",
        "title": "elif 分支",
        "description": "请写出 elif 分支语句行：判断变量 x 是否大于 10，使用变量 x 和大于号 >，并以冒号结尾（只写这一行）。",
        "starter_code": "# 在这里写出 elif 判断行（以冒号结尾）\n",
        "expected_answer": "elif x > 10:",
        "difficulty": "medium",
        "order_index": 27,
    },
    {
        "lesson_slug": "condition-detail",
        "title": "真值判断",
        "description": "请写出判断变量 name 是否非空（真值判断）的 if 语句行：直接把变量 name 当作条件，并以冒号结尾（只写这一行）。",
        "starter_code": "# 在这里写出判断 name 真值的 if 行（以冒号结尾）\n",
        "expected_answer": "if name:",
        "difficulty": "easy",
        "order_index": 28,
    },
    # 第 15 篇：Python 循环语句
    {
        "lesson_slug": "loop-overview",
        "title": "for 循环行",
        "description": "请写出使用 range(5) 的 for 循环语句行，循环变量用 i，并以冒号结尾（只写这一行）。",
        "starter_code": "# 在这里写出 for 循环语句行（以冒号结尾）\n",
        "expected_answer": "for i in range(5):",
        "difficulty": "easy",
        "order_index": 29,
    },
    {
        "lesson_slug": "loop-overview",
        "title": "while 循环行",
        "description": "请写出判断变量 i 是否小于 5 的 while 循环语句行，使用变量 i 和小于号 <，并以冒号结尾（只写这一行）。",
        "starter_code": "# 在这里写出 while 循环语句行（以冒号结尾）\n",
        "expected_answer": "while i < 5:",
        "difficulty": "medium",
        "order_index": 30,
    },
    # 第 16 篇：Python While 循环语句
    {
        "lesson_slug": "while-loop",
        "title": "while 条件行",
        "description": "请写出条件为变量 i 小于 10 的 while 循环语句行，使用变量 i 和小于号 <，并以冒号结尾（只写这一行）。",
        "starter_code": "# 在这里写出 while 循环语句行（以冒号结尾）\n",
        "expected_answer": "while i < 10:",
        "difficulty": "easy",
        "order_index": 31,
    },
    {
        "lesson_slug": "while-loop",
        "title": "更新计数器",
        "description": "请写出把变量 i 的值加 1 后再存回 i 的复合赋值语句（即 i 加一），只写这一行代码。",
        "starter_code": "# 在这里写出让 i 加一的语句\n",
        "expected_answer": "i += 1",
        "difficulty": "easy",
        "order_index": 32,
    },
    # 第 17 篇：Python for 循环语句
    {
        "lesson_slug": "for-loop",
        "title": "遍历字符串",
        "description": "请写出遍历字符串 Python 的 for 循环语句行：循环变量用 ch，字符串用引号包起来，并以冒号结尾（只写这一行）。",
        "starter_code": "# 在这里写出遍历字符串的 for 循环语句行\n",
        "expected_answer": "for ch in 'Python':",
        "difficulty": "medium",
        "order_index": 33,
    },
    {
        "lesson_slug": "for-loop",
        "title": "带步长的 range",
        "description": "请写出 for 循环语句行，用 range 生成从 1 到 9、步长为 2 的数列：即 range 的三个参数依次为 1、10、2，循环变量用 i，并以冒号结尾（只写这一行）。",
        "starter_code": "# 在这里写出带步长的 for 循环语句行\n",
        "expected_answer": "for i in range(1, 10, 2):",
        "difficulty": "medium",
        "order_index": 34,
    },
    # 第 18 篇：Python 循环嵌套
    {
        "lesson_slug": "nested-loop",
        "title": "外层循环",
        "description": "请写出外层 for 循环语句行：使用 range(3)，循环变量用 i，并以冒号结尾（只写这一行）。",
        "starter_code": "# 在这里写出外层 for 循环语句行\n",
        "expected_answer": "for i in range(3):",
        "difficulty": "easy",
        "order_index": 35,
    },
    {
        "lesson_slug": "nested-loop",
        "title": "内层循环",
        "description": "请写出内层 for 循环语句行：使用 range(i)，循环变量用 j，并以冒号结尾（只写这一行）。",
        "starter_code": "# 在这里写出内层 for 循环语句行\n",
        "expected_answer": "for j in range(i):",
        "difficulty": "medium",
        "order_index": 36,
    },
    # 第 19 篇：Python break 语句
    {
        "lesson_slug": "break-statement",
        "title": "跳出循环",
        "description": "请写出能立刻跳出当前循环的跳转语句（只写这个关键字本身，一个单词），只写这一行代码。",
        "starter_code": "# 在这里写出跳出循环的语句\n",
        "expected_answer": "break",
        "difficulty": "easy",
        "order_index": 37,
    },
    {
        "lesson_slug": "break-statement",
        "title": "触发 break 的判断",
        "description": "请写出判断变量 n 是否等于 3 的 if 语句行（常用于配合 break），判断相等用两个等号 ==，并以冒号结尾（只写这一行）。",
        "starter_code": "# 在这里写出判断是否等于 3 的 if 行\n",
        "expected_answer": "if n == 3:",
        "difficulty": "medium",
        "order_index": 38,
    },
    # 第 20 篇：Python continue 语句
    {
        "lesson_slug": "continue-statement",
        "title": "跳过本次循环",
        "description": "请写出能跳过本轮循环、直接进入下一轮的跳转语句（只写这个关键字本身，一个单词），只写这一行代码。",
        "starter_code": "# 在这里写出跳过本轮循环的语句\n",
        "expected_answer": "continue",
        "difficulty": "easy",
        "order_index": 39,
    },
    {
        "lesson_slug": "continue-statement",
        "title": "判断偶数",
        "description": "请写出判断变量 i 是否为偶数的 if 语句行：用取余运算 % 判断 i 除以 2 的余数是否等于 0（用两个等号 ==），并以冒号结尾（只写这一行）。",
        "starter_code": "# 在这里写出判断 i 是否为偶数的 if 行\n",
        "expected_answer": "if i % 2 == 0:",
        "difficulty": "medium",
        "order_index": 40,
    },
    # 第 21 篇：Python pass 语句
    {
        "lesson_slug": "pass-statement",
        "title": "空语句占位",
        "description": "请写出表示空语句、起占位作用的语句（只写这个关键字本身，一个单词），只写这一行代码。",
        "starter_code": "# 在这里写出空语句占位\n",
        "expected_answer": "pass",
        "difficulty": "easy",
        "order_index": 41,
    },
    {
        "lesson_slug": "pass-statement",
        "title": "else 空分支",
        "description": "请写出与 if 配对、在条件不成立时执行的分支语句行（该分支内暂用 pass 占位），并以冒号结尾（只写这一行）。",
        "starter_code": "# 在这里写出分支语句行（以冒号结尾）\n",
        "expected_answer": "else:",
        "difficulty": "easy",
        "order_index": 42,
    },
]
