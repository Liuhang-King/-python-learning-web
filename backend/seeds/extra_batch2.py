"""第 2 批扩展种子数据：9 篇进阶教程与 18 道配套练习题。

本模块只定义数据列表 LESSONS 与 EXERCISES，供 seed 脚本统一写入数据库。
教程的 order_index 为 22~30，练习题的 order_index 为 43~60。
"""

# ---------------------------------------------------------------------------
# 教程数据（第 2 批，order_index 22~30）
# ---------------------------------------------------------------------------
LESSONS = [
    {
        "slug": "numbers",
        "title": "Python Number(数字)",
        "summary": "深入讲解数字类型与数值运算",
        "order_index": 22,
        "duration_min": 12,
        "content_md": """# Python Number(数字)

## 数字类型概述
在 Python 中，数字是一种不可变（immutable）对象：一旦创建，其值就不能被就地修改。Python 内置了三类数字类型：int（整数）、float（浮点数）和 complex（复数）。此外，bool（布尔值）其实是 int 的子类，True 等价于 1，False 等价于 0。与其他语言不同，Python 的整数没有固定位数限制，可以表示任意精度的大整数，这让它非常适合做精确计算。可以用 type() 函数查看一个数字对象的具体类型。

## 整数与浮点数
整数就是没有小数部分的数，例如 10、-5、0。浮点数带有小数部分或指数形式，例如 3.14、1.5e3（即 1500.0）。需要注意的是，浮点数在计算机内部以二进制近似存储，因此 0.1 + 0.2 的结果往往是 0.30000000000000004，而不是精确的 0.3。在做精确比较（尤其是判断相等）时要格外小心，通常可以用 round() 限制小数位数后再比较，或改用整数运算。

## 常见算术运算
Python 支持 +（加）、-（减）、*（乘）、/（普通除法，始终返回浮点数）、//（整除/地板除，向下取整）、%（取余）、**（幂运算）。例如 7 / 2 得到 3.5，而 7 // 2 得到 3，7 % 2 得到 1，2 ** 3 得到 8。运算遵循先乘除后加减、括号优先的规则。赋值运算符还可以简写，如 x += 1 等价于 x = x + 1。

## 数值转换与数学函数
可以用 int()、float()、str() 在类型之间转换。int(3.9) 会直接截断小数部分得到 3，而 round(3.6) 四舍五入得到 4。内置的 abs() 返回绝对值，max()、min() 返回最大与最小值，pow(x, y) 等价于 x ** y。divmod(a, b) 会同时返回商和余数组成的元组，例如 divmod(7, 2) 得到 (3, 1)。需要更高级的函数（如 sqrt、sin）时可导入 math 模块。

## 常见错误
一是把整除 // 与普通除法 / 混淆，得到意外的浮点数；二是用 == 直接比较浮点数导致判断失败；三是对字符串做算术运算却没有先转换类型，例如 '10' + 5 会抛出 TypeError；四是把 int('3.5') 用于带小数的字符串，正确做法是先 float() 再 int()。

## 要点提示
- 整数精度无限，浮点数存在精度误差，比较时需谨慎。
- bool 是 int 的子类，可以直接参与算术运算。
- / 总返回浮点数，// 返回向下取整的整数。
- 类型转换用 int()、float()、str()，复杂数学函数用 math 模块。""",
        "code_example": """# 数字类型与运算示例
a = 10          # int 整数
b = 3.5         # float 浮点数
c = 2 + 3j      # complex 复数

print(type(a), type(b), type(c))   # 查看类型

print(a + 3)      # 13  加
print(a - 3)      # 7   减
print(a * 2)      # 20  乘
print(a / 4)      # 2.5 普通除法
print(a // 4)     # 2   整除
print(a % 4)      # 2   取余
print(2 ** 3)     # 8   幂运算

print(divmod(7, 2))    # (3, 1) 商和余数
print(round(3.6))      # 4      四舍五入
print(abs(-9))         # 9      绝对值
print(max(3, 8, 5))    # 8      最大值
print(int('10') + 5)   # 15     先转换再运算
""",
    },
    {
        "slug": "strings",
        "title": "Python 字符串",
        "summary": "掌握字符串方法与格式化技巧",
        "order_index": 23,
        "duration_min": 13,
        "content_md": """# Python 字符串

## 字符串是什么
字符串（str）是由一串字符组成的有序序列，用来表示文本。在 Python 中，用单引号或双引号包裹的内容都是字符串，两者完全等价。三引号（三个连续的单引号或双引号）可以定义跨多行的字符串，常用于写文档。字符串是不可变对象，创建后不能修改其中某个字符，但可以通过切片、拼接等方式生成新的字符串。

## 创建与索引
可以通过下标访问字符，s[0] 取第一个字符，s[-1] 取最后一个字符。切片 s[1:4] 取索引 1 到 3 的字符（左闭右开，含头不含尾），还支持步长写法 s[::2]。字符串支持用 + 拼接和用 * 重复，例如 'ab' * 3 得到 'ababab'。用 len(s) 可以获取字符串长度，用 in 可以判断子串是否存在。

## 常用方法
str 类型提供了大量实用方法：upper() 与 lower() 转换大小写，strip() 去除首尾空白，split(',') 按分隔符切成列表，join() 把序列拼接成字符串，replace(old, new) 替换内容，find() 查找子串位置（找不到返回 -1），startswith() 与 endswith() 判断前缀后缀，count() 统计出现次数。要特别注意：字符串不可变，所以这些方法都会返回新字符串，而不会改变原字符串本身。

## 字符串格式化
推荐使用 f-string（Python 3.6 以上版本）：在字符串前加字母 f，再用花括号嵌入变量，例如 f'你好，{name}'，既简洁又高效。此外，format() 方法和早期的 % 格式化也能实现类似功能，但在新代码中 f-string 是首选。

## 常见错误
把字符串当作列表用下标赋值（如 s[0] = 'H'）会报错；混用引号导致语法错误；忘记用 strip() 处理用户输入中多余空格；把 split() 返回的列表直接当字符串用；在 f-string 的花括号里写复杂语句。

## 要点提示
- 字符串不可变，所有修改操作都返回新对象。
- 切片左闭右开，负索引从末尾开始计数。
- f-string 是推荐的格式化方式。
- split() 与 join() 常配合使用，处理文本非常方便。""",
        "code_example": """# 字符串操作示例
s = '  Hello, Python!  '
print(s.upper())        # 全部转成大写
print(s.lower())        # 全部转成小写
print(s.strip())        # 去掉首尾空格

t = 'apple,banana,cherry'
fruits = t.split(',')   # 按逗号切成列表
print(fruits)
print('-'.join(fruits)) # 用短横线拼回一个字符串

name = '小明'
print(f'你好，{name}！')   # f-string 格式化
print(s.replace('Python', 'World'))  # 替换
print(s.count('o'))        # 统计出现次数
print(s.find('Python'))    # 查找子串位置
""",
    },
    {
        "slug": "lists",
        "title": "Python 列表(List)",
        "summary": "学会列表增删改查与排序",
        "order_index": 24,
        "duration_min": 14,
        "content_md": """# Python 列表(List)

## 列表是什么
列表（list）是 Python 中最常用的序列类型，用方括号 [] 表示，元素之间用逗号分隔。列表有序、可变，可以存放任意类型的元素，并且允许元素重复。与字符串的不可变不同，列表创建之后可以自由地增加、删除和修改元素，因此非常适合用来保存一组会变化的数据。

## 创建与访问
lst = [1, 2, 3] 创建一个列表，lst[0] 访问第一个元素，lst[-1] 访问最后一个元素。切片 lst[1:3] 得到子列表（左闭右开）。用 len(lst) 获取长度，用 in 判断元素是否存在。列表还可以嵌套，例如矩阵可以用列表的列表来表示。

## 增删改查
追加元素用 append(x)，在指定位置插入用 insert(i, x)，合并另一个列表用 extend()。删除可以用 pop()（按下标弹出并返回该元素，不传参数则弹出最后一个）、remove(x)（按值删除第一个匹配项）、del lst[i]（按下标删除）。修改元素直接赋值，如 lst[0] = 9。查找用 index(x) 返回下标，count(x) 统计元素出现次数。

## 排序与反转
sort() 方法原地升序排序，会直接改变列表本身；sorted(lst) 则返回排序后的新列表，不改变原列表。reverse() 原地反转顺序。如果需要降序，可以使用 sort(reverse=True)。排序时还能通过 key 参数指定排序规则，例如按字符串长度排序。

## 列表推导式
[x * 2 for x in range(5)] 用简洁的语法生成列表，是 Python 的特色写法，通常比手写循环更清晰。推导式还可以带条件，例如 [x for x in range(10) if x % 2 == 0] 只保留偶数。

## 常见错误
append() 每次只能添加一个元素，直接 append(另一个列表) 会形成嵌套列表，此时应该用 extend()；remove() 删除不存在的元素会报错；sort() 不返回排序结果（返回 None），不要写成 lst = lst.sort()；用 == 比较列表是按元素逐个比较的。

## 要点提示
- 列表可变、有序，允许重复元素。
- append 加单个元素，extend 合并整个列表。
- sort 原地排序，sorted 返回新列表。
- 善用列表推导式可以让代码更简洁。""",
        "code_example": """# 列表操作示例
lst = [3, 1, 4, 1, 5]
print(lst[0], lst[-1])     # 首尾元素
print(lst[1:3])            # 切片
print(len(lst))            # 长度

lst.append(9)              # 末尾追加
lst.insert(1, 10)          # 指定位置插入
print(lst)

lst.remove(1)              # 删除第一个值为 1 的元素
last = lst.pop()           # 弹出最后一个元素
print(lst, '弹出的元素:', last)

print(lst.index(4))        # 元素 4 的下标
print(lst.count(1))        # 元素 1 出现的次数

nums = sorted(lst)         # 返回排序后的新列表
print('排序后:', nums)

squares = [x ** 2 for x in range(5)]  # 列表推导式
print(squares)
""",
    },
    {
        "slug": "tuples",
        "title": "Python 元组",
        "summary": "理解元组特性与基本操作",
        "order_index": 25,
        "duration_min": 10,
        "content_md": """# Python 元组

## 元组是什么
元组（tuple）与列表非常相似，也是有序序列，但元组一旦创建就不能被修改（不可变），用小括号 () 表示。元组的不可变性让它适合存放不希望被意外改动的数据，同时由于不可变可哈希，元组还可以作为字典的键，而列表不行。在函数需要返回多个值时，Python 实际上也是用元组来打包结果的。

## 创建元组
t = (1, 2, 3) 创建一个元组。要特别注意：只包含一个元素时必须写成 (1,)，末尾的逗号不能省略，否则 (1) 只是整数 1 而不是元组。写成 t = 1, 2, 3 这种不带括号的形式同样会创建元组，这称为元组打包。空元组用一对空括号 () 表示。

## 访问与操作
元组的下标、切片、遍历方式与列表完全一样：t[0]、t[-1]、t[1:] 都可以使用。len(t) 求长度，in 判断元素是否存在，for 循环可以逐个遍历。由于不可变，元组只提供了两个方法：count(x) 统计元素出现次数，index(x) 查找元素下标。元组没有 append、remove、sort 这些会修改内容的方法。

## 元组解包
a, b = (1, 2) 会把元组中的元素分别赋给变量 a 和 b，这叫解包（unpacking），在接收函数多返回值时非常常用。还可以使用带星号的写法 a, *rest = t，让 rest 接收剩余的所有元素，从而灵活处理不定长度的数据。

## 元组与列表的转换
用 tuple(lst) 可以把列表转换成元组，用 list(t) 可以把元组转换成列表。当需要对一组数据进行临时修改时，可以先转成列表，改完后再转回元组。

## 常见错误
定义单元素元组忘记写逗号；试图对元组元素赋值（如 t[0] = 5）会抛出 TypeError；把元组误认为没有任何方法，其实它拥有 count 和 index；在需要修改数据时错误地选用了元组。

## 要点提示
- 元组不可变，用小括号表示。
- 单元素元组必须写成 (x,)，逗号不可省略。
- 只有 count 和 index 两个方法。
- 支持解包，常用作字典键和函数多返回值。""",
        "code_example": """# 元组操作示例
t = (1, 2, 2, 3)
print(t[0], t[-1])        # 索引访问
print(t[1:3])             # 切片
print(len(t))             # 长度
print(t.count(2))         # 元素 2 出现次数：2
print(t.index(3))         # 元素 3 的下标：3

# 元组解包
a, b, c, d = t
print(a, b, c, d)
first, *rest = t
print(first, rest)

# 列表与元组互转
lst = list(t)
t2 = tuple(lst)
print(lst, t2)

# 单元素元组要加逗号
single = (42,)
print(type(single), single)
""",
    },
    {
        "slug": "dictionaries",
        "title": "Python 字典(Dictionary)",
        "summary": "系统掌握字典方法与遍历",
        "order_index": 26,
        "duration_min": 14,
        "content_md": """# Python 字典(Dictionary)

## 字典是什么
字典（dict）是一种以「键-值对」（key-value）形式存储数据的映射类型，用花括号 {} 表示。字典通过键快速查找对应的值，查找速度几乎不受数据量影响。键必须是可哈希的不可变对象（如字符串、数字、元组），而值可以是任意对象。从 Python 3.7 起，字典会保持键值对的插入顺序。

## 创建与访问
d = {'name': 'Tom', 'age': 18} 创建一个字典。用 d['name'] 按键取值，如果键不存在会抛出 KeyError；更安全的做法是用 d.get('name')，键不存在时返回 None，也可以指定默认值 d.get('name', '未知')。赋值 d['city'] = '北京' 会在键不存在时新增、在键存在时修改对应的值。

## 增删改查方法
d.keys() 返回所有键的视图，d.values() 返回所有值的视图，d.items() 返回所有键值对的视图。d.pop(key) 删除指定键并返回值，d.popitem() 删除最后插入的一对，del d[key] 直接删除。d.update(other) 用另一个字典批量更新，d.setdefault(key, default) 在键不存在时为其设置默认值，d.clear() 清空整个字典。

## 遍历字典
for k in d: 默认遍历所有的键；for k, v in d.items(): 可以同时拿到键和值，这是最常用的遍历方式；for v in d.values(): 只遍历值。需要注意：不要在遍历字典的同时增加或删除键值对，否则会引发 RuntimeError，正确的做法是遍历一个副本（如 list(d.items())）。

## 字典推导式
{x: x ** 2 for x in range(5)} 可以快速构造字典。dict(zip(keys, values)) 也能从两个列表创建一个字典。字典推导式同样支持条件过滤，例如只保留值大于某阈值的条目。

## 常见错误
用列表作为字典的键会抛出 TypeError（列表不可哈希）；访问不存在的键用方括号写法会 KeyError，应改用 get()；在遍历过程中增删键值对会 RuntimeError；误以为字典是有序下标访问的序列，实际上字典没有下标，只能通过键访问。

## 要点提示
- 字典按键取值，查找速度快，键必须不可变且可哈希。
- get() 比方括号取值更安全，可以指定默认值。
- items() 是遍历键值对的首选方式。
- 遍历时不要修改字典的大小。""",
        "code_example": """# 字典操作示例
d = {'name': 'Tom', 'age': 18, 'city': '北京'}
print(d['name'])                 # 按键取值
print(d.get('gender', '未知'))   # 安全取值，带默认值

d['age'] = 20                    # 修改已有键
d['score'] = 95                  # 新增键值对
print(d)

print(list(d.keys()))            # 所有键
print(list(d.values()))          # 所有值
print(list(d.items()))           # 所有键值对

# 遍历字典
for k, v in d.items():
    print(f'{k} -> {v}')

removed = d.pop('city')          # 删除并返回值
print('删除的是:', removed, d)

# 字典推导式
squares = {x: x ** 2 for x in range(1, 5)}
print(squares)
""",
    },
    {
        "slug": "datetime",
        "title": "Python 日期和时间",
        "summary": "学会处理日期时间的常用操作",
        "order_index": 27,
        "duration_min": 12,
        "content_md": """# Python 日期和时间

## 日期时间概述
Python 通过 datetime 模块处理日期和时间。这个模块提供了几个核心类：date 只表示日期（年、月、日），time 只表示时间（时、分、秒、微秒），datetime 同时包含日期和时间，timedelta 表示一段时间间隔，timezone 用于时区处理。使用前需要先导入模块，例如 import datetime，或者 from datetime import datetime, date, timedelta。

## 获取当前时间
datetime.now() 返回当前的本地日期时间对象；date.today() 返回今天的日期。一个 datetime 对象包含 year、month、day、hour、minute、second 等属性，可以逐一访问。这些属性都是普通常量，方便我们取出想要的部分。

## 创建与格式化
可以用 datetime(2024, 1, 15, 10, 30) 直接构造一个日期时间对象。strftime('%Y-%m-%d %H:%M:%S') 把日期时间格式化成字符串：%Y 是四位年份，%m 是两位月份，%d 是日期，%H、%M、%S 分别是时、分、秒。反过来，strptime('2024-01-15', '%Y-%m-%d') 可以按照指定格式把字符串解析成日期对象，解析时格式必须与实际字符串严格对应。

## 时间运算
两个 datetime 对象相减会得到一个 timedelta 对象，可以通过 .days、.seconds 取得相隔的天数与秒数。用 datetime 加上 timedelta(days=7) 可以得到一周之后的日期。timedelta 还支持 hours、minutes、weeks 等参数，非常方便做时间的推算。

## 时间戳
time 模块中的 time.time() 返回从 1970 年 1 月 1 日至今的秒数（称为 Unix 时间戳），datetime.fromtimestamp(ts) 可以把时间戳转换回本地日期时间。时间戳常用于存储与计算时间间隔。

## 常见错误
strftime 的格式串写错，例如把表示月份的 %m 写成表示分钟的 %M；字符串解析时格式与实际内容不匹配会抛出 ValueError；把 date 对象和 datetime 对象直接比较；误以为 timedelta 只有天数，其实它还包含秒、微秒等信息。

## 要点提示
- datetime.now() 获取当前日期时间，date.today() 获取今天日期。
- strftime 负责格式化输出，strptime 负责解析字符串。
- timedelta 用于日期时间的加减运算。
- %Y-%m-%d 是最常用的日期格式。""",
        "code_example": """# 日期和时间示例
from datetime import datetime, date, timedelta
import time

now = datetime.now()          # 当前日期时间
print(now)
print('年:', now.year, '月:', now.month, '日:', now.day)
print('今天:', date.today())

# 格式化为字符串
print(now.strftime('%Y-%m-%d %H:%M:%S'))

# 字符串解析成日期对象
s = '2024-01-15'
d = datetime.strptime(s, '%Y-%m-%d')
print(d)

# 时间加减
one_week = d + timedelta(days=7)
print('一周后:', one_week.strftime('%Y-%m-%d'))

diff = one_week - d
print('相隔天数:', diff.days)

# 时间戳
ts = time.time()
print('时间戳:', ts)
print('还原:', datetime.fromtimestamp(ts))
""",
    },
    {
        "slug": "functions-detail",
        "title": "Python 函数",
        "summary": "深入参数传递、文档与lambda",
        "order_index": 28,
        "duration_min": 15,
        "content_md": """# Python 函数

## 函数回顾
函数是把一段可复用的代码封装起来的结构，用 def 函数名(参数): 定义，用 return 返回结果。前面已经介绍过函数的基本定义和调用，本篇进一步深入参数传递、函数文档和匿名函数等更细致的内容，帮助你写出更灵活、更规范的函数。

## 参数传递的几种形式
位置参数最常见：def add(a, b) 调用时按顺序传值。关键字参数允许按名字传值，如 add(b=2, a=1)，顺序可以打乱。默认参数如 def greet(name, prefix='你好')，调用时若不传入就使用默认值，要注意默认参数必须放在位置参数之后。可变参数用 *args 接收任意多个位置参数（内部是一个元组），用 **kwargs 接收任意多个关键字参数（内部是一个字典）。

## 参数传递的注意点
Python 采用「对象引用传递」。对于不可变对象（数字、字符串），在函数内重新赋值不会影响外部变量；但对于可变对象（列表、字典），在函数内原地修改会影响外部。另外，不要用可变对象作为默认参数，例如 def f(lst=[])：默认列表只在函数定义时创建一次，会在多次调用之间共享，造成数据污染。正确写法是把默认值设为 None，再在函数内创建空列表。

## 函数文档
函数体第一行的字符串是文档字符串（docstring），通常用三引号包裹，用来说明函数的用途、参数和返回值。可以用 函数名.__doc__ 查看它，用 help(函数名) 会显示更完整的信息。编写清晰的文档字符串是良好的编程习惯。

## 匿名函数 lambda
用 lambda 参数: 表达式 可以定义简洁的匿名函数，适合简单的单行逻辑，例如 square = lambda x: x ** 2。lambda 经常与 sorted()、map()、filter() 搭配使用，例如 sorted(users, key=lambda u: u['age']) 按年龄排序。lambda 体内只适合写简单表达式，复杂逻辑还是应该用 def 定义普通函数。

## 常见错误
默认参数放在位置参数之前会导致语法错误；使用可变默认参数造成数据被意外共享；在 lambda 中写多条语句或赋值；忘记 return 导致函数返回 None；混淆局部作用域与全局作用域。

## 要点提示
- 位置参数、关键字参数、默认参数可以灵活组合使用。
- *args 收集成元组，**kwargs 收集成字典。
- 不要用可变对象作为默认参数，改用 None。
- lambda 适合简单逻辑，常配合 key 参数使用。""",
        "code_example": """# 函数进阶示例

def add(a, b=10):
    '''返回两个数的和，b 默认为 10。'''
    return a + b

print(add(5))          # 15，使用默认参数
print(add(5, 3))       # 8
print(add(b=3, a=5))   # 8，关键字参数
print(add.__doc__)     # 查看文档字符串

# 可变参数
def show(*args, **kwargs):
    print('位置参数:', args)
    print('关键字参数:', kwargs)

show(1, 2, 3, name='Tom', age=18)

# 不要用可变对象作默认参数
def good_append(lst=None):
    if lst is None:
        lst = []
    lst.append(1)
    return lst

print(good_append(), good_append())  # [1] [1]，互不影响

# lambda 匿名函数
square = lambda x: x ** 2
print(square(5))       # 25
users = [{'name': 'A', 'age': 20}, {'name': 'B', 'age': 15}]
print(sorted(users, key=lambda u: u['age']))
""",
    },
    {
        "slug": "modules",
        "title": "Python 模块",
        "summary": "理解模块导入与自定义模块",
        "order_index": 29,
        "duration_min": 11,
        "content_md": """# Python 模块

## 模块是什么
模块（module）就是一个以 .py 结尾的 Python 文件，里面可以定义函数、类和变量。使用模块可以把代码组织得更清晰、便于复用，也能避免命名冲突。Python 标准库自带了大量模块，如 math、random、os、json 等，它们覆盖了数学计算、随机数、文件操作、数据交换等常见场景。

## 导入模块
用 import 模块名 导入，使用时需要通过「模块名.成员」访问，例如 import math 之后写 math.sqrt(4)。用 from 模块名 import 成员 可以直接导入具体成员，例如 from math import sqrt 之后直接写 sqrt(4)。还可以用 import math as m 给模块起别名，简化书写；而 from math import * 会把全部成员导入当前命名空间，一般不推荐使用，因为容易造成名字冲突。

## 搜索路径与 __name__
导入模块时，Python 会按 sys.path 列出的目录依次搜索。模块的 __name__ 属性非常有用：当文件被直接运行时，它的值是 '__main__'；当文件被其他模块导入时，它的值是模块名。因此常见写法 if __name__ == '__main__': 用来区分「直接运行」和「被导入」，把测试或入口代码放在这个判断里，这样被导入时就不会误执行。

## 自定义模块与包
把自己的代码保存成 mymodule.py，就可以在同级目录用 import mymodule 导入。当模块数量较多时，可以用包（package）来组织：包是包含 __init__.py 文件的文件夹，例如 my_package/utils.py 可以通过 from my_package import utils 来导入。良好的目录结构能让项目更易维护。

## 常用标准库模块举例
random 提供 random()、randint(a, b)、choice() 等随机数功能；math 提供 sqrt()、floor()、pi 等数学工具；os 提供路径与文件操作；json 提供 dumps()、loads() 完成 JSON 序列化与反序列化。

## 常见错误
把自己的文件命名为 math.py 等标准库同名文件，会导致导入时加载到自己的文件而报错；from ... import * 污染命名空间；不清楚模块的搜索路径，导致自定义模块找不到；把测试代码写在模块顶层，导致被导入时意外执行。

## 要点提示
- 模块本质就是 .py 文件，便于组织与复用。
- import 用「模块.成员」，from import 直接用成员。
- if __name__ == '__main__' 用来区分运行与导入。
- 模块名不要与标准库重名。""",
        "code_example": """# 模块使用示例
import math
import math as m
from random import randint
from math import sqrt, pi

print(math.sqrt(16))      # 4.0
print(m.floor(3.7))       # 3
print(sqrt(9))            # 3.0
print('圆周率:', pi)
print('随机数:', randint(1, 10))

# 演示 __name__ 的作用
print('当前模块的 __name__:', __name__)

if __name__ == '__main__':
    print('这是直接运行时才会执行的代码')
""",
    },
    {
        "slug": "builtins",
        "title": "Python 内置函数",
        "summary": "认识常用内置函数及其用法",
        "order_index": 30,
        "duration_min": 12,
        "content_md": """# Python 内置函数

## 内置函数概述
内置函数（built-in functions）是 Python 启动时就自动加载到内存中的函数，不需要导入即可直接使用。它们提供了最基础、最常用的功能，涵盖输入输出、类型转换、数学运算、序列操作等。可以用 dir(__builtins__) 查看所有内置名字，用 help(函数名) 查看某个函数的详细说明。掌握内置函数能显著提高编码效率。

## 输入输出与类型相关
print() 把内容输出到控制台，可以接收多个参数，默认用空格分隔。input() 读取用户输入，注意它返回的永远是字符串，做数值运算前需要用 int() 或 float() 转换。type() 返回对象的类型；isinstance(obj, type) 判断对象是否属于某类型，它会考虑继承关系，通常比 type(obj) == type 更灵活、更推荐。

## 类型转换函数
int()、float()、str()、bool() 用于基本类型转换。list()、tuple()、set()、dict() 可以在不同容器之间转换，例如 list('abc') 得到 ['a', 'b', 'c']，tuple([1, 2]) 得到 (1, 2)。这些转换函数在实际处理用户输入和数据清洗时非常常用。

## 序列操作函数
len() 返回对象长度，range() 生成整数序列，enumerate() 返回带索引的迭代器，zip() 把多个序列按位置打包，sorted() 返回排序后的新列表，reversed() 返回反向迭代器。sum() 求和，max()、min() 求最大最小值，any()、all() 分别判断条件是否「至少一个成立」和「全部成立」。

## 其他常用函数
abs() 返回绝对值，round() 四舍五入，pow() 计算幂，id() 返回对象的内存地址标识，open() 打开文件，callable() 判断对象是否可调用。这些函数虽然简单，却在日常编程中频繁出现。

## 常见错误
把内置函数名当作变量名（如 list = [1, 2]），会覆盖内置函数，导致后面调用 list() 时报错；input() 返回字符串，直接做数学运算会出错；sorted() 返回新列表而不改变原列表，忘记接收返回值；any() 与 all() 对空序列的结果分别是 False 和 True，容易搞混。

## 要点提示
- 内置函数无需导入，可直接使用。
- type() 查看类型，isinstance() 做类型判断更可靠。
- 不要用内置函数名当变量名。
- enumerate 与 zip 常配合循环使用。""",
        "code_example": """# 常用内置函数示例
print('hello', 'world')          # print 接收多个参数

x = '7'                          # 模拟 input() 得到的字符串
print('类型:', type(x))
num = int(x)                     # 转换成整数
print('平方:', num ** 2)
print('是否整数:', isinstance(num, int))

print(list('abc'))               # 字符串转列表
print(tuple([1, 2, 3]))          # 列表转元组
print(len('hello'))              # 长度

nums = [3, 1, 4, 1, 5]
print(sum(nums), max(nums), min(nums))
print(sorted(nums))              # 返回新列表
print(list(enumerate(['a', 'b'])))        # 带索引
print(list(zip([1, 2], ['a', 'b'])))      # 打包

print(any([False, True]), all([True, True]))
""",
    },
]

