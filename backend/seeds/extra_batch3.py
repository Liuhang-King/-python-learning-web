"""第 3 批扩展种子数据：9 篇进阶教程与 18 道配套练习题。

用法：由 seed.py 汇总导入，或单独引入其中的 LESSONS / EXERCISES。
本文件只定义数据，不执行任何写入操作。
"""

# ---------------------------------------------------------------------------
# 教程数据（order_index 31 - 39）
# ---------------------------------------------------------------------------
LESSONS = [
    {
        "slug": "file-methods",
        "title": "Python File 方法",
        "summary": "掌握文件定位、刷新与截断方法。",
        "order_index": 31,
        "duration_min": 12,
        "content_md": """# Python File 方法

## 什么是文件方法
在前面的课程里，我们已经学会了用 open() 打开文件，再用 read() 和 write() 读写内容。其实 open() 返回的是一个"文件对象"，它除了 read 和 write，还提供了许多更精细的控制方法，比如查看当前读写位置、跳转到指定位置、把缓冲区内容立刻写进磁盘、截断文件等。掌握这些方法，你就能像操作磁带一样，精确控制读写的每一个细节。这一篇我们系统学习这些常用的 File 对象方法。

## 文件打开模式回顾
调用 open(文件名, 模式) 会得到文件对象。常见模式有：'r' 只读（默认）、'w' 写入并清空、'a' 追加、'b' 二进制模式、'+' 读写。处理完文件后一定要用 close() 关闭，或者使用 with 语句自动关闭，这样系统资源才能及时释放。

## 位置控制：tell 与 seek
每个文件对象内部都有一个"读写位置"指针，记录着下一次读写从哪里开始。tell() 方法返回当前位置的字节数；seek(偏移量, 起始位置) 用来移动这个指针。起始位置有三个常用值：0 表示文件开头，1 表示当前位置，2 表示文件末尾。例如 f.seek(0) 表示回到文件开头，这是重新开始读取的常见写法。注意在文本模式下，seek 的偏移量通常只能是 0 或 tell() 返回的值，想随意跳转请用二进制模式 'rb'。

## 刷新与截断：flush 与 truncate
写入文件时，数据往往先存放在内存缓冲区里，并不会立刻写进磁盘。flush() 方法可以强制把缓冲区内容立刻写入磁盘，这在写日志、需要马上看到结果的场景很有用。truncate(大小) 方法把文件截断到指定字节数，省略参数时截断到当前位置，常用于"清空并重写"文件。

## 逐行读取：readline 与 readlines
readline() 每次只读取一行，适合逐行处理大文件，节省内存；readlines() 一次性把所有行读成列表。writelines(列表) 则可以把一个字符串列表一次性写入文件，注意它不会自动加换行符。

## 代码示例
下面演示 tell、seek 与 flush 的配合用法：

```python
with open("demo.txt", "w+", encoding="utf-8") as f:
    f.write("hello")
    print(f.tell())   # 当前位置：5
    f.flush()         # 立即写入磁盘
    f.seek(0)         # 回到开头
    print(f.read())   # hello
```

## 常见错误
第一，忘记关闭文件导致资源占用，建议用 with 语句。第二，在文本模式下用 seek 跳转到任意字节位置，可能得到乱码或报错，应改用二进制模式。第三，truncate 的参数是字节数而不是字符数，处理中文时要小心。

## 要点提示
- 用 with open(...) as f: 自动管理文件关闭。
- tell() 看位置，seek(偏移, whence) 移动位置，0/1/2 分别代表开头/当前/末尾。
- flush() 立即把缓冲区写入磁盘，truncate() 截断文件。
- 大文件优先用 readline() 逐行读，避免一次性读入内存。""",
        "code_example": """# 使用 with 语句安全管理文件
with open("demo.txt", "w+", encoding="utf-8") as f:
    f.write("第一行\\n")
    f.write("第二行\\n")
    f.flush()                      # 立刻把缓冲区写入磁盘
    print("当前位置：", f.tell())   # 查看读写位置
    f.seek(0)                      # 回到文件开头
    print(f.read())                # 从头读取全部内容

# 逐行读取（适合大文件）
with open("demo.txt", "r", encoding="utf-8") as f:
    for line in f:                 # 每次只读一行，节省内存
        print("读到：", line.strip())

# 截断文件
with open("demo.txt", "a+", encoding="utf-8") as f:
    f.seek(0)
    f.truncate(0)                  # 清空文件内容""",
    },
    {
        "slug": "exceptions",
        "title": "Python 异常处理",
        "summary": "捕获并处理程序运行时的错误。",
        "order_index": 32,
        "duration_min": 13,
        "content_md": """# Python 异常处理

## 什么是异常
程序运行时难免会遇到意外情况，比如除以零、打开不存在的文件、把字符串当成数字相加。这些错误在 Python 中被称为"异常"。如果不处理，程序会立刻中断并打印一大段红色错误信息。异常处理就是让我们提前预判这些意外，当问题发生时优雅地应对，而不是让程序崩溃。

## try / except 基本结构
Python 用 try 和 except 来捕获异常。把可能出错的代码放进 try 代码块，把出错后的处理代码放进 except 代码块。语法是 try: 后面缩进写可能出错的代码，然后 except 异常类型: 后面缩进写处理方式。当 try 里的代码出错时，程序会跳过剩余部分，直接执行匹配的 except 分支。except 后面可以指定具体异常类型，比如 ValueError、ZeroDivisionError、FileNotFoundError；也可以不写类型，表示捕获所有异常，但一般不推荐这样"一网打尽"，因为会掩盖真正的问题。

## else 与 finally
完整的异常处理结构还可以有 else 和 finally。else 代码块在没有发生异常时执行，finally 代码块无论是否出错都一定会执行。finally 非常适合放"收尾工作"，比如关闭文件、释放网络连接，保证资源不出意外泄漏。

## 主动抛出异常
除了被动捕获，我们也可以用 raise 语句主动抛出异常，用于判断到不合理输入时通知调用者。例如当年龄是负数时，可以 raise ValueError("年龄不能为负数")，这样调用方就能用 except 捕获并给出友好提示。

## 代码示例
一个带 else 和 finally 的完整结构：

```python
try:
    x = int("abc")          # 这里会触发 ValueError
except ValueError:
    print("转换失败，请输入数字")
else:
    print("转换成功")
finally:
    print("无论如何都会执行")
```

## 常见错误
第一，把 except 写成了 elif，语法完全不同。第二，except 后面忘记写冒号，或者代码块没缩进。第三，用空的 except: 捕获所有异常却不处理，导致错误被悄悄吞掉，排查困难。第四，认为 finally 只在出错时执行，实际上它总是执行。

## 要点提示
- try 放可能出错的代码，except 放出错后的处理。
- except 指定具体异常类型，比笼统捕获更安全。
- finally 无论是否出错都会执行，适合做清理工作。
- raise 用于主动抛出异常，配合条件判断使用。""",
        "code_example": """# 基本的异常处理
try:
    num = int(input("请输入一个整数："))
    result = 10 / num
    print("结果是：", result)
except ValueError:
    print("输入错误：请输入数字！")
except ZeroDivisionError:
    print("错误：除数不能为 0！")
else:
    print("计算顺利完成")
finally:
    print("无论成功失败，我都会执行")

# 主动抛出异常
def check_age(age):
    if age < 0:
        raise ValueError("年龄不能为负数")
    print("年龄是：", age)

try:
    check_age(-5)
except ValueError as e:
    print("捕获到异常：", e)""",
    },
    {
        "slug": "os-methods",
        "title": "Python OS 文件/目录方法",
        "summary": "用 os 模块管理文件与目录。",
        "order_index": 33,
        "duration_min": 12,
        "content_md": """# Python OS 文件/目录方法

## 认识 os 模块
os 模块是 Python 标准库中专门用来和操作系统打交道的工具箱。通过它，你可以获取当前所在目录、列出文件夹内容、创建和删除文件夹、重命名文件、判断路径是否存在等。因为它是标准库的一部分，不需要额外安装，import os 就能使用。学会 os 模块，你的程序就能"看懂"并操作电脑上的文件系统。

## 当前目录与路径
os.getcwd() 返回当前工作目录的字符串，也就是程序现在"站在"哪个文件夹。os.chdir(路径) 可以切换当前工作目录，就像在命令行里用 cd 命令一样。os.path 子模块提供了很多路径处理函数，例如 os.path.exists(路径) 判断路径是否存在，os.path.isdir(路径) 判断是不是文件夹，os.path.join(目录, 文件名) 把几段路径拼成完整路径，跨平台时特别有用。

## 列目录与创建删除
os.listdir(路径) 返回一个列表，里面是该目录下的所有文件和文件夹名字。os.mkdir(路径) 创建一个新文件夹，注意它要求上级目录已经存在；os.makedirs(路径) 可以一次性创建多层目录。删除用 os.remove(文件路径) 删文件，os.rmdir(路径) 删空文件夹。os.rename(旧名, 新名) 用来重命名或移动文件。

## 遍历目录树
os.walk(路径) 是一个强大的遍历工具，它会深入每一层子目录，产出 (当前目录, 子目录列表, 文件列表) 三元组，常配合 for 循环遍历整个文件夹树，适合批量处理文件。

## 代码示例
查看当前目录，并在缺少时创建文件夹：

```python
import os
print("当前目录：", os.getcwd())
if not os.path.exists("data"):
    os.mkdir("data")
for name in os.listdir("."):
    print(name)
```

## 常见错误
第一，删除不存在的路径会报错，操作前先用 os.path.exists 判断。第二，os.rmdir 只能删除空文件夹，里面有东西会失败。第三，直接手写路径分隔符在不同系统上可能不兼容，推荐用 os.path.join 拼接。

## 要点提示
- os 是标准库，import os 即可使用，无需安装。
- getcwd() 看当前目录，chdir() 切换目录，listdir() 列出内容。
- 创建用 mkdir / makedirs，删除用 remove / rmdir。
- 操作路径优先用 os.path.join 和 os.path.exists，更安全跨平台。""",
        "code_example": """import os

# 查看当前目录
print("当前目录：", os.getcwd())

# 列出当前目录下的内容
for name in os.listdir("."):
    print("发现：", name)

# 判断路径是否存在，不存在则创建
if os.path.exists("test_dir"):
    print("test_dir 已存在")
else:
    os.mkdir("test_dir")
    print("已创建 test_dir")

# 拼接路径（跨平台推荐写法）
file_path = os.path.join("test_dir", "note.txt")
with open(file_path, "w", encoding="utf-8") as f:
    f.write("hello")

# 遍历目录树
for root, dirs, files in os.walk("."):
    print("目录：", root, "包含文件：", files)""",
    },
    {
        "slug": "oop",
        "title": "Python 面向对象",
        "summary": "理解封装、继承与多态三大特性。",
        "order_index": 34,
        "duration_min": 14,
        "content_md": """# Python 面向对象

## 从类到对象
前面我们学过类和对象的基础：类（class）是蓝图，对象是根据蓝图造出来的实例。面向对象有三大核心特性：封装、继承和多态。理解这三点，才算真正入门面向对象编程。这一篇我们就在已有基础上，把这三个概念逐一讲清楚。

## 封装
封装就是把数据和操作数据的方法捆绑在一个类里，并把内部细节隐藏起来。Python 通过约定来实现"私有"属性：属性名前加两个下划线 __，例如 __balance，外部就不能直接访问，只能通过类提供的方法（如 get_balance）间接操作。这样做的好处是可以在方法里加入校验逻辑，防止外部把数据改成非法值，让对象自身的状态始终安全可靠。

## 继承
继承让我们基于已有的类创建新类，新类自动拥有父类的属性和方法，叫做子类。语法是 class 子类(父类):。子类可以直接用父类的方法，也可以重写（override）同名方法来改变行为，还可以用 super() 调用父类的实现。继承避免了重复写代码，体现"is-a"关系，比如 Dog 继承 Animal，因为狗是一种动物。

## 多态
多态指的是同一个方法调用，作用在不同对象上会有不同的表现。比如都调用 speak() 方法，Dog 会"汪汪"，Cat 会"喵喵"。只要对象都有同名方法，就可以用统一的方式调用，而不用关心它们具体是什么类型。这让代码更灵活、更容易扩展。

## 代码示例
通过继承与重写体现多态：

```python
class Animal:
    def speak(self):
        print("动物发出声音")

class Dog(Animal):
    def speak(self):
        print("小狗：汪汪汪")

for animal in [Animal(), Dog()]:
    animal.speak()      # 同一个调用，不同表现
```

## 常见错误
第一，把 self 参数忘了，实例方法的第一个参数必须是 self。第二，以为双下划线属性完全不能访问，其实它只是被改名（名称改写），并非绝对私有。第三，子类重写方法时忘了用 super()，导致父类初始化逻辑没有执行。

## 要点提示
- 封装：用 __属性 隐藏内部数据，通过方法对外提供访问。
- 继承：class 子类(父类):，用 super() 复用父类逻辑。
- 多态：不同对象对同一方法调用有不同响应。
- 实例方法第一个参数永远是 self，代表对象本身。""",
        "code_example": """# 封装：把余额藏起来，通过方法访问
class Account:
    def __init__(self, owner):
        self.owner = owner
        self.__balance = 0          # 双下划线表示私有属性

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

    def get_balance(self):
        return self.__balance

# 继承：子类复用并扩展父类
class Animal:
    def speak(self):
        print("动物发出声音")

class Dog(Animal):
    def speak(self):               # 重写父类方法
        print("小狗：汪汪汪")

class Cat(Animal):
    def speak(self):
        print("小猫：喵喵喵")

# 多态：同一个调用，不同表现
for animal in [Dog(), Cat()]:
    animal.speak()

acc = Account("小明")
acc.deposit(100)
print(acc.owner, "的余额是", acc.get_balance())""",
    },
    {
        "slug": "regex",
        "title": "Python 正则表达式",
        "summary": "用 re 模块查找和替换文本。",
        "order_index": 35,
        "duration_min": 12,
        "content_md": """# Python 正则表达式

## 什么是正则表达式
正则表达式（Regular Expression）是一种用来描述、匹配字符串模式的"小型语言"。比如你想在一大段文字里找出所有的手机号、邮箱，或者验证用户输入是不是合法的日期，用普通字符串方法写起来非常繁琐，而正则表达式用几个特殊符号就能表达复杂规则。Python 通过内置的 re 模块提供正则支持，import re 即可使用。

## 常用匹配符号
先认识几个最常用的"元字符"：\\d 表示一个数字，\\w 表示字母数字或下划线，. 表示任意单个字符，^ 表示字符串开头，$ 表示字符串结尾。数量词方面：* 表示重复零次或多次，+ 表示一次或多次，? 表示零次或一次，{n} 表示恰好 n 次。方括号 [abc] 表示匹配其中任意一个字符。由于反斜杠在字符串里有转义含义，推荐使用原始字符串 r"\\d+" 来写正则。

## re 模块的常用函数
re.match() 从字符串开头开始匹配，成功返回匹配对象，否则返回 None；re.search() 在整个字符串中查找第一个匹配；re.findall() 返回所有匹配结果的列表，最常用；re.sub(规则, 替换, 字符串) 用于替换；re.split(规则, 字符串) 按模式切分字符串。匹配对象可以用 group() 取出匹配到的内容。

## 代码示例
用 findall 找出文本里的所有数字：

```python
import re
text = "abc 123 xyz 456"
print(re.findall(r"\\d+", text))   # ['123', '456']
```

## 常见错误
第一，忘记用原始字符串前缀 r，导致 \\d 被当成转义字符而失效。第二，混淆 match 和 search，match 只从开头匹配，字符串中间的内容它找不到。第三，贪婪匹配：.* 会尽可能多地匹配，需要非贪婪时写成 .*?。

## 要点提示
- 用 import re 导入，正则推荐写成 r"..." 原始字符串。
- findall() 找所有结果，search() 找第一个，match() 只从开头找。
- \\d 数字、\\w 单词字符、+ 一次以上、* 零次以上。
- sub() 替换，split() 切分，是文本清洗的利器。""",
        "code_example": """import re

text = "我的电话是 13800138000，邮箱是 test@example.com"

# findall：找出所有数字串
print(re.findall(r"\\d+", text))

# search：查找第一个邮箱
m = re.search(r"\\w+@\\w+\\.\\w+", text)
if m:
    print("找到邮箱：", m.group())

# match：只从开头匹配
print(re.match(r"\\d+", text))         # None，因为开头是"我"

# sub：把数字替换成 #
print(re.sub(r"\\d", "#", text))

# split：按逗号或中文逗号切分
print(re.split(r"[,，]", text))""",
    },
    {
        "slug": "cgi",
        "title": "Python CGI 编程",
        "summary": "了解 CGI 原理与表单读取。",
        "order_index": 36,
        "duration_min": 10,
        "content_md": """# Python CGI 编程

## 什么是 CGI
CGI（Common Gateway Interface，通用网关接口）是一种早期但经典的 Web 技术，它规定了网页服务器如何把用户的请求交给外部程序处理，再把程序的输出返回给浏览器。比如你在网页表单里填写名字并提交，服务器可以调用一个 Python 脚本，脚本读出你填的内容，生成一段 HTML 作为回应。虽然现在更流行 Flask、Django 等框架，但了解 CGI 能帮你理解 Web 请求响应的底层原理。

## 运行环境要求
要运行 CGI 程序，通常需要一个支持 CGI 的 Web 服务器（如 Apache），并把脚本放在指定目录（如 cgi-bin），文件权限设为可执行。Python 标准库里的 cgi 模块可以帮我们解析表单数据，不过要注意：从 Python 3.11 起 cgi 模块已被标记为弃用，并在后续版本中移除，新项目建议使用框架。本课以"看懂代码、认识概念"为主，不要求初学者一定跑通。

## 程序的基本结构
一个 CGI 程序分三部分：第一，输出 HTTP 响应头，告诉浏览器接下来是什么内容，最关键的一行是 Content-Type: text/html 后面跟一个空行；第二，用 cgi.FieldStorage() 获取用户通过 GET 或 POST 提交的参数；第三，根据参数生成 HTML 正文并输出。所有输出本质上都是用 print 打印出来的文本。

## 表单数据的获取
cgi.FieldStorage() 返回一个类似字典的对象。假设表单里有一个名为 name 的输入框，提交后可以用 form.getvalue("name") 取到用户填的值，取不到时返回 None。取到值后要记得做转义，防止用户输入 HTML 标签造成注入问题。

## 代码示例
输出响应头并读取表单参数：

```python
import cgi
print("Content-Type: text/html")
print()                       # 响应头后必须空一行
form = cgi.FieldStorage()
name = form.getvalue("name", "访客")
print("<h1>你好，" + name + "</h1>")
```

## 常见错误
第一，忘记在响应头后输出空行，浏览器会无法显示正文。第二，脚本没有可执行权限或放错目录，服务器返回 500 错误。第三，直接把用户输入拼进 HTML 而不转义，存在安全风险。

## 要点提示
- CGI 是服务器调用脚本生成网页的古老而经典的方式。
- 先输出 Content-Type 响应头，再输出一个空行，然后才是正文。
- 用 cgi.FieldStorage() 读取表单，getvalue() 取值。
- cgi 模块在新版 Python 已弃用，实际项目推荐用 Web 框架。""",
        "code_example": """# CGI 示例程序（需放在支持 CGI 的服务器 cgi-bin 目录，并设为可执行）
# 环境：Python 3.10 及以前自带 cgi 模块；新版本建议改用 Flask 等框架
import cgi

# 1. 输出 HTTP 响应头，注意头与正文之间要有一个空行
print("Content-Type: text/html; charset=utf-8")
print()

# 2. 解析表单数据
form = cgi.FieldStorage()
name = form.getvalue("name", "访客")

# 3. 生成 HTML 正文
print("<html><body>")
print("<h1>简单的 CGI 程序</h1>")
print(f"<p>你好，{name}！欢迎访问。</p>")
print("</body></html>")""",
    },
    {
        "slug": "mysql",
        "title": "Python MySQL",
        "summary": "用 PyMySQL 操作数据库。",
        "order_index": 37,
        "duration_min": 13,
        "content_md": """# Python MySQL

## 什么是 MySQL 与驱动
MySQL 是世界上最流行的关系型数据库之一，用表格的形式存储数据，通过 SQL 语言进行增删改查。Python 本身并不直接内置 MySQL 支持，需要安装第三方驱动来"牵线搭桥"，常用的有 PyMySQL（纯 Python，跨平台，安装简单）和 mysql-connector-python。本课以 PyMySQL 为例，安装方法是命令行执行 pip install pymysql。

## 建立连接
使用 pymysql.connect() 建立到数据库的连接，需要提供主机 host、用户名 user、密码 password、数据库名 database，以及字符集 charset（推荐 utf8mb4 以支持中文和 emoji）。连接对象代表一条到数据库的通道，用完要调用 close() 关闭。

## 用游标执行 SQL
连接本身不能直接执行 SQL，需要通过 cursor() 获得游标对象。游标的作用是执行 SQL 并拿到结果。执行查询用 cursor.execute(sql)，然后用 fetchone() 取一条、fetchall() 取全部结果。执行插入、更新、删除后，必须调用连接对象的 commit() 提交事务，改动才会真正保存到数据库；否则可以用 rollback() 回滚。

## 参数化查询防注入
千万不要用字符串拼接把用户输入塞进 SQL，这会造成 SQL 注入漏洞。正确做法是用占位符 %s，把参数作为第二个参数传给 execute，例如 cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))。驱动会自动帮你转义，安全又可靠。

## 代码示例
查询数据并打印结果：

```python
import pymysql
conn = pymysql.connect(host="localhost", user="root",
                       password="123456", database="test_db")
cursor = conn.cursor()
cursor.execute("SELECT id, name FROM users")
for row in cursor.fetchall():
    print(row)
conn.close()
```

## 常见错误
第一，写漏 commit() 导致数据没有保存。第二，用 % 格式化拼接 SQL，带来注入风险。第三，忘记关闭游标和连接，长期运行会耗尽数据库连接。推荐用 try/finally 或上下文管理器确保关闭。

## 要点提示
- 先 pip install pymysql 安装驱动。
- connect() 建立连接，cursor() 获得游标，execute() 执行 SQL。
- 增删改后要 conn.commit() 提交，查询用 fetchall() 取结果。
- 用 %s 占位符传参，杜绝 SQL 注入。""",
        "code_example": """# 环境准备：pip install pymysql，并确保本机已安装并启动 MySQL
# 下面是一个典型的"查询 + 插入"写法，理解结构即可，不必强求跑通
import pymysql

# 建立连接（请按自己的实际情况修改账号密码）
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="123456",
    database="test_db",
    charset="utf8mb4",
)

try:
    with conn.cursor() as cursor:
        # 参数化查询，防止 SQL 注入
        cursor.execute("SELECT id, name FROM users WHERE id = %s", (1,))
        rows = cursor.fetchall()          # 取出所有结果
        for row in rows:
            print("查到用户：", row)

        # 插入数据，记得提交事务
        cursor.execute(
            "INSERT INTO users(name) VALUES (%s)",
            ("小明",),
        )
    conn.commit()                         # 提交，改动才会保存
except Exception as e:
    conn.rollback()                       # 出错则回滚
    print("数据库操作失败：", e)
finally:
    conn.close()                          # 关闭连接""",
    },
    {
        "slug": "networking",
        "title": "Python 网络编程",
        "summary": "用 socket 实现网络通信。",
        "order_index": 38,
        "duration_min": 13,
        "content_md": """# Python 网络编程

## 什么是网络编程
网络编程就是让两台计算机通过网络交换数据。你可能每天都在用网络：浏览网页、聊天、发邮件，这些背后都是程序在通过网络收发数据。Python 提供了 socket（套接字）模块，它是网络编程的基础工具，位于标准库中，import socket 即可使用。理解 socket，你就能看懂客户端和服务器是如何通信的。

## TCP 与 socket 概念
网络通信有多种协议，最常用的是 TCP。TCP 像打电话：先建立连接，再可靠地传输数据，最后挂断。socket 是通信的一端，可以把它想象成一个"电话插座"。服务器端先绑定一个地址和端口并监听，客户端发起连接请求，双方建立连接后就能收发数据。

## 客户端的写法
客户端步骤：用 socket.socket() 创建套接字，用 connect((主机, 端口)) 连接服务器，然后用 send/sendall 发送数据，用 recv(缓冲区大小) 接收数据，最后 close() 关闭。注意发送和接收的都是字节数据（bytes），字符串要用 encode() 编码，收到的字节要用 decode() 解码。

## 服务器端的写法
服务器端步骤：创建套接字，用 bind((地址, 端口)) 绑定地址端口，用 listen() 开始监听，用 accept() 等待并接受客户端连接（这会阻塞直到有客户端连上来），得到新的连接套接字后收发数据，最后关闭。

## 代码示例
一个最简单的 TCP 客户端：

```python
import socket
s = socket.socket()
s.connect(("127.0.0.1", 9999))
s.send("你好".encode("utf-8"))
print(s.recv(1024).decode("utf-8"))
s.close()
```

## 常见错误
第一，忘记把字符串 encode 成字节，send 会报错。第二，服务器端端口被占用，bind 会失败，换一个端口即可。第三，recv 是阻塞的，如果对方不发数据，程序会一直等待，这是正常现象。

## 要点提示
- socket 是标准库，import socket 即可，无需安装。
- TCP 通信顺序：服务端 bind/listen/accept，客户端 connect。
- 网络传输的是字节，字符串要 encode()/decode() 转换。
- 用完记得 close() 关闭套接字。""",
        "code_example": """# TCP 客户端示例（标准库自带 socket，无需安装）
# 运行前需先启动下面的服务端程序
import socket

client = socket.socket()                    # 创建套接字
client.connect(("127.0.0.1", 9999))          # 连接本机服务器
client.send("你好，服务器".encode("utf-8"))   # 字符串转字节再发送
data = client.recv(1024)                     # 最多接收 1024 字节
print("收到回复：", data.decode("utf-8"))
client.close()

# ---- 下面是服务端代码，应单独放在一个文件里先运行 ----
# import socket
# server = socket.socket()
# server.bind(("127.0.0.1", 9999))            # 绑定地址和端口
# server.listen(5)                             # 开始监听，最多排队 5 个
# conn, addr = server.accept()                 # 等待客户端连接
# data = conn.recv(1024)
# print("收到：", data.decode("utf-8"))
# conn.send("收到你的消息".encode("utf-8"))
# conn.close()
# server.close()""",
    },
    {
        "slug": "smtp",
        "title": "Python SMTP",
        "summary": "用 smtplib 发送电子邮件。",
        "order_index": 39,
        "duration_min": 12,
        "content_md": """# Python SMTP

## 什么是 SMTP
SMTP（Simple Mail Transfer Protocol，简单邮件传输协议）是用来发送电子邮件的协议。当你要在程序里自动发邮件——比如注册成功发送验证码、系统报警通知——就可以用 Python 的 smtplib 模块。它是标准库的一部分，import smtplib 即可使用，不需要额外安装。注意 smtplib 只负责"发送"，接收邮件要用 POP3 或 IMAP 协议。

## 邮件的组成
一封邮件不只有正文，还包含发件人、收件人、主题等信息，这些合起来叫邮件头。Python 用 email 包来构造符合规范的邮件内容。最简单的纯文本邮件可以用 email.mime.text.MIMEText 创建，然后设置 Subject（主题）、From（发件人）、To（收件人）等字段。如果想发带附件或 HTML 的邮件，可以用 MIMEBase 或 MIMEMultipart。

## 发送邮件的基本流程
流程是：用 smtplib.SMTP(服务器地址, 端口) 连接邮件服务器，常用端口是 25，如果用 SSL 加密通常是 465，用 STARTTLS 是 587；然后登录 login(邮箱, 授权码)，注意这里一般用"授权码"而不是邮箱密码，需要在邮箱设置里开启 SMTP 服务并生成授权码；最后用 sendmail(发件人, 收件人, 邮件内容) 发送，完成后 quit() 退出。

## 代码示例
构造并发送一封纯文本邮件：

```python
import smtplib
from email.mime.text import MIMEText
msg = MIMEText("你好，这是一封测试邮件", "plain", "utf-8")
msg["Subject"] = "测试"
msg["From"] = "a@example.com"
msg["To"] = "b@example.com"
server = smtplib.SMTP("smtp.example.com", 25)
server.sendmail("a@example.com", ["b@example.com"], msg.as_string())
server.quit()
```

## 常见错误
第一，用邮箱登录密码而不是授权码，会导致登录失败。第二，没在邮箱设置里开启 SMTP 服务，连接会被拒绝。第三，端口或加密方式选错，比如 465 端口需要用 SMTP_SSL 而不是普通 SMTP。第四，邮件内容没有正确设置邮件头，容易被当成垃圾邮件。

## 要点提示
- smtplib 负责发送邮件，email 包负责构造邮件内容。
- 连接后用 login(邮箱, 授权码) 登录，授权码不是登录密码。
- sendmail(发件人, 收件人, 内容) 发送，最后 quit() 关闭。
- 端口 25/465/587 对应不同的加密方式，要配对使用。""",
        "code_example": """# SMTP 发邮件示例（标准库自带，无需安装）
# 前提：在邮箱设置中开启 SMTP 服务，并获取"授权码"（不是登录密码）
import smtplib
from email.mime.text import MIMEText

# 1. 构造邮件内容
msg = MIMEText("这是一封用 Python 发送的测试邮件。", "plain", "utf-8")
msg["Subject"] = "Python 测试邮件"
msg["From"] = "sender@example.com"
msg["To"] = "receiver@example.com"

# 2. 连接服务器并发送（以 25 端口为例，请换成自己的邮箱服务器）
server = smtplib.SMTP("smtp.example.com", 25)
server.login("sender@example.com", "你的授权码")
server.sendmail("sender@example.com", ["receiver@example.com"], msg.as_string())
server.quit()
print("邮件已发送")

# 提示：若使用 465 端口和 SSL 加密，把连接改为：
# server = smtplib.SMTP_SSL("smtp.example.com", 465)""",
    },
]

