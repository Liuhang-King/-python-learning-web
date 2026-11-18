"""种子数据脚本：写入 6 篇教程与 12 道练习题。

用法（在项目根目录执行）：
    python backend/seeds/seed.py

特性：
    - 导入前检查 lessons 表是否存在，不存在则提示先运行 migrate.py。
    - 幂等：按 slug（教程）与 (lesson_id, title)（练习）去重，已有数据则跳过。
"""

import os
import sqlite3
import sys
from pathlib import Path

# seeds -> backend -> 项目根
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def get_database_path() -> Path:
    raw = os.environ.get("DATABASE_PATH", "backend/data/learning.db")
    path = Path(raw)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path


# ---------------------------------------------------------------------------
# 教程数据
# ---------------------------------------------------------------------------
LESSONS = [
    {
        "slug": "intro",
        "title": "Python 简介与运行环境",
        "summary": "认识 Python 语言，搭好运行环境，写出第一个程序。",
        "order_index": 1,
        "duration_min": 8,
        "content_md": """# Python 简介与运行环境

## 什么是 Python
Python 是一门语法简洁、可读性很强的通用编程语言。它诞生于 1991 年，由 Guido van Rossum 创建，如今被广泛用于网站开发、数据分析、人工智能、自动化办公和科学计算等几乎所有领域。Python 的设计哲学是"优雅、明确、简单"，写代码时更接近自然语言，因此非常适合零基础初学者作为第一门编程语言。

## 为什么选择 Python
首先是语法简单：它用缩进表示代码块，不需要写大量花括号和分号。其次是生态丰富：有大量现成的第三方库，能让你用很少的代码完成复杂任务。最后是社区庞大：遇到问题时，很容易在文档和论坛里找到答案。对初学者来说，这意味着可以把精力放在"编程思维"上，而不是被繁杂的语法细节绊住脚。

## 安装与运行环境
你可以从 Python 官网下载并安装最新稳定版，安装时记得勾选"Add Python to PATH"。安装完成后，打开终端输入 `python --version`，如果能看到版本号就说明安装成功。运行 Python 代码有两种常见方式：一种是交互式 REPL，输入 `python` 进入后逐行执行，适合做小实验；另一种是把代码保存为 `.py` 文件，再用 `python 文件名.py` 一次性运行，适合正式项目。推荐初学者两者都用：先用 REPL 验证想法，再写进文件里保存。

## 你的第一个程序
按照惯例，学习一门语言的第一步是让屏幕打印一句话。下面这行代码会在屏幕上输出 Hello, World!：

```python
print("Hello, World!")
```

`print` 是 Python 内置函数，作用是把括号里的内容输出到屏幕。文字需要用引号包起来，单引号和双引号都可以，效果一样。

## 代码注释
注释是写给人类看的说明文字，Python 不会执行它。单行注释用 `#` 开头，从 `#` 到行尾的内容都会被忽略。给代码写清楚注释是一个好习惯，能帮助未来的自己和他人快速理解代码意图。

## 要点提示
- Python 用缩进（通常是 4 个空格）表示代码块，不要用 Tab 和空格混用。
- 字符串必须放在一对匹配的引号里，单引号和双引号都可以。
- 文件名建议用英文、数字和下划线，不要用中文或空格。
- 遇到报错不要慌，错误信息里通常会写明出错的行号和原因，逐字读一读往往就能找到线索。""",
        "code_example": """# 我的第一个 Python 程序
print("Hello, World!")
print("你好，Python！")

# 这是一行注释，不会被运行
name = "小明"
print("欢迎你，" + name)""",
    },
    {
        "slug": "variables",
        "title": "变量与数据类型",
        "summary": "学会用变量保存数据，认识数字、字符串和布尔值。",
        "order_index": 2,
        "duration_min": 10,
        "content_md": """# 变量与数据类型

## 什么是变量
变量就像一个个带标签的盒子，用来存放数据。你可以把值放进盒子里，之后通过标签找到它。在 Python 中，用等号 `=` 给变量赋值，等号左边是变量名，右边是要存的值。例如 `x = 10` 表示把数字 10 放进名为 x 的盒子里。注意这里的等号是"赋值"的意思，不是数学里的"相等"。

## 变量命名规则
变量名可以由字母、数字和下划线组成，但不能以数字开头，也不能使用 Python 的关键字（比如 if、for、class）。变量名区分大小写，所以 `Name` 和 `name` 是两个不同的变量。命名时要做到"见名知意"，比如表示年龄用 `age`，表示姓名用 `name`，不要用 `a`、`b` 这种让人猜不透的名字。多个单词建议用下划线连接，例如 `user_name`。

## 常见数据类型
Python 有几种最常用的数据类型。整数 `int`，例如 `10` 和 `-3`；浮点数 `float`，也就是带小数点的数，例如 `3.14`；字符串 `str`，用引号包起来的文本，例如 `"你好"`；布尔值 `bool`，只有 `True` 和 `False` 两个值，表示真和假。可以用内置函数 `type()` 查看一个值或变量的类型，这在调试时非常有用。

## 查看和使用变量
把变量直接放进 `print()` 就能输出它的值。也可以在字符串里用 f-string 插入变量，写法是在字符串前加字母 f，然后用花括号包住变量名，例如 `f"我今年{age}岁"`。f-string 直观又好读，是推荐初学者掌握的字符串格式化方式。

## 一点小提醒
Python 是动态类型语言，同一个变量可以先存整数，再存字符串，类型会自动变化。但为了代码清晰，实际开发中最好让一个变量始终保持同一种类型。

## 要点提示
- 变量名区分大小写，命名要清晰、见名知意。
- `=` 表示赋值，把右边的值交给左边的变量。
- 用 `type()` 可以查看数据类型，用 f-string 可以方便地拼接变量。
- 不要使用 Python 关键字作为变量名。""",
        "code_example": """# 定义变量并输出
name = "小明"
age = 12
height = 1.65
is_student = True

print(name)
print("年龄：", age)
print(f"{name}今年{age}岁，身高{height}米")
print("是学生吗？", is_student)
print("age 的类型是：", type(age))""",
    },
    {
        "slug": "operators",
        "title": "运算符与表达式",
        "summary": "掌握算术、比较和逻辑运算符，学会组合表达式。",
        "order_index": 3,
        "duration_min": 8,
        "content_md": """# 运算符与表达式

## 什么是表达式
表达式是由数字、变量和运算符组成的式子，计算后会得到一个结果。例如 `3 + 5` 是一个表达式，结果是 8；`age + 1` 也是表达式，结果是变量 age 的值加一。把表达式放进 `print()`，就能看到它的计算结果。

## 算术运算符
Python 支持常见的算术运算：`+` 加法、`-` 减法、`*` 乘法、`/` 除法（结果总是浮点数）、`//` 整除（只取整数部分）、`%` 取余（求余数）、`**` 幂运算。例如 `7 // 2` 的结果是 3，而 `7 % 2` 的结果是 1。运算时遵循数学里的优先级：先乘除后加减，括号可以改变顺序，这一点和数学完全一致。

## 比较运算符
比较运算符用来比较两个值，结果是布尔值 True 或 False。`>` 大于、`<` 小于、`>=` 大于等于、`<=` 小于等于、`==` 等于、`!=` 不等于。特别注意：判断相等要用两个等号 `==`，一个等号 `=` 是赋值，写错的话程序会出错或者得到意想不到的结果，这是初学者最常踩的坑之一。

## 逻辑运算符
逻辑运算符用于组合多个条件：`and` 表示"并且"，两边都为真结果才为真；`or` 表示"或者"，只要一边为真结果就为真；`not` 表示"取反"，把真变假、假变真。例如 `x > 5 and x < 10` 表示 x 大于 5 且小于 10。

## 赋值运算符
除了普通的 `=`，还有复合赋值运算符，例如 `x += 1` 等价于 `x = x + 1`，表示把 x 的值加一后再存回去。`-=`、`*=`、`/=` 用法类似，能让代码更简洁。

## 要点提示
- `/` 的结果一定是浮点数，想要整数结果请用 `//`。
- 判断两个值是否相等用 `==`，不要用单个 `=`。
- 多用括号明确运算顺序，代码更易读也不容易出错。
- 比较和逻辑运算符的结果都是布尔值，它们是后面学习条件判断的基础。""",
        "code_example": """# 算术运算
print(3 + 5)
print(7 / 2)
print(7 // 2)
print(7 % 2)
print(2 ** 3)

# 比较运算
x = 10
print(x > 5)
print(x == 10)
print(x != 3)

# 逻辑运算
print(x > 5 and x < 20)
print(x < 0 or x > 5)

# 复合赋值
x += 1
print("x 加一后：", x)""",
    },
    {
        "slug": "conditions",
        "title": "条件判断 if/else",
        "summary": "让程序学会做选择，掌握 if、elif 与 else。",
        "order_index": 4,
        "duration_min": 10,
        "content_md": """# 条件判断 if/else

## 让程序做选择
程序默认从上往下依次执行每一行代码。但在实际生活中，我们常常需要根据不同情况做不同的事：如果下雨就带伞，否则就不带。条件判断就是让程序拥有这种"做选择"的能力。

## if 语句
最基本的写法是 `if 条件:`，下一行用缩进写下条件成立时要执行的代码。注意条件后面必须有冒号 `:`，而且后面的代码块必须缩进（通常是 4 个空格）。例如 `if x > 5:` 后面缩进的那几行，只有在 x 大于 5 时才会运行。缩进在 Python 里不是装饰，而是语法的一部分，用来标识代码属于哪个代码块。

## else 与 elif
当条件不成立时，可以用 `else:` 分支执行另一段代码，它同样需要冒号和缩进。如果有多种情况要依次判断，可以用 `elif:`（else if 的缩写）连接多个分支。整个结构从上往下检查，哪个条件先满足就执行哪个分支，执行完就跳出整个判断结构，后面的分支不再检查。

## 嵌套判断
if 语句内部还可以再写 if 语句，这叫嵌套。嵌套可以处理更复杂的多重条件，但层级太深会降低可读性，能用 elif 平铺解决时就不要层层嵌套。

## 常见错误
第一，忘记写条件后面的冒号；第二，代码块没有缩进或缩进不一致；第三，把判断相等的 `==` 写成赋值的 `=`。这三种错误都会导致语法错误，运行时 Python 会明确提示你。

## 要点提示
- if / elif / else 后面都要加英文冒号 `:`。
- 属于分支的代码必须缩进，同一分支内缩进要一致。
- 条件通常是比较表达式，结果是 True 或 False。
- 多个分支只会有其中一个被执行，判断顺序会影响结果。""",
        "code_example": """# 基本 if 判断
x = 10
if x > 5:
    print("x 大于 5")

# if / else 二选一
if x % 2 == 0:
    print("x 是偶数")
else:
    print("x 是奇数")

# 多分支判断
score = 85
if score >= 90:
    print("优秀")
elif score >= 60:
    print("及格")
else:
    print("不及格")""",
    },
    {
        "slug": "loops",
        "title": "循环 for/while",
        "summary": "用循环重复执行代码，掌握 for 与 while 的用法。",
        "order_index": 5,
        "duration_min": 12,
        "content_md": """# 循环 for/while

## 为什么要循环
如果要打印 1 到 100 的每个数字，手写一百行 `print` 显然不现实。循环的作用就是让一段代码重复执行多次。Python 提供了两种循环：`for` 循环和 `while` 循环。

## for 循环
for 循环适合"已知要循环多少次"的场景，它遍历一个序列中的每个元素。最常搭配的是 `range()` 函数，例如 `range(5)` 会产生 0、1、2、3、4 这五个数（注意不包含 5）。写法是 `for i in range(5):`，意思是让变量 i 依次取这些值，冒号后面缩进的代码每取一个值就执行一次。也可以直接遍历列表、字符串等序列，例如 `for ch in "abc":`。

## while 循环
while 循环适合"只要条件成立就一直循环"的场景。写法是 `while 条件:`，每次执行前先检查条件，为真就执行代码块，为假就结束循环。例如 `while i < 10:` 会在变量 i 小于 10 时持续循环。使用 while 时一定要在循环体内改变条件变量（比如 `i += 1`），否则条件永远成立，程序会陷入死循环。

## break 与 continue
`break` 用于立刻跳出整个循环，不再执行剩余次数；`continue` 用于跳过本次循环剩下的代码，直接进入下一次循环。二者常配合 if 使用，用来处理特殊情况。

## 循环中的 else
Python 的循环还可以带 `else` 分支：循环正常执行完毕（没有被 break 打断）时会执行 else 里的代码。这个特性初学者了解即可，用得不多。

## 要点提示
- `range(n)` 生成 0 到 n-1，不含 n；也可指定起点和步长。
- for 适合次数已知，while 适合条件驱动。
- while 循环务必更新条件变量，避免死循环。
- 循环体同样需要缩进，冒号不能漏。""",
        "code_example": """# for 循环打印 0 到 4
for i in range(5):
    print(i)

# for 遍历字符串
for ch in "Python":
    print(ch)

# while 循环
i = 0
while i < 5:
    print("当前 i =", i)
    i += 1

# break 提前结束
for n in range(10):
    if n == 3:
        break
    print(n)""",
    },
    {
        "slug": "functions",
        "title": "函数入门",
        "summary": "把代码打包成函数，学会定义、调用与返回值。",
        "order_index": 6,
        "duration_min": 10,
        "content_md": """# 函数入门

## 什么是函数
函数是一段可以重复使用的代码块，给它起个名字，之后只要写这个名字就能执行它。前面用过的 `print()`、`type()`、`range()` 都是 Python 内置函数。学会自己定义函数，是把代码组织得清晰、可复用的关键一步。

## 定义函数
用 `def` 关键字定义函数，写法是 `def 函数名(参数):`，后面缩进的代码是函数体。例如 `def greet():` 定义了一个名为 greet 的函数，它不需要任何参数。函数名同样要见名知意，一般用小写字母和下划线。定义函数时代码不会立刻执行，只有"调用"它时才会运行函数体。

## 参数
函数可以接收参数，让同一段代码处理不同的数据。定义时括号里写的是形参（如 `def greet(name):`），调用时传进去的是实参（如 `greet("小明")`）。参数可以有多个，用逗号隔开。这样函数就不再是死板的固定流程，而是能根据不同输入产生不同结果。

## 返回值
用 `return` 语句可以把函数计算的结果返回给调用者。例如 `def add(a, b):` 的函数体里写 `return a + b`，调用 `add(2, 3)` 就会得到 5。返回值可以用变量接收，也可以直接参与其他运算。如果函数没有写 return，默认返回 None。注意 return 会立即结束函数，后面的代码不再执行。

## 变量作用域
在函数内部定义的变量是局部变量，只在函数内部有效，函数外面访问不到。这种隔离避免了不同代码之间的变量互相干扰，是函数带来的重要好处。

## 要点提示
- 用 `def` 定义函数，函数名后要加括号和冒号，函数体要缩进。
- 定义不执行，调用才执行；调用时写 `函数名(参数)`。
- `return` 用于返回结果，同时结束函数。
- 给函数起一个能说明用途的名字，是良好编程习惯。""",
        "code_example": """# 定义一个无参数函数
def greet():
    print("你好，欢迎学习 Python！")

greet()

# 带参数的函数
def greet_person(name):
    print(f"你好，{name}！")

greet_person("小明")

# 带返回值的函数
def add(a, b):
    return a + b

result = add(3, 5)
print("3 + 5 =", result)""",
    },
]

