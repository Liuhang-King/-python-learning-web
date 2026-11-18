"""扩展教程数据：第 5 批（Python 文件 I/O，补齐目录项）。

说明：与已有《文件读写》主题相互呼应，本篇更偏"文件 I/O 全景与模式对照"，
作为目录中的独立条目保留。
"""

LESSONS = [
    {
        "slug": "file-io-extra",
        "title": "Python 文件I/O",
        "summary": "系统认识文件的打开模式与读写方法。",
        "order_index": 49,
        "duration_min": 12,
        "content_md": """# Python 文件I/O

## 什么是文件 I/O
I/O 是 Input/Output（输入/输出）的缩写。文件 I/O 指的就是程序与磁盘文件之间的数据交换：把数据写入文件叫输出，从文件读取数据叫输入。前面《文件读写》已经用过 `open()` 的最基本用法，这一篇把文件模式和方法系统地梳理一遍，让你面对不同需求时能选对工具。

## open() 的打开模式
`open(文件名, 模式)` 的第二个参数决定能做什么，常用模式如下：`r` 只读（默认，文件不存在会报错）；`w` 只写，会先清空原文件，不存在则创建；`a` 追加，在文件末尾写入，不存在则创建；`r+` 读写，文件必须存在；`w+` 读写，会先清空；`a+` 读写，从末尾开始。模式后面还能加 `b` 表示二进制模式，比如 `rb`、`wb`，用来读写图片、音频等非文本文件。处理中文文本时建议加上 `encoding="utf-8"` 避免乱码。

## 文件对象的常用方法
打开文件得到一个文件对象，常用方法有：`read()` 读全部内容；`readline()` 读一行；`readlines()` 读所有行并返回列表；`write(内容)` 写入字符串；`writelines(列表)` 批量写入多行；`seek(位置)` 移动读写指针；`tell()` 返回当前指针位置；`flush()` 把缓冲区内容立刻写入磁盘；`close()` 关闭文件。这些方法在《File 方法》一篇会展开讲，这里先认识。

## 用 with 自动管理
无论读写，都推荐用 `with open(...) as f:` 的写法。它会在代码块执行完毕后自动调用 `close()`，即使中途出错也不会忘记关闭文件。手动 `open()` 后忘记 `close()` 是初学者常见问题，可能导致数据没写入或文件被占用。

## 文本模式与二进制模式
不加 `b` 是文本模式，读写的是字符串，会处理换行符和编码；加 `b` 是二进制模式，读写的是字节（bytes），适合图片、压缩包等。两种模式不能混用：文本模式写入字符串，二进制模式必须写入 bytes，否则会报 TypeError。

## 常见错误
第一，用 `r` 模式打开不存在的文件会报 FileNotFoundError；第二，用 `w` 模式不小心清空了重要文件；第三，路径里的反斜杠在字符串中会被当成转义符，可以写成原始字符串 `r"C:\\data\\a.txt"` 或用正斜杠。

## 要点提示
- `r` 只读、`w` 清空写、`a` 追加写，是最常用的三种模式。
- 处理中文文本加 `encoding="utf-8"`。
- 始终用 `with open(...) as f:` 自动关闭文件。
- 图片等二进制文件要用 `rb` / `wb` 模式。""",
        "code_example": """# 以不同模式操作文件
with open("demo.txt", "w", encoding="utf-8") as f:
    f.write("第一行\\n")
    f.write("第二行\\n")

# 只读
with open("demo.txt", "r", encoding="utf-8") as f:
    print(f.read())

# 逐行读取
with open("demo.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())

# 追加
with open("demo.txt", "a", encoding="utf-8") as f:
    f.write("追加行\\n")

# 二进制复制（示意）
with open("demo.txt", "rb") as src, open("demo_copy.txt", "wb") as dst:
    dst.write(src.read())""",
    },
]

EXERCISES = [
    {
        "lesson_slug": "file-io-extra",
        "title": "只读模式打开",
        "description": "请写出以只读模式打开 'a.txt'、编码为 'utf-8'、用 as f 的 with 语句头，并以冒号结尾（只写这一行）。",
        "starter_code": "# 在这里写出 with open 只读语句头（以冒号结尾）\\n",
        "expected_answer": "with open('a.txt', 'r', encoding='utf-8') as f:",
        "difficulty": "medium",
        "order_index": 97,
    },
    {
        "lesson_slug": "file-io-extra",
        "title": "写入字符串",
        "description": "已有文件对象 f，请用 f.write() 写入字符串 'hello'（只写这一行）。",
        "starter_code": "# 在这里用 f.write 写入 'hello'\\n",
        "expected_answer": "f.write('hello')",
        "difficulty": "easy",
        "order_index": 98,
    },
]
