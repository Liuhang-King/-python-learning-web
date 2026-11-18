"""种子数据脚本：写入 49 篇教程与 98 道练习题（基础 12 + 扩展 37）。

用法（在项目根目录执行）：
    python backend/seeds/seed.py

特性：
    - 导入前检查 lessons 表是否存在，不存在则提示先运行 migrate.py。
    - 幂等：按 slug（教程）与 (lesson_id, title)（练习）去重，已有数据则跳过。
"""

import importlib.util
import os
import sqlite3
import sys
from pathlib import Path

# seeds -> backend -> 项目根
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# 目录扩展内容分散在 extra_batch1..5.py，按批次合并（每个模块导出 LESSONS / EXERCISES）
THEME_BATCHES = 5


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
    {
        "slug": "collections",
        "title": "集合与字典",
        "summary": "用列表、集合和字典高效组织一组数据。",
        "order_index": 7,
        "duration_min": 12,
        "content_md": """# 集合与字典

## 为什么需要容器
如果要用变量保存一个班级 50 个人的名字，定义 50 个变量显然不现实。容器就是用来一次性存放多个数据的工具。Python 最常用的三种容器是列表（list）、集合（set）和字典（dict），它们各有特点，解决不同的问题。

## 列表 list
列表用方括号 `[]` 表示，元素之间用逗号隔开，例如 `fruits = ["苹果", "香蕉", "橙子"]`。列表是有序的，可以通过下标访问元素，下标从 0 开始，所以 `fruits[0]` 是"苹果"。用 `append()` 可以在末尾添加元素，用 `len()` 获取元素个数。列表允许重复元素，适合需要保持顺序、可能重复的场景。

## 集合 set
集合用花括号 `{}` 表示，例如 `s = {1, 2, 3}`。集合最大的特点是**元素不重复且无序**，Python 会自动去掉重复项，所以 `{1, 2, 2, 3}` 实际只有 1、2、3 三个元素。集合常用于去重和集合运算，比如判断某元素是否在集合中用 `in`，速度比列表快得多。注意空集合要用 `set()` 创建，因为 `{}` 表示的是空字典。

## 字典 dict
字典用花括号加键值对表示，例如 `person = {"name": "小明", "age": 12}`。每个元素由"键"和"值"组成，用冒号连接。字典通过键来取值，例如 `person["name"]` 得到"小明"。字典里的键不能重复，值可以重复。添加或修改键值对用 `person["city"] = "北京"`。字典适合描述一个事物的多个属性，是实际开发中使用频率极高的数据结构。

## 怎么选择
需要保持顺序、允许重复 → 列表；需要去重、做成员判断 → 集合；需要根据名字（键）快速找到对应的值 → 字典。理解三者的区别，是写出高效代码的重要一步。

## 要点提示
- 列表下标从 0 开始，`fruits[0]` 是第一个元素。
- 集合自动去重、无序；空集合用 `set()`，不要用 `{}`。
- 字典用键取值，`person["name"]` 这种写法要牢记。
- 用 `in` 判断元素是否存在，对集合尤其高效。""",
        "code_example": """# 列表：有序、可重复
fruits = ["苹果", "香蕉", "橙子"]
print(fruits[0])
fruits.append("葡萄")
print("列表长度：", len(fruits))

# 集合：去重、无序
nums = {1, 2, 2, 3}
print(nums)          # {1, 2, 3}
print(3 in nums)     # True

# 字典：键值对
person = {"name": "小明", "age": 12}
print(person["name"])
person["city"] = "北京"
print(person)""",
    },
    {
        "slug": "abstraction",
        "title": "函数与抽象",
        "summary": "默认参数、关键字参数与递归，理解抽象的力量。",
        "order_index": 8,
        "duration_min": 12,
        "content_md": """# 函数与抽象

## 什么是抽象
前面已经学会了定义函数。函数更深一层的价值在于**抽象**：把复杂的细节封装起来，只暴露简单的接口给使用者。你调用 `print()` 时并不需要知道它内部怎么把字符显示在屏幕上，这就是抽象。学会用好参数、返回值的组合，能让你把复杂问题拆成一个个简单的函数。

## 默认参数
定义函数时，可以给参数指定默认值，例如 `def greet(name, greeting="你好"):`。调用时如果传了 greeting 就用传入的值，不传就用默认值。默认参数让函数更灵活，调用者也更省心。注意默认参数要放在普通参数的后面。

## 关键字参数
调用函数时，可以用 `函数名(参数名=值)` 的形式明确指定参数，例如 `greet(name="小明", greeting="早上好")`。这样即使记不清参数顺序也不会出错，代码可读性也更好。

## 返回多个值
函数可以用 `return a, b` 一次返回多个值，Python 会把它们打包成一个元组。调用时用 `x, y = 函数名()` 就能分别接收。这让函数能一次给出多个结果。

## 递归
函数可以调用自己，这叫递归。递归适合解决"问题可以拆成更小的同类问题"的场景，比如计算阶乘：n 的阶乘等于 n 乘以 (n-1) 的阶乘。写递归一定要有一个"终止条件"（比如 1 的阶乘是 1），否则会无限调用下去导致错误。递归是抽象思想的集中体现，但初学阶段理解概念即可，不必强求熟练。

## 要点提示
- 默认参数放在普通参数后面，调用时可以不传。
- 关键字参数用 `参数名=值`，避免记错顺序。
- `return a, b` 返回多个值，用 `x, y = 函数名()` 接收。
- 递归必须有终止条件，否则会无限递归。""",
        "code_example": """# 默认参数
def greet(name, greeting="你好"):
    print(f"{greeting}，{name}！")

greet("小明")
greet("小红", greeting="早上好")

# 关键字参数
greet(name="小刚", greeting="晚上好")

# 返回多个值
def min_max(a, b):
    if a < b:
        return a, b
    return b, a

small, big = min_max(5, 3)
print(small, big)

# 递归求阶乘
def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))""",
    },
    {
        "slug": "file-io",
        "title": "文件读写",
        "summary": "用 open 读写文本文件，掌握 with 语句安全操作文件。",
        "order_index": 9,
        "duration_min": 12,
        "content_md": """# 文件读写

## 为什么要操作文件
程序运行时的变量存在内存里，一旦程序结束数据就消失了。如果想把数据长期保存下来，就需要写入文件。文件读写是程序与外部世界交换数据的基本方式，日志、配置、数据报表都离不开它。

## 打开文件
Python 用内置函数 `open()` 打开文件，最常用的是 `open("文件名", "模式")`。模式 `"r"` 表示读取（read），`"w"` 表示写入（write，会清空原内容），`"a"` 表示追加（append，在末尾添加）。例如 `f = open("note.txt", "w")` 打开一个文件准备写入。操作完成后要调用 `f.close()` 关闭文件，释放系统资源。

## 用 with 语句更安全
手动 `close()` 容易忘记，而且中途出错时可能执行不到。推荐用 `with open(...) as f:` 的写法，它会在代码块结束后自动关闭文件，即使发生异常也一样。这是 Python 处理文件的标准写法，务必养成习惯。

## 读取文件
用 `f.read()` 一次性读出文件的全部内容，返回一个字符串。也可以用 `for line in f:` 逐行读取，适合大文件。读取模式的文件如果不存在会报错，写入模式则会自动创建。

## 写入文件
用 `f.write("内容")` 写入字符串。注意 `"w"` 模式会覆盖原有内容，想保留原内容并追加请用 `"a"` 模式。写入的内容都是文本，如果需要写入数字要先转成字符串，比如用 f-string 或 `str()`。

## 常见错误
最常见的是编码问题：读写中文文件时可能因为默认编码不一致出现乱码，可以指定 `encoding="utf-8"`。另一个是文件路径写错导致找不到文件。

## 要点提示
- 用 `with open(...) as f:` 自动管理文件关闭，推荐始终使用。
- 模式：`r` 读、`w` 写（覆盖）、`a` 追加。
- 读写中文建议加 `encoding="utf-8"`。
- 写入的内容必须是字符串，数字要先转换。""",
        "code_example": """# 写入文件（with 自动关闭）
with open("note.txt", "w", encoding="utf-8") as f:
    f.write("你好，文件！\\n")
    f.write("这是第二行。\\n")

# 读取文件
with open("note.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)

# 追加内容
with open("note.txt", "a", encoding="utf-8") as f:
    f.write("追加的一行\\n")

# 逐行读取
with open("note.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())""",
    },
    {
        "slug": "classes",
        "title": "类和对象",
        "summary": "理解面向对象，学会定义类、创建对象与使用属性方法。",
        "order_index": 10,
        "duration_min": 15,
        "content_md": """# 类和对象

## 什么是面向对象
前面写过的数据和函数都是零散的。面向对象（OOP）提供了一种把"数据"和"操作数据的函数"打包在一起的思路。类（class）是蓝图或模板，对象（object）是根据蓝图创建出来的具体实例。比如"狗"是一个类，而"我家的小白"是一个对象。类描述了所有狗共有的属性（名字、年龄）和行为（叫、跑）。

## 定义类
用 `class` 关键字定义类，类名习惯用大驼峰命名法（每个单词首字母大写），例如 `class Dog:`。类里面可以定义属性和方法。方法就是写在类里面的函数，第一个参数必须是 `self`，它代表对象本身。

## 构造方法 __init__
`__init__` 是创建对象时自动调用的特殊方法，用来初始化对象的属性。例如 `def __init__(self, name, age):` 里写 `self.name = name`、`self.age = age`，就把传入的值保存到了对象上。这里的 `self.name` 是对象自己的属性，右边的 `name` 是传入的参数，二者同名但含义不同。

## 创建对象
有了类就可以创建对象，写法是 `dog = Dog("小白", 3)`，这会自动调用 `__init__`，把"小白"和 3 传进去。创建对象也叫实例化。

## 属性与方法
创建对象后，用 `dog.name` 访问属性，用 `dog.bark()` 调用方法。方法定义时虽然第一个参数是 self，但调用时不需要传它，Python 会自动把对象传进去。

## 为什么要面向对象
当程序变大时，面向对象能把相关的数据和行为组织在一起，让代码更好维护、更好复用。比如游戏里的角色、网站里的用户，都适合用类来建模。

## 要点提示
- 类名用大驼峰命名法，如 `Dog`、`Student`。
- `__init__` 在创建对象时自动执行，用于初始化属性。
- 方法的第一个参数必须是 `self`，代表对象自身。
- 访问属性和调用方法都用点号：`dog.name`、`dog.bark()`。""",
        "code_example": """# 定义一个类
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        print(f"{self.name}：汪汪！")

    def introduce(self):
        print(f"我是{self.name}，今年{self.age}岁")

# 创建对象（实例化）
dog = Dog("小白", 3)

# 访问属性、调用方法
print(dog.name)
print(dog.age)
dog.bark()
dog.introduce()""",
    },
    {
        "slug": "science",
        "title": "科学与工程实践",
        "summary": "用 math、random 等库做数值计算与简单数据处理。",
        "order_index": 11,
        "duration_min": 12,
        "content_md": """# 科学与工程实践

## Python 与科学计算
Python 之所以在科研和工程领域大受欢迎，是因为它有丰富的数学和科学计算库，能用很少的代码完成复杂计算。这一篇通过几个小实践，把前面学的变量、循环、函数、容器串起来用一用。

## math 库：数学计算
Python 内置了 `math` 库，提供常用数学函数和常量。使用前要先 `import math`。常用的有 `math.sqrt(16)` 求平方根得到 4.0，`math.pi` 是圆周率，`math.sin()`、`math.cos()` 是三角函数，`math.pow(2, 3)` 求幂。这些函数让你不必自己实现复杂公式。

## random 库：随机数
`random` 库用来生成随机数，做模拟和抽签时很有用。`random.randint(1, 10)` 返回 1 到 10 之间的随机整数（包含两端），`random.random()` 返回 0 到 1 之间的随机小数。可以用它模拟掷骰子、随机抽样。

## 实践一：统计一组数据
把一组数字放进列表，用循环求和再除以个数，就得到平均值。Python 也提供了 `sum(nums)` 和 `len(nums)`，让这件事一行就能完成。再配合 `max()`、`min()` 就能得到最大值和最小值。这就是最基础的数据分析。

## 实践二：温度转换
写一个函数把摄氏度转成华氏度，公式是 `F = C * 9/5 + 32`。把公式封装成函数后，就能方便地对任意温度转换。这体现了函数带来的复用价值。

## 综合小项目
试着写一个"猜数字"游戏：用 `random.randint` 生成一个 1 到 100 的数，让玩家用 `input()` 反复猜，程序用 if 判断提示"大了"或"小了"，直到猜中。这个小程序综合了随机数、循环、条件、输入输出，是巩固基础知识的绝佳练习。

## 要点提示
- 使用标准库前先 `import 库名`。
- `math.sqrt()` 求平方根，`math.pi` 是圆周率。
- `random.randint(a, b)` 返回 a 到 b 的随机整数（含两端）。
- 用 `sum()`、`len()`、`max()`、`min()` 快速统计列表数据。""",
        "code_example": """import math
import random

# math 库
print("16 的平方根：", math.sqrt(16))
print("圆周率：", math.pi)

# random 库
print("掷骰子：", random.randint(1, 6))

# 统计数据
scores = [85, 92, 78, 96, 88]
print("平均分：", sum(scores) / len(scores))
print("最高分：", max(scores))
print("最低分：", min(scores))

# 温度转换函数
def c_to_f(c):
    return c * 9 / 5 + 32

print("100 摄氏度 =", c_to_f(100), "华氏度")""",
    },
    {
        "slug": "gui-intro",
        "title": "图形界面程序设计初探",
        "summary": "用 tkinter 创建第一个窗口，认识事件驱动编程。",
        "order_index": 12,
        "duration_min": 12,
        "content_md": """# 图形界面程序设计初探

## 什么是图形界面
前面写的程序都是在终端里输入输出，也就是命令行界面（CLI）。图形界面（GUI）则用窗口、按钮、输入框等可视化元素和用户交互，更直观友好。Python 标准库自带 `tkinter`，无需额外安装就能做出简单的桌面窗口程序，非常适合入门。

## 创建第一个窗口
使用 tkinter 通常分三步：先 `import tkinter as tk`，再用 `root = tk.Tk()` 创建主窗口，最后调用 `root.mainloop()` 进入事件循环。窗口不会自己关闭，`mainloop()` 会一直运行，等待用户的操作。

## 添加控件
控件是界面上的元素。标签 `Label` 用来显示文字，按钮 `Button` 用来触发操作，输入框 `Entry` 用来接收文本。创建控件时要指定它属于哪个窗口，例如 `label = tk.Label(root, text="你好")`。创建之后还要"摆放"到窗口上，最简单的是用 `pack()` 方法，它会从上到下自动排列控件。

## 事件与回调函数
GUI 是"事件驱动"的：程序不再从头到尾顺序执行，而是等待用户点击、输入等事件，事件发生时才调用对应的函数。这种函数叫回调函数。创建按钮时用 `command=函数名` 绑定回调，例如 `tk.Button(root, text="点我", command=say_hello)`。注意这里写函数名，不要加括号，因为要把它"交给"按钮，而不是立即执行。点击按钮时，`say_hello` 才会被调用。

## 一个完整的小例子
做一个"点击计数"程序：用一个标签显示数字，一个按钮，每点一次按钮数字加一。这需要在回调函数里修改标签文字，用 `label.config(text=...)` 即可。这个例子虽小，却完整展示了窗口、控件、事件、回调的核心概念。

## 要点提示
- 用 `import tkinter as tk` 导入，`tk.Tk()` 创建主窗口。
- 必须调用 `root.mainloop()` 让窗口保持响应。
- 控件创建后用 `pack()` 摆放到窗口上。
- `command=函数名` 绑定按钮回调，函数名后不要加括号。""",
        "code_example": """import tkinter as tk

# 创建主窗口
root = tk.Tk()
root.title("我的第一个 GUI")
root.geometry("300x200")

# 添加标签
label = tk.Label(root, text="你好，tkinter！")
label.pack()

# 按钮的回调函数
def say_hello():
    label.config(text="你点击了按钮！")

# 添加按钮并绑定回调
button = tk.Button(root, text="点我", command=say_hello)
button.pack()

# 进入事件循环
root.mainloop()""",
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
    # 第 7 篇：集合与字典
    {
        "lesson_slug": "collections",
        "title": "定义列表",
        "description": "请定义列表 nums，包含整数 1、2、3 三个元素（只写这一行赋值语句）。",
        "starter_code": "# 在这里定义列表 nums = [1, 2, 3]\n",
        "expected_answer": "nums = [1, 2, 3]",
        "difficulty": "easy",
        "order_index": 13,
    },
    {
        "lesson_slug": "collections",
        "title": "字典取值",
        "description": "已有字典 person，请用 print() 输出键 'name' 对应的值，写成 print(person['name'])（只写这一行）。",
        "starter_code": "# 在这里用 print 输出 person['name']\n",
        "expected_answer": "print(person['name'])",
        "difficulty": "medium",
        "order_index": 14,
    },
    # 第 8 篇：函数与抽象
    {
        "lesson_slug": "abstraction",
        "title": "默认参数函数头",
        "description": "请写出定义函数 greet 的函数头：参数 name 无默认值，参数 greeting 默认值为 '你好'，以冒号结尾（只写这一行）。",
        "starter_code": "# 在这里写出带默认参数的函数头（以冒号结尾）\n",
        "expected_answer": "def greet(name, greeting='你好'):",
        "difficulty": "medium",
        "order_index": 15,
    },
    {
        "lesson_slug": "abstraction",
        "title": "返回多个值",
        "description": "请写出一条 return 语句，同时返回变量 a 和 b 两个值（只写这一行）。",
        "starter_code": "# 在这里写一行 return 语句，返回 a 和 b\n",
        "expected_answer": "return a, b",
        "difficulty": "medium",
        "order_index": 16,
    },
    # 第 9 篇：文件读写
    {
        "lesson_slug": "file-io",
        "title": "打开文件写模式",
        "description": "请用 open() 以写入模式打开 'note.txt'，赋值给变量 f，并指定 encoding 为 'utf-8'（只写这一行）。",
        "starter_code": "# 在这里用 open 以 'w' 模式打开 note.txt\n",
        "expected_answer": "f = open('note.txt', 'w', encoding='utf-8')",
        "difficulty": "medium",
        "order_index": 17,
    },
    {
        "lesson_slug": "file-io",
        "title": "with 语句开头",
        "description": "请写出以只读模式打开 'note.txt'、编码为 'utf-8'、用 as f 的 with 语句头，并以冒号结尾（只写这一行）。",
        "starter_code": "# 在这里写出 with open 语句头（以冒号结尾）\n",
        "expected_answer": "with open('note.txt', 'r', encoding='utf-8') as f:",
        "difficulty": "medium",
        "order_index": 18,
    },
    # 第 10 篇：类和对象
    {
        "lesson_slug": "classes",
        "title": "定义类",
        "description": "请写出定义名为 Student 的类的类头，使用 class 关键字并以冒号结尾（只写这一行）。",
        "starter_code": "# 在这里写出定义 Student 类的类头（以冒号结尾）\n",
        "expected_answer": "class Student:",
        "difficulty": "easy",
        "order_index": 19,
    },
    {
        "lesson_slug": "classes",
        "title": "构造方法参数",
        "description": "请写出 __init__ 方法的定义行：参数为 self、name、age，以冒号结尾（只写这一行）。",
        "starter_code": "# 在这里写出 __init__ 方法的定义行（以冒号结尾）\n",
        "expected_answer": "def __init__(self, name, age):",
        "difficulty": "medium",
        "order_index": 20,
    },
    # 第 11 篇：科学与工程实践
    {
        "lesson_slug": "science",
        "title": "导入 math 库",
        "description": "请写出导入 math 库的语句（只写这一行）。",
        "starter_code": "# 在这里写导入 math 库的语句\n",
        "expected_answer": "import math",
        "difficulty": "easy",
        "order_index": 21,
    },
    {
        "lesson_slug": "science",
        "title": "求平方根并输出",
        "description": "请用 print() 输出 math.sqrt(16) 的结果（只写这一行）。",
        "starter_code": "# 在这里用 print 输出 16 的平方根\n",
        "expected_answer": "print(math.sqrt(16))",
        "difficulty": "medium",
        "order_index": 22,
    },
    # 第 12 篇：图形界面程序设计初探
    {
        "lesson_slug": "gui-intro",
        "title": "导入 tkinter",
        "description": "请写出导入 tkinter 并简写为 tk 的语句，写成 import tkinter as tk（只写这一行）。",
        "starter_code": "# 在这里写导入 tkinter 的语句\n",
        "expected_answer": "import tkinter as tk",
        "difficulty": "easy",
        "order_index": 23,
    },
    {
        "lesson_slug": "gui-intro",
        "title": "创建主窗口",
        "description": "请写出创建 tkinter 主窗口并赋值给变量 root 的语句，写成 root = tk.Tk()（只写这一行）。",
        "starter_code": "# 在这里创建主窗口 root\n",
        "expected_answer": "root = tk.Tk()",
        "difficulty": "easy",
        "order_index": 24,
    },
]


# ---------------------------------------------------------------------------
# 合并扩展目录：把 extra_batch1..5 的教程与练习并入主列表
# ---------------------------------------------------------------------------
def _load_theme_batches() -> None:
    here = Path(__file__).resolve().parent
    for i in range(1, THEME_BATCHES + 1):
        module_path = here / f"extra_batch{i}.py"
        if not module_path.exists():
            print(f"警告：扩展批次文件缺失：{module_path.name}，已跳过。")
            continue
        spec = importlib.util.spec_from_file_location(f"extra_batch{i}", module_path)
        if spec is None or spec.loader is None:
            continue
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        LESSONS.extend(getattr(module, "LESSONS", []))
        EXERCISES.extend(getattr(module, "EXERCISES", []))


_load_theme_batches()


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