# ---------------------------------------------------------------------------
# 练习题数据（适配"答案规范化比较"：expected_answer 为精确代码文本）
# ---------------------------------------------------------------------------
EXERCISES = [
    # 第 1 篇：Python 简介与运行环境
    {
        "lesson_slug": "intro",
        "title": "打印问候语",
        "description": "请使用 print() 输出文本 Hello, World!（引号内的文字需完全一致，只写出这一行代码）。",
        "starter_code": "# 在这里写一行代码，输出 Hello, World!\n",
        "expected_answer": "print('Hello, World!')",
        "difficulty": "easy",
        "order_index": 1,
    },
    {
        "lesson_slug": "intro",
        "title": "打印一个数字",
        "description": "请使用 print() 输出整数 42，只写出这一行代码。",
        "starter_code": "# 在这里写一行代码，输出数字 42\n",
        "expected_answer": "print(42)",
        "difficulty": "easy",
        "order_index": 2,
    },
    # 第 2 篇：变量与数据类型
    {
        "lesson_slug": "variables",
        "title": "给变量赋值",
        "description": "请定义变量 x，并把整数 10 赋值给它（只写这一行赋值语句）。",
        "starter_code": "# 在这里定义变量 x 并赋值为 10\n",
        "expected_answer": "x = 10",
        "difficulty": "easy",
        "order_index": 3,
    },
    {
        "lesson_slug": "variables",
        "title": "定义字符串变量",
        "description": "请定义变量 name，并把字符串 Python 赋值给它（引号内的文字需完全一致，只写这一行赋值语句）。",
        "starter_code": "# 在这里定义变量 name 并赋值为 'Python'\n",
        "expected_answer": "name = 'Python'",
        "difficulty": "easy",
        "order_index": 4,
    },
    # 第 3 篇：运算符与表达式
    {
        "lesson_slug": "operators",
        "title": "加法并输出",
        "description": "请使用 print() 输出表达式 3 + 5 的计算结果（只写出这一行代码）。",
        "starter_code": "# 在这里写一行代码，输出 3 + 5 的结果\n",
        "expected_answer": "print(3 + 5)",
        "difficulty": "easy",
        "order_index": 5,
    },
    {
        "lesson_slug": "operators",
        "title": "乘法并输出",
        "description": "请使用 print() 输出 7 乘以 6 的结果（只写出这一行代码）。",
        "starter_code": "# 在这里写一行代码，输出 7 * 6 的结果\n",
        "expected_answer": "print(7 * 6)",
        "difficulty": "medium",
        "order_index": 6,
    },
    # 第 4 篇：条件判断 if/else
    {
        "lesson_slug": "conditions",
        "title": "判断大于 5",
        "description": "请写出判断变量 x 是否大于 5 的 if 语句行：使用变量 x 和大于号，并以冒号结尾（只写这一行）。",
        "starter_code": "# 在这里写出 if 判断行（以冒号结尾）\n",
        "expected_answer": "if x > 5:",
        "difficulty": "medium",
        "order_index": 7,
    },
    {
        "lesson_slug": "conditions",
        "title": "判断等于 10",
        "description": "请写出判断变量 x 是否等于 10 的 if 语句行：使用变量 x 和相等比较运算符 ==，并以冒号结尾（只写这一行）。",
        "starter_code": "# 在这里写出判断 x 等于 10 的 if 行（以冒号结尾）\n",
        "expected_answer": "if x == 10:",
        "difficulty": "medium",
        "order_index": 8,
    },
    # 第 5 篇：循环 for/while
    {
        "lesson_slug": "loops",
        "title": "for 循环头",
        "description": "请写出使用变量 i、遍历 range(5) 的 for 循环语句行，并以冒号结尾（只写这一行循环头）。",
        "starter_code": "# 在这里写出 for 循环头（以冒号结尾）\n",
        "expected_answer": "for i in range(5):",
        "difficulty": "medium",
        "order_index": 9,
    },
    {
        "lesson_slug": "loops",
        "title": "while 循环头",
        "description": "请写出当变量 i 小于 10 时持续循环的 while 语句行，并以冒号结尾（只写这一行循环头）。",
        "starter_code": "# 在这里写出 while 循环头（以冒号结尾）\n",
        "expected_answer": "while i < 10:",
        "difficulty": "medium",
        "order_index": 10,
    },
    # 第 6 篇：函数入门
    {
        "lesson_slug": "functions",
        "title": "定义函数",
        "description": "请写出定义一个名为 greet 的无参数函数的函数头，使用 def 关键字并以冒号结尾（只写这一行）。",
        "starter_code": "# 在这里写出定义 greet 函数的函数头（以冒号结尾）\n",
        "expected_answer": "def greet():",
        "difficulty": "medium",
        "order_index": 11,
    },
    {
        "lesson_slug": "functions",
        "title": "返回结果",
        "description": "请写出一条 return 语句，把变量 result 作为函数的返回值（只写这一行）。",
        "starter_code": "# 在这里写一行 return 语句，返回变量 result\n",
        "expected_answer": "return result",
        "difficulty": "easy",
        "order_index": 12,
    },
]


