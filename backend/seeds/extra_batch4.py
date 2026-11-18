"""扩展教程数据：第 4 批（多线程、XML、Tkinter、版本区别、IDE、JSON、绘画、100例、测验）。

本文件只定义 LESSONS 与 EXERCISES 两个列表，供 seed 脚本按 slug 去重导入。
教程 order_index 为 40-48，练习题 order_index 为 79-96。
"""

LESSONS = [
    {
        "slug": "threading",
        "title": "Python 多线程",
        "summary": "掌握线程的创建与同步基础。",
        "order_index": 40,
        "duration_min": 12,
        "content_md": """# Python 多线程

## 什么是线程与多线程
线程（thread）是操作系统能够进行运算调度的最小单位，它被包含在进程之中，是进程里实际运作的单位。一个进程可以拥有多个线程，每个线程执行不同的任务。多线程（multithreading）就是让一个程序同时运行多个线程，从而在同一时刻处理多件事。举个生活例子：你一边听歌一边浏览网页，听歌和浏览就是两个线程在同时工作。对 Python 来说，多线程特别适合处理 I/O 密集型任务，比如网络请求、文件读写、等待用户输入等：当某个线程在等待时，其他线程可以继续干活，从而提升程序整体效率。

## 创建线程的两种方式
Python 的标准库 threading 提供了线程支持。创建线程有两种常见方式。第一种是直接创建 threading.Thread 对象，把要在线程中执行的函数传给 target 参数，然后调用 start() 启动，例如 `t = threading.Thread(target=work)` 再 `t.start()`。第二种是继承 threading.Thread 类并重写它的 run() 方法，把线程要执行的逻辑写进 run() 里，然后创建子类实例并调用 start()。初学时推荐第一种，简单直观。注意：只创建对象而不调用 start()，线程里的函数根本不会执行。

## 线程的常用方法与属性
Thread 对象有一些常用方法：start() 启动线程，一个线程只能启动一次；join() 等待线程结束，让主线程停下来等子线程干完活再继续；is_alive() 判断线程是否还在运行。模块级函数 threading.current_thread() 返回当前线程对象，threading.active_count() 返回当前活跃的线程数量。给线程起名字可以用 name 参数，方便调试时区分。利用 f-string 配合 current_thread().name 能在输出中看清是哪个线程在执行。

## 一个完整示例
下面示例启动两个线程，分别循环打印自己的名字。为了让输出更清楚，我们在每个线程里用 current_thread().name 拿到线程名，并用 time.sleep() 稍微暂停，模拟耗时任务。主线程用 join() 等待两个子线程结束后才打印结束提示，这样能保证输出顺序完整，不会在主线程退出时被中断。

```python
import threading
import time

def worker():
    name = threading.current_thread().name
    for i in range(3):
        print(f"{name} 正在工作：第 {i + 1} 次")
        time.sleep(0.2)
    print(f"{name} 完成")

t1 = threading.Thread(target=worker, name="线程A")
t2 = threading.Thread(target=worker, name="线程B")
t1.start()
t2.start()
t1.join()
t2.join()
print("所有线程结束，活跃线程数：", threading.active_count())
```

## 常见错误
第一，只创建线程对象却忘记调用 start()，那样线程里的函数不会执行；第二，同一个线程对象调用两次 start() 会报 RuntimeError；第三，多个线程同时修改同一个全局变量时可能出现竞态条件，结果不可预期，这时需要用到锁 threading.Lock；第四，没有 join() 就急于读取线程产生的结果，可能还没算完；第五，误以为多线程能大幅加速纯计算任务，实际上受 GIL 全局解释器锁限制，CPU 密集型任务提速有限。

## 要点提示
- 用 threading.Thread(target=函数) 创建线程，用 start() 启动。
- join() 让主线程等待子线程完成，适合需要汇总结果的场景。
- 多线程适合 I/O 密集型任务；受 GIL 限制，CPU 密集型任务提速有限。
- 多线程共享全局变量，修改共享数据时要加锁保护。""",
        "code_example": """import threading
import time

def worker(name):
    for i in range(3):
        print(f"{name} 正在工作：第 {i + 1} 次")
        time.sleep(0.3)
    print(f"{name} 完成")

t1 = threading.Thread(target=worker, args=("线程A",))
t2 = threading.Thread(target=worker, args=("线程B",))
t1.start()
t2.start()

t1.join()
t2.join()
print("主线程结束，当前活跃线程数：", threading.active_count())""",
    },
    {
        "slug": "xml",
        "title": "Python XML 解析",
        "summary": "掌握 XML 的解析与生成。",
        "order_index": 41,
        "duration_min": 12,
        "content_md": """# Python XML 解析

## 什么是 XML
XML（Extensible Markup Language，可扩展标记语言）是一种用标签描述数据的文本格式，长得很像 HTML，但 HTML 用来显示数据，XML 用来存储和传输数据。XML 由元素（element）组成，元素用开始标签和结束标签包裹，例如 `<name>小明</name>`，标签之间可以嵌套，形成树状结构。XML 常用于配置文件、数据交换和企业系统之间的信息传递。因为它是纯文本、结构清晰且与平台无关，所以曾经非常流行，至今在很多老系统和配置文件里仍能看到它。

## 用 ElementTree 解析 XML
Python 标准库里解析 XML 最常用的模块是 xml.etree.ElementTree，通常按别名 ET 导入：`import xml.etree.ElementTree as ET`。解析有两种常见方式：如果 XML 在文件里，用 `tree = ET.parse("data.xml")` 得到 ElementTree 对象，再用 `root = tree.getroot()` 拿到根元素；如果 XML 是字符串，用 `root = ET.fromstring(xml_str)` 直接得到根元素。两种方式拿到的 root 都是一个 Element 对象，代表整棵树的根节点。

## 遍历与查找元素
Element 对象可以像列表一样遍历，每个子元素又是一个 Element。常用属性和方法：root.tag 得到元素的标签名；root.attrib 得到属性组成的字典；element.text 得到标签之间的文本内容；用 for child in root 遍历子元素；root.find("子元素标签") 查找第一个匹配的子元素；root.findall("子元素标签") 查找所有匹配的子元素并返回列表；root.iter("标签") 遍历整棵树中某个标签的所有元素。属性可以用 element.get("属性名") 读取。

## 生成与保存 XML
除了读，ElementTree 也能写。用 ET.Element("标签") 创建元素，用 ET.SubElement(父元素, "标签") 添加子元素，用 element.set("属性名", "值") 设置属性，用 element.text = "内容" 设置文本，最后用 tree.write("out.xml", encoding="utf-8") 保存到文件。下面示例先解析一段 XML 字符串并读取每位学生的信息，再新建一棵树保存为文件，覆盖了读写两方面。

```python
import xml.etree.ElementTree as ET

xml_text = "<class><student id='1'><name>小明</name></student></class>"
root = ET.fromstring(xml_text)
print("根标签：", root.tag)
for student in root.findall("student"):
    print(student.get("id"), student.find("name").text)

new_root = ET.Element("note")
ET.SubElement(new_root, "to").text = "小明"
tree = ET.ElementTree(new_root)
tree.write("note.xml", encoding="utf-8")
```

## 常见错误
第一，XML 标签必须正确闭合，而且大小写敏感，Name 和 name 是不同标签；第二，属性值必须加引号；第三，用 parse 打开不存在的文件会报 FileNotFoundError；第四，格式不合法的 XML 会抛 ET.ParseError；第五，解析外部不可信的 XML 时要注意安全，标准库对 XML 外部实体攻击防护较弱，处理不可信数据可考虑更安全的第三方库 defusedxml。

## 要点提示
- 用 import xml.etree.ElementTree as ET 导入标准库模块。
- ET.parse(文件) 解析文件，ET.fromstring(字符串) 解析字符串。
- find 找第一个，findall 找全部，iter 遍历整棵树。
- .tag 是标签名，.attrib 是属性字典，.text 是文本内容，get 读属性。""",
        "code_example": """import xml.etree.ElementTree as ET

# 解析一段 XML 字符串
xml_text = '''<class>
  <student id="1"><name>小明</name><score>92</score></student>
  <student id="2"><name>小红</name><score>88</score></student>
</class>'''
root = ET.fromstring(xml_text)
print("根标签：", root.tag)
for student in root.findall("student"):
    name = student.find("name").text
    score = student.find("score").text
    print(f"学号 {student.get('id')}：{name}，成绩 {score}")

# 生成一棵新的 XML 树并保存
new_root = ET.Element("note")
ET.SubElement(new_root, "to").text = "小明"
ET.SubElement(new_root, "from").text = "小红"
tree = ET.ElementTree(new_root)
tree.write("note.xml", encoding="utf-8")
print("已生成 note.xml")""",
    },
    {
        "slug": "tkinter-detail",
        "title": "Python GUI 编程(Tkinter)",
        "summary": "用 Tkinter 做出第一个桌面窗口。",
        "order_index": 42,
        "duration_min": 13,
        "content_md": """# Python GUI 编程(Tkinter)

## 什么是 GUI 与 Tkinter
GUI 是 Graphical User Interface（图形用户界面）的缩写，指通过窗口、按钮、输入框等可视化控件与程序交互的方式，和在命令行里敲命令的命令行界面相对。Tkinter 是 Python 标准库自带的 GUI 工具包，封装了 Tcl/Tk 图形库，无需额外安装就能使用，非常适合初学者做出第一个带窗口的小程序。它的优点是简单、跨平台，缺点是界面风格比较朴素，复杂界面需要更多代码。

## 创建第一个窗口
使用 tkinter 的第一步是导入模块并按别名 tk 使用：`import tkinter as tk`。然后按固定流程搭建程序：先创建主窗口 `root = tk.Tk()`；再往窗口里添加各种控件；接着调用 `root.mainloop()` 进入主事件循环，让窗口保持显示并响应用户操作。mainloop 会一直运行直到用户关闭窗口，所以通常放在代码最后一行。省略 mainloop，窗口会一闪而过，这是初学时最常遇到的问题之一。

## 常用控件介绍
Tkinter 提供多种控件（也叫部件、widget）：Label 标签，用来显示文字或图片；Button 按钮，点击后触发函数；Entry 单行输入框；Text 多行文本框；Frame 框架，作为容器把其他控件分组；Checkbutton 复选框；Radiobutton 单选框；Listbox 列表框。创建控件时要指定父容器，例如 `label = tk.Label(root, text="你好")`，第一个参数 root 表示把标签放到主窗口里。控件创建后还要用布局方法摆放出来。

## 布局管理
控件创建后需要摆放到窗口里，Tkinter 有三种布局管理器：pack() 按垂直或水平方向依次排列，最简单；grid() 按行列的网格放置，适合表单类界面；place() 按精确坐标放置，灵活但麻烦。初学推荐 pack 和 grid。用 pack() 时控件会依次堆叠，可以用 pady 设置上下间距；用 grid(row=0, column=0) 时要指定行号和列号。注意同一个容器里不要混用 pack 和 grid，否则会报错。

## 一个完整示例
下面示例创建一个窗口，包含标题、标签、输入框和按钮。点击按钮后，程序通过 entry.get() 读取输入框内容，再用 label.config() 更新标签文字，展示最基本的事件响应流程。command 参数接收的是函数名，不要写成带括号的调用形式。

```python
import tkinter as tk

def say_hello():
    name = entry.get()
    label.config(text=f"你好，{name}！")

root = tk.Tk()
root.title("我的第一个 GUI")
label = tk.Label(root, text="请输入你的名字")
label.pack(pady=10)
entry = tk.Entry(root)
entry.pack(pady=5)
button = tk.Button(root, text="打招呼", command=say_hello)
button.pack(pady=10)
root.mainloop()
```

## 常见错误
第一，忘记调用 mainloop()，窗口不显示或一闪而过；第二，把 root.mainloop() 写在添加控件之前，导致后续代码被阻塞、控件加不上去；第三，同一个父容器混用 pack 和 grid 会报错；第四，点击按钮时函数需要参数却没传，应写成 lambda 表达式包装；第五，在按钮的 command 里写 函数名加括号 会在创建按钮时立即执行，正确做法是只写函数名本身。

## 要点提示
- 用 import tkinter as tk 导入，tk.Tk() 创建主窗口。
- 程序结尾必须调用 root.mainloop() 进入事件循环。
- 控件创建时要指定父容器，如 tk.Label(root, ...)。
- pack、grid、place 三种布局不要在同一容器里混用。""",
        "code_example": """import tkinter as tk

def say_hello():
    name = entry.get()
    label.config(text=f"你好，{name}！欢迎学习 Python。")

root = tk.Tk()
root.title("我的第一个 GUI")
root.geometry("320x180")

label = tk.Label(root, text="请输入你的名字", font=("Arial", 13))
label.pack(pady=12)

entry = tk.Entry(root)
entry.pack(pady=6)

button = tk.Button(root, text="打招呼", command=say_hello)
button.pack(pady=12)

root.mainloop()""",
    },
    {
        "slug": "py2-vs-py3",
        "title": "Python2.x 与 3.x 版本区别",
        "summary": "了解 2/3 差异，专注学习 3.x。",
        "order_index": 43,
        "duration_min": 10,
        "content_md": """# Python2.x 与 3.x 版本区别

## 为什么要了解版本区别
Python 在发展过程中有两个主要版本系列：Python 2.x 和 Python 3.x。Python 2 发布于 2000 年，曾经非常流行，但它的一些设计存在历史遗留问题。Python 3 于 2008 年发布，是一次不向后兼容的大升级，修复了许多设计缺陷。Python 官方已经在 2020 年停止对 Python 2 的支持，也就是说它不再获得安全更新和错误修复。因此现在学习 Python 应当直接学 Python 3.x。了解两者的区别，主要是为了能看懂老代码、理解网上老教程里的写法差异。

## print 的区别
最直观的区别是 print。Python 2 中 print 是一条语句，写成 print 空格 字符串，不加括号；Python 3 中 print 是一个函数，必须写成 `print("hello")`。在 Python 2 里带括号的写法也能运行，因为它把括号当成了普通分组，但打印多个值时会得到元组；而在 Python 3 中 `print("a", "b")` 会正确打印两个值。所以初学时一定要用函数形式，把要输出的内容放进括号里。

## 整数除法的区别
Python 2 中两个整数相除 5 / 2 结果是整数 2（向下取整），想要小数必须写成 5.0 / 2；Python 3 中斜杠除法总是返回浮点数，5 / 2 结果是 2.5，想要整数商要用整除运算符 `//`，即 5 // 2 得到 2。这个变化让除法结果更符合直觉，也避免了结果类型随操作数变化的困惑。另外 Python 3 中 // 对负数同样向下取整，需要留意。

## 编码与字符串的区别
Python 2 的默认字符串是字节串（bytes），处理中文需要加 u 前缀写成 u"中文"；Python 3 中字符串默认是 Unicode（str），可以直接写中文，字节串要显式加 b 前缀写成 b"abc"。Python 3 源码文件默认按 UTF-8 编码，写中文更省心，这也是它更适合处理多语言文本的原因。想把一个字符串编码成字节用 encode()，把字节解码成字符串用 decode()，这一对方法是处理编码问题的常用工具。

## range 与 input 的区别
Python 2 中 range(5) 直接返回列表，而 xrange(5) 返回一个惰性序列（按需生成，更省内存）；Python 3 中去掉了 xrange，range() 本身就变成了惰性的 range 对象，要得到列表需要写 `list(range(5))`。另外 Python 3 中 input() 总是返回字符串；Python 2 的 raw_input() 才返回字符串，而 input() 会把输入当作表达式求值，存在安全隐患。下面的示例全部采用 Python 3 的正确写法。

```python
print("hello")
print(5 / 2)      # 2.5
print(5 // 2)     # 2
text = "中文字符串"
print(list(range(5)))
```

## 常见错误
第一，照抄 Python 2 教程里的 print 语句写法，在 Python 3 会语法错误；第二，以为 5 / 2 得到整数，实际是 2.5，需要整除要用 //；第三，把 Python 2 的 xrange 用到 Python 3 会报 NameError；第四，用 Python 2 的方式处理中文字符串导致乱码；第五，误以为 net 上所有代码都能直接运行，运行前要先判断它属于哪个版本。

## 要点提示
- 现在学 Python 请直接学 3.x，官方已停止支持 Python 2。
- print 是函数，要写成 print(内容) 的形式。
- 斜杠除法返回浮点数，整除用两个斜杠。
- 字符串默认支持中文；range 是惰性对象，要列表用 list(range(n))。""",
        "code_example": """# 以下均为 Python 3 写法
print("hello")            # print 是函数，要加括号

a = 5 / 2
b = 5 // 2
print("5 / 2 =", a)       # 2.5
print("5 // 2 =", b)      # 2

text = "中文字符串"        # 默认支持中文
print(text)

nums = list(range(5))     # range 是惰性对象，转成列表
print(nums)

name = input("请输入姓名：")  # input 返回字符串
print("你好，" + name)""",
    },
    {
        "slug": "ide",
        "title": "Python IDE",
        "summary": "认识常见 Python 编辑器与选择。",
        "order_index": 44,
        "duration_min": 8,
        "content_md": """# Python IDE

## 什么是 IDE
IDE 是 Integrated Development Environment（集成开发环境）的缩写，指把代码编辑、运行、调试等功能整合在一起的软件。对初学者来说，选一个顺手的工具能让学习事半功倍。广义上，任何能写 Python 代码的工具都可以算编辑器，而 IDE 通常还额外提供代码补全、语法高亮、断点调试、项目管理等能力。需要澄清的是：IDE 只是写代码和运行的工具，Python 语言本身的语法不会因为你换了工具而改变，所以本篇不安排需要特定环境才能运行的代码示例，重点是帮你选对工具、用对方法。

## 常见工具介绍
第一，IDLE：安装 Python 时自带，轻量简单，自带交互式窗口，适合刚入门写几十行的小程序。第二，PyCharm：功能强大的专业 IDE，分免费的社区版和收费的专业版，代码补全和调试体验极佳，适合做项目。第三，VS Code：微软出品的轻量级代码编辑器，通过安装 Python 插件获得语法高亮、补全和调试能力，免费且插件生态丰富，是目前非常流行的选择。第四，Jupyter Notebook 与 JupyterLab：以笔记本形式运行代码，单元格可逐个执行并立即看到结果，广泛用于数据分析、机器学习和教学。

## 如何选择
如果刚入门，先用 IDLE 或 VS Code 写小程序，把基础语法练熟；如果要做完整项目、重视调试和重构，选 PyCharm；如果做数据分析、需要边写边看图表结果，选 Jupyter。工具没有绝对好坏，关键是顺手、能让你专注写代码。很多开发者会同时用多个工具：平时用 VS Code 或 PyCharm 写项目，做数据探索时用 Jupyter。不必在选择上纠结太久，先装一个用起来最重要，等有了具体需求再尝试其他工具也不迟。

## 基本使用流程
不管用哪个工具，核心流程类似：新建 Python 文件（扩展名是 .py）→ 写代码 → 保存 → 点击运行或按快捷键（通常是 F5）→ 在终端或控制台查看输出。遇到报错时，认真阅读红色的错误信息，通常包含文件名、行号和错误类型，这比盲目试错高效得多。学会用断点调试（在行号旁点一下设置断点，然后以调试模式运行，逐行查看变量值）是进阶的重要一步，能帮你真正看清程序是怎么一步步执行的。下面这段通用代码可以在任何 IDE 或交互式环境中运行，用来验证环境是否配置成功：

```python
def greet(name):
    return "你好，" + name

print(greet("小明"))
```

## 常见错误
第一，把文件命名为与标准库重名的名字（例如 print.py、json.py），导致导入冲突；第二，代码没保存就运行，看到的还是旧结果；第三，在编辑器里选错了 Python 解释器，尤其是电脑装了多个版本时，运行的不是你以为的那个环境；第四，把中文全角符号（如中文括号、中文引号）写进代码，引发语法错误，这时要把输入法切到英文半角状态再写符号。

## 要点提示
- IDLE 自带最轻量；PyCharm 功能全；VS Code 轻便插件多；Jupyter 适合数据探索。
- 文件用 .py 扩展名，运行前记得保存。
- 不要给文件起与标准库相同的名字，避免导入冲突。
- 学会看报错信息和用断点调试，比记住快捷键更重要。""",
        "code_example": """# 这是一段通用示例代码，可在任意 Python IDE 中运行
def greet(name):
    return f"你好，{name}！欢迎学习 Python。"

if __name__ == "__main__":
    message = greet("小明")
    print(message)""",
    },
    {
        "slug": "json",
        "title": "Python JSON",
        "summary": "掌握 JSON 数据的转换方法。",
        "order_index": 45,
        "duration_min": 11,
        "content_md": """# Python JSON

## 什么是 JSON
JSON（JavaScript Object Notation）是一种轻量级的数据交换格式，虽然名字里有 JavaScript，但它独立于语言，几乎所有编程语言都支持。JSON 用文本表示结构化数据，非常适合在网络上传输（比如网站前后端之间传数据）和保存配置。它的数据结构只有两种：对象和数组。对象用花括号包裹，里面是键和值用冒号分隔的键值对；数组用方括号包裹，里面是有序的值列表。键必须是字符串，值可以是字符串、数字、布尔值、null、对象或数组。

## JSON 与 Python 数据类型的对应
JSON 和 Python 的数据类型有对应关系，理解它就能正确转换：JSON 对象对应 Python 的字典（dict），JSON 数组对应 Python 的列表（list），JSON 字符串对应 str，数字对应 int 或 float，true 和 false 对应 True 和 False，null 对应 None。需要注意 JSON 里是小写的 true、false、null，而 Python 里是首字母大写的 True、False 和 None。转换时这些细节由 json 模块自动处理，一般不需要手动转换。

## 用 json 模块序列化
把 Python 对象转成 JSON 字符串叫序列化，用 json.dumps()。例如 json.dumps({"name": "小明", "age": 12}) 返回一个 JSON 格式的字符串。如果想写到文件，用 json.dump(对象, 文件对象)。常用参数：ensure_ascii=False 让中文正常显示而不是被转义成 unicode 编码；indent=2 让输出带缩进、更美观。初学时最常忘记的就是 ensure_ascii=False，导致中文变成一堆看不懂的转义序列。

## 用 json 模块反序列化
把 JSON 字符串转回 Python 对象叫反序列化，用 json.loads()。例如 json.loads 一个包含键值对的 JSON 字符串，会得到一个字典。如果从文件读，用 json.load(文件对象)。反序列化后就可以像普通字典、列表一样用下标或键操作数据。注意区分四兄弟：dumps 和 loads 操作字符串，dump 和 load 操作文件，记住"带 s 的是字符串"就不容易混。下面示例演示完整的序列化再反序列化过程。

```python
import json

data = {"name": "小明", "age": 12}
json_str = json.dumps(data, ensure_ascii=False, indent=2)
print(json_str)
restored = json.loads(json_str)
print(restored["name"])
```

## 常见错误
第一，JSON 的键和字符串值必须用双引号，不能用单引号；第二，JSON 中不能出现多余逗号或注释，否则 json.loads() 会抛 JSONDecodeError；第三，直接 dumps 中文会得到转义后的编码，加 ensure_ascii=False 解决；第四，Python 的元组、集合等类型不在 JSON 标准里，序列化集合会报 TypeError；第五，把 dumps/loads 和 dump/load 记混，对字符串误用了需要文件对象的函数。

## 要点提示
- 用 import json 导入模块。
- dumps 把 Python 对象转 JSON 字符串，loads 把 JSON 字符串转回 Python 对象。
- dump 和 load 配文件使用，别忘了传文件对象。
- 处理中文加 ensure_ascii=False，想美化输出加 indent=2。""",
        "code_example": """import json

data = {"name": "小明", "age": 12, "skills": ["Python", "数学"]}

# 序列化：Python 对象 -> JSON 字符串
json_str = json.dumps(data, ensure_ascii=False, indent=2)
print(json_str)

# 反序列化：JSON 字符串 -> Python 对象
restored = json.loads(json_str)
print(type(restored), restored["name"])

# 写入文件再读回
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
print("从文件读回：", loaded)""",
    },
    {
        "slug": "ai-art",
        "title": "Python AI 绘画",
        "summary": "用 turtle 开启代码绘画。",
        "order_index": 46,
        "duration_min": 12,
        "content_md": """# Python AI 绘画

## 用 Python 画画
提到 AI 绘画，很多人想到的是输入一句话就生成精美图片的智能程序，那背后是复杂的深度学习模型，超出了初学者的范围。但其实用 Python 也能轻松画出漂亮的图案：一类是用代码精确控制笔触的绘图，比如标准库自带的 turtle 海龟绘图；另一类是用 Pillow（PIL 的现代维护版）库处理图片、绘制图形。本篇带你用 turtle 入门编程绘图，并简单认识 PIL。用代码作画的核心是把图形拆成一步步的指令，这正是编程思维的绝佳训练，不需要任何 AI 模型也能玩得很开心。

## turtle 海龟绘图入门
turtle 模块模拟一只小海龟在画布上爬行，它背上绑着一支笔，爬过的地方就留下线条。用 import turtle 导入后，通过模块函数下达命令：turtle.forward(距离) 让海龟前进，turtle.backward(距离) 后退，turtle.left(角度) 左转，turtle.right(角度) 右转，turtle.penup() 抬笔（移动不留线），turtle.pendown() 落笔，turtle.pensize(宽度) 设置笔粗细，turtle.pencolor("red") 设置颜色。循环配合转向指令能画出各种规则图形，例如重复四次前进加左转九十度就能画一个正方形。

## 用循环画重复图案
turtle 最强大的地方是可以用循环画出复杂图案。例如画一个正 n 边形，只需循环 n 次，每次前进固定长度再左转 360 除以 n 度；如果每次转向角度略有变化，就能画出旋转的漂亮花纹。绘制前可以用 turtle.speed(0) 把速度设为最快，用 turtle.title() 设置窗口标题，画完用 turtle.done() 让窗口保持打开。注意 turtle.done() 要放在最后，它会阻塞程序直到你关闭窗口。给海龟换颜色、调整笔宽，同一个循环就能呈现完全不同的视觉效果。例如画一个正方形只需要四步循环：

```python
import turtle
for i in range(4):
    turtle.forward(100)
    turtle.left(90)
turtle.done()
```

## PIL 绘图简介
如果想生成图片文件而不是在窗口里画，可以用第三方库 Pillow（安装命令是 pip install pillow）。核心是 Image 类和 ImageDraw 模块：先用 Image.new("RGB", (宽, 高), "white") 创建一张白色画布，再用 ImageDraw.Draw(img) 得到画笔对象，调用 draw.line()、draw.rectangle()、draw.ellipse() 等画线条和形状，最后 img.save("out.png") 保存成图片。Pillow 还能裁剪、缩放、加文字，是处理图片的利器。注意导入写法是 from PIL import Image，老教程里的写法已经过时。

## 常见错误
第一，用 turtle 时窗口一闪而过，通常是忘了最后调用 turtle.done() 或 turtle.mainloop()；第二，海龟位置不对，忘记先 penup 抬笔就移动，留下了多余的线；第三，转向角度用错单位，turtle 用的是角度而不是弧度；第四，用 PIL 却没安装 pillow 会报 ModuleNotFoundError，需要先执行安装命令；第五，忘记落笔或把颜色写成不支持的名称，导致画线颜色不符合预期，建议用常见的英文颜色名如 red、blue、green。

## 要点提示
- turtle 是标准库，无需安装；用 import turtle 导入。
- 前进 forward、转向 left 和 right、抬落笔 penup 和 pendown 是最常用指令。
- 循环加转向能画出规则多边形和旋转花纹，done 要放最后。
- PIL（Pillow）需先安装，用 from PIL import Image 导入，适合生成图片文件。""",
        "code_example": """import turtle

# 设置画布与画笔
turtle.title("turtle 绘图示例")
turtle.speed(0)
turtle.pensize(2)

# 画一个彩色旋转图案
colors = ["red", "orange", "yellow", "green", "blue", "purple"]
for i in range(36):
    turtle.pencolor(colors[i % len(colors)])
    turtle.forward(100)
    turtle.right(170)   # 每次多转一点，形成旋转花纹

# 回到起点并标注文字
turtle.penup()
turtle.goto(0, -140)
turtle.pendown()
turtle.write("Python 代码绘画", align="center", font=("Arial", 14, "bold"))

turtle.done()""",
    },
    {
        "slug": "examples-100",
        "title": "Python 100例",
        "summary": "通过经典小题巩固循环与函数。",
        "order_index": 47,
        "duration_min": 14,
        "content_md": """# Python 100例

## 为什么要做经典练习题
很多人学习编程时都听说过 Python 100 例，它指的是一批经典的入门练习题。刷题不是死记硬背答案，而是把学过的语法真正用起来：把问题拆解成步骤，再用顺序、分支、循环和函数把步骤翻译成代码。坚持做经典题能快速建立编程思维，也是检验基础是否扎实的有效方式。本篇精选几道最经典的题目，讲清思路并给出代码片段，建议你先自己试着写一遍，再看参考代码，这样收获最大。

## 例一：斐波那契数列
题目要求输出斐波那契数列的前 n 项。这个数列从第 3 项开始，每一项等于前两项之和：1, 1, 2, 3, 5, 8 以此类推。思路是用两个变量 a、b 保存前两项，每次循环先打印 a，再同时更新 a、b 为 b 和 a+b。这里同时赋值的写法非常关键，如果分两步写会互相干扰导致结果错误。循环 n 次即可输出前 n 项，用 end 参数让结果打印在同一行。

```python
def fibonacci(n):
    a, b = 1, 1
    for _ in range(n):
        print(a, end=" ")
        a, b = b, a + b

fibonacci(10)
```

## 例二：判断素数
素数（质数）是大于 1 且只能被 1 和自身整除的数。思路：对 n，用循环让 i 从 2 遍历到 n 的平方根附近，如果 n 能被某个 i 整除，就不是素数；循环结束都没整除，就是素数。把判断写成函数 is_prime(n) 便于复用，注意先排除小于 2 的情况。范围取到 n 的平方根取整再加一即可，没必要检查到 n 减一，这样效率更高。

```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
```

## 例三：九九乘法表
用嵌套循环打印九九乘法表：外层循环控制行数 i（1 到 9），内层循环控制每行的列 j（1 到 i）。打印每一项时把 end 参数设为制表符来对齐，在内层循环结束后用一个空的 print 换行。这里内层循环的上限是 i 而不是 9，正好形成下三角形的形状。嵌套循环是初学者必须掌握的结构，外层走一步、内层走一圈的节奏要多练习体会。

```python
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}x{i}={i * j}", end="    ")
    print()
```

## 例四：统计字符出现次数
给一段字符串，统计每个字符出现的次数。思路是用一个字典作计数器，遍历字符串，遇到字符就把对应的值加一，写法是 counts[ch] = counts.get(ch, 0) + 1。get 方法的第二个参数是默认值，避免第一次遇到字符时因为键不存在而报错。这是字典非常典型的应用，很多统计类问题都能套用这个套路。

## 常见错误
第一，斐波那契里分两步更新 a 和 b，导致结果错乱，要用同时赋值；第二，判断素数时范围写错或从 1 开始除，导致所有数都被判为非素数；第三，乘法表内层循环上限写成 9，打印出完整方形而不是三角形；第四，统计字符时直接对键做加一，第一次遇到字符会因键不存在报 KeyError；第五，忘记函数在调用前要先定义。

## 要点提示
- 斐波那契用 a, b = b, a + b 同时更新，避免顺序干扰。
- 素数判断只需除到平方根，注意排除小于 2 的数。
- 嵌套循环：内层用 end 不换行，内层结束后再换行。
- 字典计数用 counts.get(key, 0) + 1 最稳妥。""",
        "code_example": """# 例一：斐波那契数列前 10 项
def fibonacci(n):
    a, b = 1, 1
    for _ in range(n):
        print(a, end=" ")
        a, b = b, a + b
    print()

fibonacci(10)

# 例二：判断素数
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

print("17 是素数吗？", is_prime(17))

# 例三：九九乘法表
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}x{i}={i * j}", end="\\t")
    print()""",
    },
    {
        "slug": "quiz",
        "title": "Python 测验",
        "summary": "通过自测题检验并巩固基础。",
        "order_index": 48,
        "duration_min": 10,
        "content_md": """# Python 测验

## 为什么要做自测
学完基础语法后，怎么知道自己真的掌握了吗？最好的办法就是自测：不看答案，先自己想一想、写一写，再对照解析找出薄弱点。自测不是考试，而是帮你发现以为懂了其实没懂的地方。本篇准备了几道检验基础概念的选择题和思考题，覆盖变量、运算、循环、字符串和列表等主题，每题都给出答案与解析。建议先遮住答案，把每题在心里或纸上答一遍，再往下看解析，效果最好。

## 选择题一：输出是什么
问题：执行两整数运算 7 整除 2 和 7 取余 2 并打印，输出是什么？A. 3.5 和 1；B. 3 和 1；C. 3 和 3；D. 3.5 和 3。答案：B。解析：整除运算符只取商的整数部分，7 整除 2 得 3；取余运算符 7 除以 2 余 1。所以输出 3 和 1。注意普通斜杠除法才会得到浮点数 3.5，这是初学者最容易混淆的地方，一定要区分三种除法运算符。

## 选择题二：变量与类型
问题：x 赋值为字符串 5 之后，x 加整数 1 会怎样？A. 得到 6；B. 得到 51；C. 报错 TypeError；D. 得到字符串 6。答案：C。解析：x 是字符串，字符串不能和整数直接相加，会抛 TypeError。想拼接要先转成同类型，例如把字符串转成整数再加一得到 6，或者把整数转成字符串再拼接到后面得到 51。这说明 Python 虽然不用声明类型，但运算时类型必须匹配，否则就会报错。

## 思考题：range 与列表
问题：range(5) 包含哪些数？直接打印 range(5) 会输出列表形式吗？答案：不会。解析：Python 3 中 range 返回一个惰性的 range 对象，直接打印显示的是 range(0, 5)，而不是列表内容。但它可以被 for 循环遍历，也可以用 list 函数转成真正的列表。这种按需生成的设计能节省内存，尤其在处理很大范围的数时优势明显。

## 选择题三：列表操作
问题：nums 等于列表 1、2、3，执行 append 添加 4 后，列表长度是多少？A. 3；B. 4；C. 5；D. 报错。答案：B。解析：append 方法在列表末尾添加一个元素，列表变成四个元素，长度是 4。注意 append 没有返回值（返回 None），不要写成把返回值再赋值给列表，那样会把变量变成 None。这是初学列表时非常典型的错误。

## 思考题：字符串不可变
问题：字符串 s 等于 abc，能把第一个字符改成大写 A 吗？答案：不可以，会报 TypeError。解析：Python 中字符串是不可变对象，创建后不能修改其中某个字符。想修改只能生成一个新字符串，例如用 A 加上原字符串从第二个字符开始切片的部分拼接得到新串。理解可变（列表、字典）与不可变（字符串、数字、元组）的区别，对后续学习非常重要。

## 如何继续自测
做错的题目要回到对应章节复习，而不是只记住答案。你还可以给自己出题：把学过的每个知识点变换一个数字或条件，看看还能不能写对。坚持写、运行、对照、修正的循环，基础会越来越扎实。也可以把错题整理成笔记，定期回看，避免在同一个地方反复出错。

## 常见错误
自测时常见的误区有：只看答案不动手写，以为看懂就等于会写；忽略报错信息，不去看错误发生在哪一行；遇到不会的题马上翻答案，没有真正思考。正确的做法是先独立思考几分钟，写不出再看提示，最后对照解析弄懂原理，把每个选项为什么对、为什么错都想清楚。下面这段代码把前面几道题写成可执行的形式，你可以先心算结果再运行验证：

```python
print("第一题：", 7 // 2, 7 % 2)
nums = [1, 2, 3]
nums.append(4)
print("第四题：", nums, len(nums))
```

## 要点提示
- 自测时先独立思考，再看答案与解析，动手写比看懂更重要。
- 整除取整数商，取余得余数，斜杠除法得浮点数。
- 运算时类型必须匹配，字符串和数字不能直接相加。
- 列表可变、字符串不可变；append 方法没有返回值。""",
        "code_example": """# 自测小练习：先自己算出答案，再运行验证
print("第一题：", 7 // 2, 7 % 2)

print("第三题：", range(5), list(range(5)))

nums = [1, 2, 3]
nums.append(4)
print("第四题：", nums, len(nums))

s = "abc"
new_s = "A" + s[1:]
print("第五题：", new_s)""",
    },
]