# ---------------------------------------------------------------------------
# 练习题数据（第 2 批，order_index 43~60）
# expected_answer 为精确的单行代码文本，判分按字符串规范化比对，不执行代码。
# ---------------------------------------------------------------------------
EXERCISES = [
    # 第 1 篇：Python Number(数字)
    {
        "lesson_slug": "numbers",
        "title": "计算幂运算",
        "description": "写一行代码，用 print() 输出 2 的 3 次幂（使用 ** 运算符）。",
        "starter_code": "# 在这里写一行代码，输出 2 的 3 次幂\n",
        "expected_answer": "print(2 ** 3)",
        "difficulty": "easy",
        "order_index": 43,
    },
    {
        "lesson_slug": "numbers",
        "title": "整除运算",
        "description": "写一行代码，用 print() 输出 7 整除 2 的结果（使用 // 运算符）。",
        "starter_code": "# 在这里写一行代码，输出 7 整除 2 的结果\n",
        "expected_answer": "print(7 // 2)",
        "difficulty": "medium",
        "order_index": 44,
    },
    # 第 2 篇：Python 字符串
    {
        "lesson_slug": "strings",
        "title": "字符串转大写",
        "description": "写一行代码，用 print() 输出字符串 'hello' 转换成大写后的结果（使用 upper 方法）。",
        "starter_code": "# 在这里写一行代码，输出 'hello' 的大写形式\n",
        "expected_answer": "print('hello'.upper())",
        "difficulty": "easy",
        "order_index": 45,
    },
    {
        "lesson_slug": "strings",
        "title": "字符串长度",
        "description": "写一行代码，用 print() 输出字符串 'Python' 的长度（使用内置函数 len）。",
        "starter_code": "# 在这里写一行代码，输出 'Python' 的长度\n",
        "expected_answer": "print(len('Python'))",
        "difficulty": "medium",
        "order_index": 46,
    },
    # 第 3 篇：Python 列表(List)
    {
        "lesson_slug": "lists",
        "title": "追加列表元素",
        "description": "假设已有列表 lst = [1, 2, 3]，写一行代码把元素 4 追加到 lst 的末尾（使用 append 方法）。",
        "starter_code": "# 已有列表 lst = [1, 2, 3]，在这里写一行代码追加元素 4\n",
        "expected_answer": "lst.append(4)",
        "difficulty": "easy",
        "order_index": 47,
    },
    {
        "lesson_slug": "lists",
        "title": "列表原地排序",
        "description": "假设已有列表 lst，写一行代码对 lst 进行原地升序排序（使用 sort 方法）。",
        "starter_code": "# 已有列表 lst，在这里写一行代码对 lst 原地升序排序\n",
        "expected_answer": "lst.sort()",
        "difficulty": "medium",
        "order_index": 48,
    },
    # 第 4 篇：Python 元组
    {
        "lesson_slug": "tuples",
        "title": "创建元组",
        "description": "写一行代码，创建一个包含元素 1 和 2 的元组，并赋值给变量 t。",
        "starter_code": "# 在这里写一行代码，创建元组 (1, 2) 并赋值给 t\n",
        "expected_answer": "t = (1, 2)",
        "difficulty": "easy",
        "order_index": 49,
    },
    {
        "lesson_slug": "tuples",
        "title": "统计元组元素",
        "description": "假设已有元组 t = (1, 2, 2, 3)，写一行代码用 print() 输出元素 2 出现的次数（使用 count 方法）。",
        "starter_code": "# 已有元组 t = (1, 2, 2, 3)，在这里写一行代码输出元素 2 的次数\n",
        "expected_answer": "print(t.count(2))",
        "difficulty": "medium",
        "order_index": 50,
    },
    # 第 5 篇：Python 字典(Dictionary)
    {
        "lesson_slug": "dictionaries",
        "title": "获取所有键",
        "description": "假设已有字典 d，写一行代码用 print() 输出字典 d 的所有键（使用 keys 方法）。",
        "starter_code": "# 已有字典 d，在这里写一行代码输出所有键\n",
        "expected_answer": "print(d.keys())",
        "difficulty": "easy",
        "order_index": 51,
    },
    {
        "lesson_slug": "dictionaries",
        "title": "安全获取字典值",
        "description": "假设已有字典 d，写一行代码用 get 方法安全地获取键 'name' 对应的值（键不存在时返回 None）。",
        "starter_code": "# 已有字典 d，在这里写一行代码用 get 获取键 'name' 的值\n",
        "expected_answer": "d.get('name')",
        "difficulty": "medium",
        "order_index": 52,
    },
    # 第 6 篇：Python 日期和时间
    {
        "lesson_slug": "datetime",
        "title": "导入 datetime 类",
        "description": "写一行代码，从 datetime 模块中导入 datetime 类。",
        "starter_code": "# 在这里写一行代码，从 datetime 模块导入 datetime 类\n",
        "expected_answer": "from datetime import datetime",
        "difficulty": "easy",
        "order_index": 53,
    },
    {
        "lesson_slug": "datetime",
        "title": "输出当前时间",
        "description": "假设已执行 from datetime import datetime，写一行代码用 print() 输出当前的日期时间（使用 now 方法）。",
        "starter_code": "# 已导入 datetime 类，在这里写一行代码输出当前日期时间\n",
        "expected_answer": "print(datetime.now())",
        "difficulty": "medium",
        "order_index": 54,
    },
    # 第 7 篇：Python 函数
    {
        "lesson_slug": "functions-detail",
        "title": "定义平方 lambda",
        "description": "写一行代码，定义一个名为 square 的 lambda 函数，接收参数 x 并返回 x 的平方。",
        "starter_code": "# 在这里写一行代码，定义 lambda 函数 square 返回 x 的平方\n",
        "expected_answer": "square = lambda x: x ** 2",
        "difficulty": "easy",
        "order_index": 55,
    },
    {
        "lesson_slug": "functions-detail",
        "title": "定义求和 lambda",
        "description": "写一行代码，定义一个名为 add 的 lambda 函数，接收两个参数 a 和 b 并返回它们的和。",
        "starter_code": "# 在这里写一行代码，定义 lambda 函数 add 返回两数之和\n",
        "expected_answer": "add = lambda a, b: a + b",
        "difficulty": "medium",
        "order_index": 56,
    },
    # 第 8 篇：Python 模块
    {
        "lesson_slug": "modules",
        "title": "导入 math 模块",
        "description": "写一行代码，导入 math 模块。",
        "starter_code": "# 在这里写一行代码，导入 math 模块\n",
        "expected_answer": "import math",
        "difficulty": "easy",
        "order_index": 57,
    },
    {
        "lesson_slug": "modules",
        "title": "输出圆周率",
        "description": "假设已导入 math 模块，写一行代码用 print() 输出圆周率 pi 的值。",
        "starter_code": "# 已导入 math 模块，在这里写一行代码输出圆周率 pi\n",
        "expected_answer": "print(math.pi)",
        "difficulty": "medium",
        "order_index": 58,
    },
    # 第 9 篇：Python 内置函数
    {
        "lesson_slug": "builtins",
        "title": "求列表最大值",
        "description": "写一行代码，用 print() 输出列表 [1, 2, 3] 中的最大值（使用内置函数 max）。",
        "starter_code": "# 在这里写一行代码，输出列表 [1, 2, 3] 的最大值\n",
        "expected_answer": "print(max([1, 2, 3]))",
        "difficulty": "easy",
        "order_index": 59,
    },
    {
        "lesson_slug": "builtins",
        "title": "列表元素求和",
        "description": "写一行代码，用 print() 输出列表 [1, 2, 3, 4] 所有元素之和（使用内置函数 sum）。",
        "starter_code": "# 在这里写一行代码，输出列表 [1, 2, 3, 4] 所有元素之和\n",
        "expected_answer": "print(sum([1, 2, 3, 4]))",
        "difficulty": "medium",
        "order_index": 60,
    },
]