def table_exists(conn: sqlite3.Connection, table: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?", (table,)
    ).fetchone()
    return row is not None


def seed(conn: sqlite3.Connection) -> None:
    if not table_exists(conn, "lessons"):
        print("错误：未找到 lessons 表，请先运行 python backend/migrations/migrate.py 初始化数据库。")
        raise SystemExit(1)

    # 教程：按 slug 去重
    existing_slugs = {row[0] for row in conn.execute("SELECT slug FROM lessons")}
    slug_to_id = {row[0]: row[1] for row in conn.execute("SELECT slug, id FROM lessons")}

    new_lessons = 0
    for lesson in LESSONS:
        if lesson["slug"] in existing_slugs:
            continue
        cur = conn.execute(
            """INSERT INTO lessons
               (slug, title, summary, content_md, code_example, order_index, duration_min)
               VALUES (:slug, :title, :summary, :content_md, :code_example, :order_index, :duration_min)""",
            lesson,
        )
        slug_to_id[lesson["slug"]] = cur.lastrowid
        new_lessons += 1

    # 练习题：按 (lesson_id, title) 去重
    existing_exercises = {
        (row[0], row[1]) for row in conn.execute("SELECT lesson_id, title FROM exercises")
    }
    new_exercises = 0
    for exercise in EXERCISES:
        lesson_id = slug_to_id.get(exercise["lesson_slug"])
        if lesson_id is None:
            print(f"警告：找不到教程 slug={exercise['lesson_slug']}，跳过题目《{exercise['title']}》")
            continue
        if (lesson_id, exercise["title"]) in existing_exercises:
            continue
        conn.execute(
            """INSERT INTO exercises
               (lesson_id, title, description, starter_code, expected_answer, difficulty, order_index)
               VALUES (:lesson_id, :title, :description, :starter_code, :expected_answer, :difficulty, :order_index)""",
            {
                "lesson_id": lesson_id,
                "title": exercise["title"],
                "description": exercise["description"],
                "starter_code": exercise["starter_code"],
                "expected_answer": exercise["expected_answer"],
                "difficulty": exercise["difficulty"],
                "order_index": exercise["order_index"],
            },
        )
        new_exercises += 1

    conn.commit()
    print(f"种子数据完成：新增 {new_lessons} 篇教程，新增 {new_exercises} 道练习题。")
    print(f"当前共 {conn.execute('SELECT COUNT(*) FROM lessons').fetchone()[0]} 篇教程，"
          f"{conn.execute('SELECT COUNT(*) FROM exercises').fetchone()[0]} 道练习题。")


def main() -> int:
    db_path = get_database_path()
    if not db_path.exists():
        print("错误：数据库文件不存在，请先运行 python backend/migrations/migrate.py 初始化数据库。")
        return 1
    print(f"数据库路径：{db_path}")
    conn = sqlite3.connect(db_path)
    try:
        seed(conn)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