EXERCISES = [
    # 第 40 篇：Python 多线程
    {
        "lesson_slug": "threading",
        "title": "导入线程模块",
        "description": "请使用标准库导入线程模块 threading，只写出这一行导入语句。",
        "starter_code": "# 在这里导入 threading 模块\n",
        "expected_answer": "import threading",
        "difficulty": "easy",
        "order_index": 79,
    },
    {
        "lesson_slug": "threading",
        "title": "查看活跃线程数",
        "description": "请写出一行代码：调用 threading 模块的函数，返回当前活跃的线程数量（函数名是 active_count）。",
        "starter_code": "# 在这里写一行代码，返回当前活跃线程数\n",
        "expected_answer": "threading.active_count()",
        "difficulty": "medium",
        "order_index": 80,
    },
    # 第 41 篇：Python XML 解析
    {
        "lesson_slug": "xml",
        "title": "导入 XML 解析模块",
        "description": "请把标准库 xml.etree.ElementTree 按常用别名 ET 导入，只写这一行导入语句。",
        "starter_code": "# 在这里按别名 ET 导入 ElementTree\n",
        "expected_answer": "import xml.etree.ElementTree as ET",
        "difficulty": "easy",
        "order_index": 81,
    },
    {
        "lesson_slug": "xml",
        "title": "解析 XML 文件",
        "description": "请用别名 ET 解析名为 data.xml 的文件，写出这一行调用（使用 parse 方法，文件名用双引号）。",
        "starter_code": "# 在这里写一行代码，解析 data.xml 文件\n",
        "expected_answer": 'ET.parse("data.xml")',
        "difficulty": "medium",
        "order_index": 82,
    },
    # 第 42 篇：Python GUI 编程(Tkinter)
    {
        "lesson_slug": "tkinter-detail",
        "title": "导入 tkinter 模块",
        "description": "请把 tkinter 模块按常用别名 tk 导入，只写这一行导入语句。",
        "starter_code": "# 在这里按别名 tk 导入 tkinter\n",
        "expected_answer": "import tkinter as tk",
        "difficulty": "easy",
        "order_index": 83,
    },
    {
        "lesson_slug": "tkinter-detail",
        "title": "创建主窗口",
        "description": "请用别名 tk 创建 GUI 主窗口对象，写出这一行代码（调用 Tk 类）。",
        "starter_code": "# 在这里写一行代码，创建主窗口\n",
        "expected_answer": "tk.Tk()",
        "difficulty": "medium",
        "order_index": 84,
    },
    # 第 43 篇：Python2.x 与 3.x 版本区别
    {
        "lesson_slug": "py2-vs-py3",
        "title": "Python 3 的打印",
        "description": "请用 Python 3 的函数形式输出字符串 hello，只写这一行代码（要带括号，内容用双引号）。",
        "starter_code": "# 在这里写一行代码，输出 hello\n",
        "expected_answer": 'print("hello")',
        "difficulty": "easy",
        "order_index": 85,
    },
    {
        "lesson_slug": "py2-vs-py3",
        "title": "range 转列表",
        "description": "在 Python 3 中 range(5) 是惰性对象，请写出一行表达式，用 list 函数把它转换成列表。",
        "starter_code": "# 在这里写一行表达式，把 range(5) 转成列表\n",
        "expected_answer": "list(range(5))",
        "difficulty": "medium",
        "order_index": 86,
    },
    # 第 44 篇：Python IDE
    {
        "lesson_slug": "ide",
        "title": "输出问候语",
        "description": "请写出能在任意 Python IDE 中运行、输出文本 Hello 的一行代码（用 print 函数，内容用双引号）。",
        "starter_code": "# 在这里写一行代码，输出 Hello\n",
        "expected_answer": 'print("Hello")',
        "difficulty": "easy",
        "order_index": 87,
    },
    {
        "lesson_slug": "ide",
        "title": "交互式求值",
        "description": "请在交互式环境（如 IDLE 或 Jupyter）中求表达式 2 加 3 的值，写出这个表达式本身。",
        "starter_code": "# 在这里写出求 2 加 3 的表达式\n",
        "expected_answer": "2 + 3",
        "difficulty": "medium",
        "order_index": 88,
    },
    # 第 45 篇：Python JSON
    {
        "lesson_slug": "json",
        "title": "导入 json 模块",
        "description": "请使用标准库导入 json 模块，只写这一行导入语句。",
        "starter_code": "# 在这里导入 json 模块\n",
        "expected_answer": "import json",
        "difficulty": "easy",
        "order_index": 89,
    },
    {
        "lesson_slug": "json",
        "title": "序列化为 JSON",
        "description": "变量 data 是一个字典，请用 json 模块把它序列化为 JSON 字符串，写出这一行调用（用 dumps 函数）。",
        "starter_code": "# 在这里写一行代码，把 data 转成 JSON 字符串\n",
        "expected_answer": "json.dumps(data)",
        "difficulty": "medium",
        "order_index": 90,
    },
    # 第 46 篇：Python AI 绘画
    {
        "lesson_slug": "ai-art",
        "title": "导入 turtle 模块",
        "description": "请用标准库导入海龟绘图模块 turtle，只写这一行导入语句。",
        "starter_code": "# 在这里导入 turtle 模块\n",
        "expected_answer": "import turtle",
        "difficulty": "easy",
        "order_index": 91,
    },
    {
        "lesson_slug": "ai-art",
        "title": "海龟向前移动",
        "description": "请写出一行代码：让海龟（turtle）向前移动 100 像素（调用 forward 方法）。",
        "starter_code": "# 在这里写一行代码，让海龟前进 100 像素\n",
        "expected_answer": "turtle.forward(100)",
        "difficulty": "medium",
        "order_index": 92,
    },
    # 第 47 篇：Python 100例
    {
        "lesson_slug": "examples-100",
        "title": "循环遍历 1 到 9",
        "description": "请写出一行 for 循环语句的首行：让变量 i 依次取 1 到 9（用 range(1, 10)），以冒号结尾。",
        "starter_code": "# 在这里写出 for 循环的首行\n",
        "expected_answer": "for i in range(1, 10):",
        "difficulty": "medium",
        "order_index": 93,
    },
    {
        "lesson_slug": "examples-100",
        "title": "判断偶数",
        "description": "请写出一行表达式：判断整数 n 是否为偶数（用取余运算符，结果为布尔值）。",
        "starter_code": "# 在这里写出判断 n 为偶数的表达式\n",
        "expected_answer": "n % 2 == 0",
        "difficulty": "easy",
        "order_index": 94,
    },
    # 第 48 篇：Python 测验
    {
        "lesson_slug": "quiz",
        "title": "查看数据类型",
        "description": "请写出一行代码：用 print 和 type 函数输出整数 42 的类型。",
        "starter_code": "# 在这里写一行代码，输出 42 的类型\n",
        "expected_answer": "print(type(42))",
        "difficulty": "medium",
        "order_index": 95,
    },
    {
        "lesson_slug": "quiz",
        "title": "求列表长度",
        "description": "请写出一行表达式：求列表 [1, 2, 3] 的长度（用 len 函数）。",
        "starter_code": "# 在这里写出求列表长度的表达式\n",
        "expected_answer": "len([1, 2, 3])",
        "difficulty": "easy",
        "order_index": 96,
    },
]