# ---------------------------------------------------------------------------
# 练习题数据（expected_answer 为精确单行代码文本，判分用规范化字符串比对）
# ---------------------------------------------------------------------------
EXERCISES = [
    # 第 31 篇：Python File 方法
    {
        "lesson_slug": "file-methods",
        "title": "回到文件开头",
        "description": "请写出把文件对象 f 的读写位置移动到文件开头的语句，使用 seek 方法并传入 0（只写这一行代码）。",
        "starter_code": "# 在这里写一行代码，把 f 的位置移到文件开头\n",
        "expected_answer": "f.seek(0)",
        "difficulty": "easy",
        "order_index": 61,
    },
    {
        "lesson_slug": "file-methods",
        "title": "查看当前位置",
        "description": "请写出用文件对象 f 的 tell() 方法获取当前读写位置，并赋值给变量 pos 的语句（只写这一行赋值语句）。",
        "starter_code": "# 在这里把 f 的当前位置保存到变量 pos\n",
        "expected_answer": "pos = f.tell()",
        "difficulty": "medium",
        "order_index": 62,
    },
    # 第 32 篇：Python 异常处理
    {
        "lesson_slug": "exceptions",
        "title": "异常处理的开头",
        "description": "请写出异常处理结构的关键字起始行，以冒号结尾（只写这一行）。",
        "starter_code": "# 在这里写出异常处理的起始关键字行（以冒号结尾）\n",
        "expected_answer": "try:",
        "difficulty": "easy",
        "order_index": 63,
    },
    {
        "lesson_slug": "exceptions",
        "title": "捕获指定异常",
        "description": "请写出捕获 ValueError 类型异常的 except 语句行，以冒号结尾（只写这一行）。",
        "starter_code": "# 在这里写出捕获 ValueError 的 except 行（以冒号结尾）\n",
        "expected_answer": "except ValueError:",
        "difficulty": "medium",
        "order_index": 64,
    },
    # 第 33 篇：Python OS 文件/目录方法
    {
        "lesson_slug": "os-methods",
        "title": "导入 os 模块",
        "description": "请写出导入 os 模块的语句（只写这一行代码）。",
        "starter_code": "# 在这里写一行代码，导入 os 模块\n",
        "expected_answer": "import os",
        "difficulty": "easy",
        "order_index": 65,
    },
    {
        "lesson_slug": "os-methods",
        "title": "获取当前目录",
        "description": "请写出调用 os 模块中 getcwd() 方法获取当前工作目录的表达式（只写这一行代码）。",
        "starter_code": "# 在这里写一行代码，获取当前工作目录\n",
        "expected_answer": "os.getcwd()",
        "difficulty": "medium",
        "order_index": 66,
    },
    # 第 34 篇：Python 面向对象
    {
        "lesson_slug": "oop",
        "title": "定义一个类",
        "description": "请写出定义一个名为 Dog 的类的语句行，以冒号结尾（只写这一行）。",
        "starter_code": "# 在这里写出定义 Dog 类的语句行（以冒号结尾）\n",
        "expected_answer": "class Dog:",
        "difficulty": "easy",
        "order_index": 67,
    },
    {
        "lesson_slug": "oop",
        "title": "定义子类",
        "description": "请写出定义一个继承自 Dog 的子类 Puppy 的语句行，以冒号结尾（只写这一行）。",
        "starter_code": "# 在这里写出定义 Puppy 类并继承 Dog 的语句行（以冒号结尾）\n",
        "expected_answer": "class Puppy(Dog):",
        "difficulty": "medium",
        "order_index": 68,
    },
    # 第 35 篇：Python 正则表达式
    {
        "lesson_slug": "regex",
        "title": "导入 re 模块",
        "description": "请写出导入正则表达式模块 re 的语句（只写这一行代码）。",
        "starter_code": "# 在这里写一行代码，导入 re 模块\n",
        "expected_answer": "import re",
        "difficulty": "easy",
        "order_index": 69,
    },
    {
        "lesson_slug": "regex",
        "title": "查找所有匹配",
        "description": "请写出使用 re.findall 在变量 text 中查找字母 a 的语句，规则用字符串 'a'（只写这一行代码）。",
        "starter_code": "# 在这里写一行代码，用 re.findall 在 text 中查找字母 a\n",
        "expected_answer": "re.findall('a', text)",
        "difficulty": "medium",
        "order_index": 70,
    },
    # 第 36 篇：Python CGI 编程
    {
        "lesson_slug": "cgi",
        "title": "导入 cgi 模块",
        "description": "请写出导入 CGI 模块 cgi 的语句（只写这一行代码）。",
        "starter_code": "# 在这里写一行代码，导入 cgi 模块\n",
        "expected_answer": "import cgi",
        "difficulty": "easy",
        "order_index": 71,
    },
    {
        "lesson_slug": "cgi",
        "title": "输出响应头",
        "description": "请写出用 print() 输出值为 Content-Type: text/html 的 HTTP 响应头的语句（只写这一行代码）。",
        "starter_code": "# 在这里写一行代码，输出 Content-Type: text/html 响应头\n",
        "expected_answer": "print('Content-Type: text/html')",
        "difficulty": "medium",
        "order_index": 72,
    },
    # 第 37 篇：Python MySQL
    {
        "lesson_slug": "mysql",
        "title": "导入 pymysql",
        "description": "请写出导入 PyMySQL 模块 pymysql 的语句（只写这一行代码）。",
        "starter_code": "# 在这里写一行代码，导入 pymysql 模块\n",
        "expected_answer": "import pymysql",
        "difficulty": "easy",
        "order_index": 73,
    },
    {
        "lesson_slug": "mysql",
        "title": "执行 SQL 语句",
        "description": "请写出使用游标 cursor 执行变量 sql 中保存的 SQL 语句的代码（只写这一行代码）。",
        "starter_code": "# 在这里写一行代码，用 cursor 执行变量 sql\n",
        "expected_answer": "cursor.execute(sql)",
        "difficulty": "medium",
        "order_index": 74,
    },
    # 第 38 篇：Python 网络编程
    {
        "lesson_slug": "networking",
        "title": "导入 socket 模块",
        "description": "请写出导入 socket 模块的语句（只写这一行代码）。",
        "starter_code": "# 在这里写一行代码，导入 socket 模块\n",
        "expected_answer": "import socket",
        "difficulty": "easy",
        "order_index": 75,
    },
    {
        "lesson_slug": "networking",
        "title": "创建套接字",
        "description": "请写出创建一个 socket 套接字对象并赋值给变量 s 的语句（只写这一行赋值语句）。",
        "starter_code": "# 在这里写一行代码，创建 socket 对象并赋值给 s\n",
        "expected_answer": "s = socket.socket()",
        "difficulty": "medium",
        "order_index": 76,
    },
    # 第 39 篇：Python SMTP
    {
        "lesson_slug": "smtp",
        "title": "导入 smtplib",
        "description": "请写出导入 smtplib 模块的语句（只写这一行代码）。",
        "starter_code": "# 在这里写一行代码，导入 smtplib 模块\n",
        "expected_answer": "import smtplib",
        "difficulty": "easy",
        "order_index": 77,
    },
    {
        "lesson_slug": "smtp",
        "title": "创建 SMTP 对象",
        "description": "请写出创建一个 SMTP 对象并赋值给变量 server 的语句，不传任何参数（只写这一行赋值语句）。",
        "starter_code": "# 在这里写一行代码，创建 SMTP 对象并赋值给 server\n",
        "expected_answer": "server = smtplib.SMTP()",
        "difficulty": "medium",
        "order_index": 78,
    },
]
