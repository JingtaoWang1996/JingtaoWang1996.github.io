---
title: 'python-notes'
date: 2023-05-15
permalink: /posts/2023/05/python-notes/
tags:
  - cool posts
  - category1
  - category2
---

python related contents.

# 开发相关

## 带参数启动

通过python自带的argparse 带参数启动脚本

```python
import argparse

def param_parse():
    # 配置参数实例
    parser = argparse.ArgumentParser(description="input params")
    # required = 是否必传，default
    parser.add_argument('--参数长名称', '-参数短名称', required=True, choices=["可选参数值列表"],help="参数说明")
    parser.add_argument('--enable_ipv6', '-v6', default="默认值", choices=["True", "False"],help="参数说明")
    return parser.parse_args()

if __name__ == '__main__':
    # 启动命令参数配置解析:
    args = param_parse()
    logger.debug("输入参数使用:%s,%s,%s", args.enable_ipv6, args.node, args.query_all)
```

具体使用：[更多使用，搜索argparse]

1）启动脚本：python3 xxxx.py -参数短名称1 参数值 -参数短名称2 参数值 -参数短名称3 参数值

2）参数说明帮助：python3 xxxx.py -h

## 配置文件

常用的3种配置文件：.ini,.yml,.py

1） .ini: 直接使用python编译器自带 configparser 库读取；无法执行脚本（读取时执行）；数据需要转换。

2） .yml: 包含**大部分数据格式，无需转换**。依赖第三方库读取文件

3） .py：类似代码模块直接import

### .ini 作为配置文件例子

```.ini
[nodeStatus]
# 此类元素为str
nodeStatusTopic = activeNodeStatus

[ipv4] # section 名称不重复
# list 元素用,隔开
nodeStatusTopic = 42.83.189.4,1.2.3.4 #
# dict 元素例子
practice_dict = {'1.1.1.1':['abcd123'],'1.2.1.1':['adsss']}
```

对应python读取.ini 文件方式如下

```python
import configparser

conf = configparser.ConfigParser()
conf.read("path")  # .ini 配置文件路径
hosts = conf.get("section_name", "具体参数名称")  # str
ip_list = conf.get("section_name", "ipv4").split(",")  # str2list
# 类型强转
ip_int = int(conf.get("section_name", "ipv4").split(",")[0])  # str2int
str2dict = eval(conf.get("section","practice_dict")) # str2dict
```

## 项目依赖模块导入

* 文件名称：requirements.txt

* 文件写法：**[****每个依赖一行，中间双等号，最后没有任何符号]**

​      alembic ==1.0.10

​      click == 7.0

​      …

* 文件使用---pip 安装项目环境的依赖：pip install -r requirements.txt

​       PS: 依赖写入requirements.txt 中：

* pip freeze >requirements.txt

## 开发规范

[参考]:http://mpwang.github.io/2019/10/20/python-convention/

* Import：

​      1）使用独立的行导入一个模块

​      2）原则上禁止 import *，需要明确列出引用模块，以免无法找到变量定义的模块&修改import引起其他问题

​      3）顺序：pycharm optimize imports 功能格式化导入语句，避免手动管理，除非有明确的导入先后顺序。

* 命名：

  1） 任何地方避免使用短横线“-”

  2） 避免使用 \__xxx__ 形式的名字, 这种形式的名字(magic method)保留给 Python 解析器使用

  3） 避免使用单个字符作为变量名

  4） 不要使用双下划线的形式（\__xx），使用单下划线开头表示私有变量（\_x）

  5） 相互关联的类及函数放在一个模块中，不要限制一个模块只有一个类

  **6）** **类的命名使用驼峰CamelCase（eg：class CapWords）**

  **7）** **类所在的文件名使用：snake_case（eg：cap_words.py）**

  | 名字              | 公开变量           | 内部变量                        |
  | ----------------- | ------------------ | ------------------------------- |
  | 包                | lower_with_under   | 文件夹都是包，都小写+下划线     |
  | 模块              | lower_with_under   | .py 文件都是模块，都小写+下划线 |
  | 类                | CapWords           | 驼峰                            |
  | 异常              | CapWords           | 驼峰                            |
  | 函数              | lower_with_under() | 小写+下划线                     |
  | 全局常量/类常量   | CAPS_WITH_UNDER    | _CAPS_WITH_UNDER                |
  | 全局变量/类变量   | lower_with_under   | 小写+下划线                     |
  | 对象变量          | lower_with_under   | 小写+下划线                     |
  | 方法名            | lower_with_under   | 小写+下划线                     |
  | 函数/方法  参数名 | lower_with_under   | 小写+下划线                     |
  | 局部变量名        | lower_with_under   | 小写+下划线                     |

* 描述

​       函数名、类方法以动词开头；类名，类属性以名词开头

* Main 方法

​      在编写可执行的 Python 脚本时, 必须使用 if \_\_name\__ == '\__main__'：

​      单元测试，自动文档生成、静态代码分析等工具都会import模块，必须使用__name__ 检查以防止该脚本import时候会运行，可执行脚本必须提供main方法

* 注释

​       非直挂代码需要进行注释，注释也需要更新，注释在代码前尽量

* 包：使用模块的全路径名来导入每个模块，避免冲突问题，同时写全路径避免相对路径在大型项目中同名模块or移动模块带来的问题

* 类：直接class MyClass： 即可，__init__ 方法初始化所有实例变量

  class Square:
     def \_\_init\_\_(self, side):
       self._side = side
       self.area = side ** 2

* 异常：自定义异常多以Error结尾，继承Exception，可自定义异常

  class MyError(Exception):

  pass

  PS: 没有特殊处理要求，body可以直接pass

  1） 异常抛出形式：raise MyError(“error message”)

  2） 注意捕获异常的范围：不要except捕获所有异常，除非debug确认一定出现的异常，否则代码正常运行。

## 日志模块-logging

### 使用

配置

```
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

# 日志存放目录
log_path = "logs/"
# 设置日志handler参数，最大文件128M,保留7个备份
log_handler = RotatingFileHandler(filename=log_path + "active_dns.log", maxBytes=128 * 1024 * 1024, backupCount=7)
# 设置日志handler参数，只保留最近7天的日志
# log_handler = TimedRotatingFileHandler(filename="active_dns.log", when="D", interval=1, backupCount=7)

# 设置日志输出format
log_format = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
log_handler.setFormatter(log_format)
# 设置日志输出等级
logger = logging.getLogger("active_dns")
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)  # 此处设置为INFO,则debug信息不会输出,查看数据输出时修改为logging.DEBUG
```

使用

```python
from configuration.log_setting import logger, log_handler
logger.info("aaaaa") # 日志信息
log_handler.close() # 日志切换时关闭句柄
```

### 消息等级

FATAL：致命错误

CRITICAL：特别糟糕的事情，如内存耗尽、磁盘空间为空，一般很少使用

ERROR：发生错误时，如IO操作失败或者连接问题 

WARNING：发生很重要的事件，但是并不是错误时，如用户登录密码错误

INFO：处理请求或者状态变化等日常事务

DEBUG：调试过程中使用DEBUG等级，如算法中每个循环的中间状态

log 命令能够显示不同级别参数和消息，消息等级大写：INFO,DEBUG

**ps: info** **能够看到 warning info****； debug** **能够看到 info debug warning error critical**

  **critical** **只能看到critical   error** **能看到critical** **和 error**

## 类class的使用

参考：[菜鸟教程](https://www.runoob.com/python3/python3-class.html)、[其他blog](https://www.cnblogs.com/chengd/articles/7287528.html)

### 基本定义

* 类：描述具有相同的属性和方法的对象集合，定义该集合每个对象共有的属性和方法

* 对象：类的实例

* 方法：类当中定义的函数

* 类变量：整个实例化对象中公用，类变量定义在类中且在函数体之外，通常不作为实例变量使用。

* 局部变量：定义在方法中的变量，只作用于当前实例的类。

* 实例变量：在类的声明中，属性通过变量来表示，这种变量称为实例变量，即：用self修饰的变量。

* 实例化：创建一个类的实例，类的具体对象。

### 实例

```
import folium


class mapSettings: 具体类
    def __init__(self): # 该方法实例化时会自动调用，可以有参数，参数通过该方法传到实例化操作上
        # 类变量
        self.map2loc_city = {"Buffalo": [42.886, -78.88]}
        self.map2loc_pos = {"UB": [43.002, -78.785]}
        self.map_center = self.map2loc_city["Buffalo"]  # 控制地图中心点的坐标
        self.map = folium.Map(location=self.map_center, zoom_start=13)
        self._private = "1111" # 私有属性，外部无法直接访问
    # 方法
    def add_loc_maker(self):
        # 添加标注
        for key in self.map2loc_city:
            folium.Marker(self.map2loc_city[key], popup=key).add_to(self.map)
        for key in self.map2loc_pos:
            folium.Marker(self.map2loc_pos[key], popup=key).add_to(self.map)


if __name__ == "__main__":
    m = mapSettings() # 实例化类
    m.add_loc_maker() # 实例化后访问类的方法
    # 保存地图
    m.map.save("map.html")
```

PS: 类的方法与普通函数只有一个区别---类方法当中第一个参数必须是self

PPS:私有属性定义方式是在前面加上下划线； 外部可以调用公有方法，公有方法当中可以再调取私有方法

### 子类继承基类

Cat 类继承Animal 基类，并在初始化的时候，通过super（类，self）._init_(name,age) 引入基类animal初始化中的所有属性。

```python
class Animal(object):  # 所有类都可以继承object基类
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __call__(self, *args, **kwargs):
        print(self.name, "barking!")


class Cat(Animal):  # cat 继承Animal
    def __init__(self, name, age, sex): # 多一个sex属性
        super(Cat, self).__init__(name, age)  # 从animal类引入属性
        self.sex = sex # 初始化sex

if __name__ == "__main__":
    c = Cat("喵",2,"male")
    c.call()
```

## 工程中互相import 文件

从一个目录import另一个目录中的文件

### 相对导入

- project/
  - main.py
  - directory/
    - module.py

要在main.py中导入module.py：from directory import module

### 绝对导入

从一个完全不同的目录导入文件，使用`sys.path.append()`将另一个目录添加到Python的搜索路径中，然后使用`import`语句导入文件。

```python
import sys
sys.path.append('/path/to/directory') # 在sys系统中添加要导入的module的路径

import module
```

## 性能相关

python 中性能多于高并发、多进程、多线程、进程池、线程池、异步等相关

### 信号量---semaphore

​        用于多线程中控制对共享资源的访问，主要有两个操作：wait & signal。在多个线程同时访问共享资源时，wait检查信号量的值：为0则阻塞当前线程等待资源访问释放；否则表示可以访问，此时信号量-1继续执行。signal +1 通知其线程有可用的资源。

内置计数器：

* 每当调用acquire() 时，内置计数器-1，realse() 时，内置计数器+1
* 计数器不能小于0，当计数器为0时，acquire() 将阻塞线程直到其他线程调用release()
* 内置计数器大小可以通过参数进行设置

### 进程相关

​        与多进程相关的库，常用：[multiprocessing](https://docs.python.org/3/library/multiprocessing.html)，multiprocessing当中包含Process类和Pool 类，用于构造多进程和进程池。

```
import multiprocessing
from multiprocessing import Process, Pool

# 创建进程池
pool = Pool(multiprocessing.cpu_count())
# 创建进程
p = Process(target=目标方法, args=(传入的参数))
# 进程类相关方法
p.is_alive() # 返回进程是否在运行
p.start() # 启动进程
p.terminate() # 终止进程
```

#### 多进程之间数据共享

multiprocessing 库通过manager 实现多进程数据共享，数据类型dict，list 等

```
from multiprocessing import Manager
# 多进程共享字典
mg = Manager()
mg.dict()
```

#### 进程池

创建完进程池后，可以调用apply_async 方法进行进程池异步调用，其他进程方法具体查询

```
def task2pool(current_round_tasks, update_round):
    # 向进程池中非阻塞添加及执行任务，通过进程池管理任务状态,最后一个逗号是必须的
    for i in range(dns_conf.max_process):
        async_result = pool.apply_async(create_loop, args=(a, b,)) # 存下异步状态
        # 为了检查进程状态
        result.append(async_result)
       
if __name__ == '__main__':
   for async_result in result:
      if not async_result.ready(): # 判断异步任务是否结束
          logger.warning("Too many tasks!")  # 任务过多查不完告警
              break
```

#### 多进程间数据交换

Queue 模块构造生产消费模型进行消费队列

* get & put 方法

```
import queue

q = queue.Queue(maxsize=10)  # 构造队列
q.put(1)  # 向队列中放入参数 
q.get()  # 从队列中取值
```

* join & task_done()

  join 阻塞进程，直到所有任务完成，需要配合task_done(）

```
import queue
def join(self):
    with self.all_tasks_done:
        while self.unfinished_tasks:
            self.all_tasks_down.wait()

q = queue.Queue(5)
q.put(10)
print(q.get())
q.task_done()  # task_done() 表示某个任务完成，每一条get语句后需要一条task_done
```

* 其他队列常用方法

```
import queue

q = queue.Queue()
q.qsize()  # 队列大小
q.empty() # 队列是否为空
q.full() # 队列是否为满
q.get_nowait() # 相当于q.get(False) 非阻塞
q.put_nowait(item="111") # 相当于q.put(False) 非阻塞
```

### 线程相关

#### threading 类创建

```
import threading

t = threading.Thread(target=函数, args=(参数1, 参数2,))  # 最后一个逗号必须
# t.setDaemon(True) # 将线程声明为守护线程，在start方法之前调用
t.start()  # 启动线程

# t.join(timeout = 10) # 所有子线程结束前阻塞父线程，timeout设置超时参数
```

* 若不设置守护线程，程序将会无限挂起（设置了守护线程，主线程完成后，可以不等待子线程退出）

thread 实例对象的其他方法

*   Xxx.is\_alive() # xxx线程是否存活
*   Xxx.getName() # 返回线程名
*   Xxx.setName() # 设置线程
*   Threading.currentThread() # 返回当前的线程变量
*   Threading.enumerate() # 返回一个包含正常运行的线程list
*   Threading.activeCount()#正在运行的线程数量 = len（threading.enumerate()）

### 锁

#### 全局解释器锁GIL（Global Interpret Locker）

​        Python 中的线程是操作系统的原生线程，为了支持多线程机制，**一个基本要求就是要实现不同线程对共享资源访问的互斥**。因此GIL被提出：在一个线程拥有了解释器的访问权后，其他所有线程都必须等待它释放解释器的访问权，即使这些线程的下一条指令并不会互相影响。

* 优点：避免大量加锁解锁操作； 缺点：多处理器退化为单处理器（组合为1个处理器）

* 影响：无论启多少个线程，有多少个CPU, python在执行一个进程的时候在同一个时刻，只能允许一个线程运行。因此，python无法利用多核CPU实现多线程。

  PS:**这种情况对计算密集型任务效果不如串行（无大量切换）,但是对IO密集型的任务效率有显著提升。**

  ​     ---- 解决只能使用单进程的方案：multiprocessing 代替Thread（multiprocessing，弥补thread库因为GIL而低效的缺陷。和thread不同的地方在它使用多进程而非多线程。每个进程有自己独立的GIL，不会出现进程之间争抢GIL。 **In conclusion: 因为GIL的存在，只有在IO密集型场景下多线程会获得较好性能，计算密集型不会。**

#### 同步锁

* **常用于实现对共享资源的同步访问，为每一个共享资源创建一个lock对象，当需要访问该资源时，调用acquire方法来获取锁对象（如果其他线程已经获得了该锁，则当前线程需要等待其被释放），待资源访问完后，再调用release访问释放锁**

​       PS:为什么有GIL还需要线程同步：保证同一时刻，只有一个线程对共享资源进行获取

#### 死锁

* **两个或两个以上进程或线程再执行过程中，因争夺资源而造成相互等待的现象**。若无外力作用，他们都将无法推进下去，此时称系统处于死锁状态或系统产生了死锁，这些永远再互相等待的进程成为死锁进程。【Solution】Python中为了多次请求同一资源，可以设置重入锁RLock，其内部维护一个lock和一个counter变量，counter记录请求资源的次数，从而使得资源可以被多次请求，**直到所有acquire被release之后其他线程才能获得资源，用Rlock替换lock之后不会发生死锁**。

#### 同步锁

### 事件对象--Event

​       因为线程都是独立运行且状态不可预测，如果**代码中的其他线程需要通过判断某个线程的状态来决定下一步的操作，就需要使用threading库当中的event对象**。Event 对象包含可由线程设置的信号标志，运行线程----最开始这个event设置为假；当设置为真时，视为这个进程结束，同时唤醒所有等待这个event对象的进程。

* Event.isSet（）； # 返回event的状态值
* Event.wait()   # 如果event.isSet == False 将阻塞线程。
* Event.set();   # 设置event 的状态为True
* Event.clear();  # 恢复event的状态值为False

​       可以考虑一种应用场景（仅仅作为说明），例如，我们有多个线程从Redis队列中读取数据来处理，这些线程都要尝试去连接Redis的服务，一般情况下，如果Redis连接不成功，在各个线程的代码中，都会去尝试重新连接。如果我们想要在启动时确保Redis服务正常，才让那些工作线程去连接Redis服务器，那么我们就可以采用threading.Event机制来协调各个工作线程的连接操作：主线程中会去尝试连接Redis服务，如果正常的话，触发事件，各工作线程会尝试连接Redis服务。(flink 当中不存在主线程的问题，流处理的情况都是主线程。)

### Asyncio /Trio

封装后的异步python非阻塞库，两个库各有优缺点

#### 分布式进程

[参考](https://blog.csdn.net/lilong117194/article/details/76051843)

将process进程分布到多台机器上，在python 中仍然需要利用multiprocessing 模块。

Multiprocessing 模块不仅支持多进程，其中的managers 子模块还支持把多进程分到多台机器上。可以写一个服务进程作为调度，将任务分布到其他子进程中，依靠网络通信管理。

创建分布式进程需要分为6个步骤：

1）建立Queue队列，用来进行进程间的通信，服务进程创建任务队列task_queue,用来回传任务给任务进程通道；服务进程创建结果队列 result_queue作为任务进程完成后回复服务进程的通道。在分布式多进程环境下，必须通过由QueueManager获得的Queue接口来添加任务。

2）把第一步中建立的队列在网络上注册，暴露给其他进程，注册后获得网络队列，相当于本地队列的映像

3）建立第一个对象Queuemanager（Base manager）manager，绑定端口和验证口令。

4） 启动第三部中建立的实例，即启动管理manager，监管信息通道。

5） 通过管理实例的方法获得通过网络访问Queue对象，即再把网络队列实例化成可以使用的本地队列。

6）创建任务到“本地”队列，自动上传任务到网络队列中，分配给任务进程进行处理

在Thread 和 process 中，优先选择Process,因为process 更稳定，且能够分不到多台机器上，Thread 只能分不到同一台机器的多个CPU上。可以通过multiprocessing 的manager子模块将任务分布到多台子机器上，一个服务进程作为任务调度者，将任务分布到其他多个进程中，依靠网络通信。

PS：manager 模块封装较好，可以直接使用，编写分布式多进程程序。

### 协程 coroutine

[协程又称微线程，纤程，一种用户态的轻量级线程。](https://www.cnblogs.com/yuanchenqi/articles/6755717.html)

协程拥有自己的寄存器上下文和栈。调度切换时，将寄存器上下文和栈保存到其他地方，在切换回来的时候，恢复先前保存的寄存器上下文和栈。因此：协程能够保留上一次调用时候的状态（即：所有局部状态的一个特定组合），每次过程重入时，就相当于进入上一次调用的状态（上一次离开时所处逻辑流的位置）

优点:

1) 无需线程上下文切换的开销； 2）无需原子操作锁定及同步开销； 

3）方便切换控制流，简化编程模型。4）高并发+高扩展性+低成本： 一个CPU支持上万个协程都不是问题，很适合高并发处理。

缺点：

1） 无法利用多核资源：协程的本质是个单线程，它不能同时将单个cpu的多核利用上，需要和进程配合才能用在多个CPU上，当然常见的绝大部分应用没有这个必要，除非是CPU密集型应用。

2） 进行阻塞操作（IO）时会阻塞掉整个程序。

### 性能相关问题记录

* 不同系统允许的最大并发数不一致： 在windows 和 linux 不同平台下，系统内核能够用于发送任务的loop数量不一致，**windows 下是512，Linux下是1024。**

  PS1: ulimit -n 查看并发数 & 可以永久修改系统最大链接数（最大并发数）

  PS2: 在不永久修改最大链接、并发数的情况下的解决办法，采用sem 对selector 的数量进行限制， windows 限制在500，linux 限制在1000。一个进程的当中的Loop任务达到该数量级之后，进程开始等待，直到loop当中的任务数量级降低再继续执行。

  PS3: 最大并发可具体修改

* 异步进程卡顿:当中执行某一个异步非阻塞task 时，使用 asyncio.wait_for(future，timeout=) 当timeout 超时之后，该过程仅仅时取消请求，但wait_for 仍然可能在协程当中运行切返回,[参见](https://bugs.python.org/issue32751)

  解决思路：1）python multiprocessing库下Process 进程是否可以设置超时

  ​                   2）process 经常卡顿可能是由于内存不足；

  ​                   3）进程启动时定时回收所有开启的子进程（使用work.kill(), 替代 kill -9）

# pycharm相关

## 同时执行多个程序

Run -> Edit Configurations -> 勾选Allow parallel run前面的框 [示例见下图]

## 运行带参数脚本

Run -> Edit Configurations -> 选择脚本后，右侧“parameters“ 中添加参数

![pycharm运行参数配置图](./img/pycharm运行参数配置图.png)

## pycharm中修改源码库

* 以“管理员身份运行”，才能进行第三方库修改及保存

* 理解源码过程中：

  1） 通过debug方式，一步一步走，观察函数调用关系

  2） class 和方法中的每一个参数，都需要仔细看（包括传入的class类的所有参数，以及所有参数中方法以及class的具体实现&初始化等等，其中是否有具体的参数实现上述问题）

## 问题记录

* 运行报错

  1）报错信息：error running ‘newfiletest’:Unexpected content storage modification: page=15, 1）newRecord=23581

  2）问题说明：pycharm 意外关闭，无法正常编译代码

  3）解决方案：删除C盘相关数据重启即可



# pip 换源

* pip install -i https://pypi.douban.com/simple module # 使用豆瓣源

* pip install -i http://mirrors.aliyun.com/pypi/simple/ module # 阿里云

* pip install -i https://pypi.mirrors.ustc.edu.cn/simple/ module # 中国科技大学

* pip install -i http://pypi.douban.com/simple/ module # 豆瓣(douban)

* pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ module # 清华大学

* pip install -i http://pypi.mirrors.ustc.edu.cn/simple/ module # 中国科学技术大学

# 环境配置

## centos 编译安装 python

* [Gzipped source tarball](https://www.python.org/ftp/python/3.8.5/Python-3.8.5.tgz) 是linux 对应的源码包

* 具体安装步骤

  * 将1）中提到的源码压缩包上传到 /root/ 路径下

  * 解压上述tar.gz 包：tar -zxvf python-3.8.5.tgz

  * cd 到对应解压目录下: cd /root/Python-3.8.5

  * 依次执行:

  ​       * ./configure

  ​       * sudo make & make install

  * 测试 python3 是否安装成功，键入命令：python3

* 源码编译安装python 之前需要的[依赖](https://www.cnblogs.com/bigriverx/p/8743008.html)安装

* 编译安装python的[所有命令](https://blog.csdn.net/kan2016/article/details/81276996)

* Ubuntu 装python[步骤](https://blog.csdn.net/halazi100/article/details/97117369)

# conda命令 

## 环境相关

* 查看当前存在的虚拟环境：conda env list

* 创建conda虚拟环境：conda create -n 虚拟环境名 python=3.6

* 激活虚拟环境：conda activate 虚拟环境名

* 关闭虚拟环境：conda deactivate 虚拟环境名

* 删除虚拟环境：conda remove -n 虚拟环境名 --all

* 检查更新当前conda环境：conda update conda

* 环境迁移 --- 本机克隆

  1） 克隆老环境构建新环境：conda create --name 新环境名称 --clone 老环境名称

  2） 激活新环境：conda activate 新环境环境迁移：

* 环境迁移 --- 迁移到其他服务器

  1）安装conda-forge & conda-pack 打包工具：conda install –c conda-forge conda-pack

  2）打包当前环境：conda pack -n 新环境 -o 新环境.tar.gz

## 第三方库相关

* 查看当前环境安装的包：激活后执行---conda list
* 虚拟环境中安装新第三方库：conda install -n 虚拟环境名 要安装的包 | pip3 install 要安装的

# 数据结构

## 堆heapq

* 小根堆：父节点**小于等于**所有子节点
* 大根堆：父节点**大于等于** 所有子节点
* **python实现：默认为小根堆 == 最小值为父节点，根堆list第一个元素永远最小**

```
import heapq

nums, k = list(), 10
q = [(-nums[i], i) for i in range(k)] # 初始化k窗口大小的list
print(q)
heapq.heapify(q) # list 转为堆，默认小根堆
print(q)
# 入队：heapq.happush(q, (-nums[i], i))  # 入队新的元素
# 出队：heapq.heappop(q)
```

## hash-dict

* 将字典中单引号修改为双引号：json.dumps()

```
import json

a = {"a": "aaaa"}
b = json.dumps(a) # b={'a':'aaaa'}  
```

* 按照dict的值来排序  **a = sorted(dict.items(),key = lambda x: x[1],reverse = True)** 

## 进制转换

* 十进制转二进制：bin（x）

* 二进制转十进制：int(data,2)  --- data是str类型二进制

## 线段树

* 定义：类似于二叉树，每个父节点存两个子节点的值，构成线段树的结构。

* 与树状数组的区别：树状数组能解决的问题线段树都可以解决，但树状数组的系数比线段树少很多。

* 两者构建：线段树：类似于二叉树，每个父节点存两个子节点的值，构成线段树的结构。

## 树状数组 

* binary Index Tree/ 二进制下标树 Fenwick Tree

* 定义：数组来模拟树形结构，解决大部分基于区间上的更新及求和问题。数组的下标模拟二进制的方式来进行求和计算。

* 功能及时间复杂度

  * 单点修改：更改数组中的一个元素值

  * 区间查询：查询一个区间内所有元素的和

    PS: **两者时间复杂度均为：O（logN）**【PS:** **相比于直接数组单点修改的O (1)** **和区间求和的O(n),** **或者前缀和的单点修改的O (n)** **和区间求和的O(1)****，当两种功能都需要实现的时候树状数组综合较好】**

* 区别于线段树

  * 树状数组能解决的线段树都可以解决，但树状数组系数比线段树少很多。
  * 树状数组比传统数组读写快，但复杂区间问题不容易解决。

* 树状数组的构建 --- 比正常数组多一个下标0,因此第一个0不用。

  利用“二进制”进行分段。树状结构大致如下：

  <img src="./img/树状数组实例图.png" alt="树状数组实例图" style="zoom:80%;" />

   例: 求前11项的和

     1） Step1：计算11转2进制，得到1011

     2）Step2：前11项的和转化为 (0000，1000],(1000,1010],(1010,1011]

     3）对上述三个区间求和，三个区间的由来：不断去掉最右边的1改为0

  <img src="./img/树状数组实例区间图.png" alt="树状数组实例区间图" style="zoom:80%;" />

  ​    **Ps:** 前8项的和可以参照上图，(0000，0100],(0100,0110],(0110,0111]

  * Lowbit(x) 的定义：二进制最低位置的1和其后的0一起作为lowbit（x），那么我们用Ci 维护区间 (Ai-lowbit(Ai),Ai]，这样显然查询前n项和时需要合并的区间数是少于log2N的。

  ​       PS: 关于上述Ci 维护区间 (Ai-lowbit(Ai),Ai] 的定义，不要受到最顶上二叉树图的影响

  * lowbit 计算：lowbit(x) = (x) & (-x)

    说明：如公式：计算机的有符号数一般以补码形式存储，-x相当于按位取反+1（原码=反码+1），因此如果x=1000,-x=0111+1=1000,前面完全取反。【不可能绕开最低位的1】---- 按位与，两个位置都是1，最后的结果才是1，因此可以直接计算lowbit

  * C0= (A0-lowbit(A0),A0] = (0,0]  ---- 0000-0000

  ​       PS:假如数组第一个0不用，计算方式还是 Ci 维护区间 (Ai-lowbit(Ai),Ai]

  * C1 =(A1-lowbit(A1),A1] = (0001-00001,0001] = (0,1] = A[1]

  * C2 =(A2-lowbit(A2),A2] = (0010-0010,0010] = (0,2] = A[1]+A[2]

  * C3 = (A3-lowbit(A3),A3] = (0011-0001,0011] = (2,3] = A[3]

  * C4 =(A4-lowbit(A4),A4] = (0100-0100,0100] = (0,4]=A[1]+A[2]+A[3]+A[4]

  * C5 = (0101-0001,0101] = (4,5] = A[5]

  * C6 = (0110-0010,0110] = (4,6] = A[5]+A[6]

  * C7 = (0111-0001,0111] = (6,7] = A[7]

  * C8 = (10000-10000,10000] = (0,8] = A[1]+…+A[8]

    C[i] = A[i-2^k+1]+A[i-2^k+2]+…+A[i] //k 为二进制最低位到最高位连续0的长度

* 树状数组的更新

  ---爬树过程：一路往上更新，直到树状数组容量值

  * 例子：以二进制数100110 为例

  ​       (100100,100110] 最小区间；（100000，1010000] （100000，110000] （000000，100000]； 为lowbit的较大范围区间，如下图：**左边为****lowbit计算方式**，**右边为每次加上lowbit后进位**, 这样更新区间不会超过log（maxN），能够以O（logN）进行查询的和修改的数据结构便完成了。

  <img src="./img/树状数组更新示例.png" alt="树状数组更新示例" style="zoom:50%;" />

## 前缀树Trie

* 定义：单词查找树、字典树（字典套字典递归）Hash Tree 变种，查询快、内存消耗小

* 优点：利用字符串公共前缀减少查询时间、最大限度减少无谓字符串比较，查询效率高于hash

* 典型应用：统计、排序和保存大量字符串（不限于字符串），经常被搜索引擎用于文本词频统计。

  PS: 其他应用--单词自动补全、拼写检查、最长前缀匹配、前缀预测单词、统一前缀的全部键值等

* 主要操作：插入、查找、删除

* **主要性质**

  * 根节点不包含字符，其他每个节点只包含一个字符
  * 从根节点到某个节点开始，路径上经过的字符连接起来为该节点对应字符串
  * 每个节点的所有子节点包含字符不相同（都含有26个可能的子节点表示26个字母）

* 前缀树例子:假设有b,abc,bcd,abcd,efg,hii 6个单词创建就得到下述前缀树

  <img src="./img/前缀树例子.png" alt="前缀树例子" style="zoom: 80%;" />

* 实现步骤

  * 字典树实质：字典套字典，并在结束位置加上一个字符表明该字符串已结束。

  * 更新字典时加上递归遍历字典。

    ```python
    class Trie:
        # 字典树：根节点不存值，每个根节点的子节点都是26个字符中的1个，字典套字典
        def __init__(self):
            self.tree = dict()
    
        # 字典套字典层层遍历
        def insert(self, word: str) -> None:
            tree = self.tree
            for s in word:
                if s not in tree:
                    tree.update({s: {}})
                tree = tree[s]
            # 字典单词结束位置记录：#
            tree.update({"#": True})
    
        def search(self, word: str) -> bool:
            tree = self.tree
            for s in word:
                if s not in tree:
                    return False
                tree = tree[s]
            return True if "#" in tree else False
    
        def startsWith(self, prefix: str) -> bool:
            tree = self.tree
            for s in prefix:
                if s not in tree:
                    return False
                tree = tree[s]
            return True
    ```

* 具体实现 ---leetcode 307

  * 建立BIT: BIT =[0]+原数组 # 2进制原因第一个下标不用
  * 建立lowbit函数：x &(-x)
  * 初始化BIT：BIT下标index 从1开始，计算 j = index+lowbit(index),若j在BIT 长度以内，BIT[j]+=BIT[i]
  * 自定义前缀和函数presum，通过lowbit对下标递减更新需要求和的区间
  * 区间求和 presum（right）-presum(left-1)
  * 更新某个位置的元素：sumRange（x,x)

  ```
  class BIT_tree:
      def __init__(self, nums):
          self.BIT = [0] + nums  # 构造bit树，bit树比原来数组多一个空间，第一个0下标不用
          # 跳过第一个0后使用lowbit函数来更新整个树状数组
          for i in range(1, len(self.BIT)):
              j = i + self.lowbit(i)
              if j < len(self.BIT):  # 加上lowbit之后放大的区间在范围内，则更新
                  self.BIT[j] += self.BIT[i]
  
      def lowbit(self, x):
          return x & (-x)
  
      # 自定义前缀和函数
      def preSum(self, index: int) -> int:
          i = index + 1  # index 为原来nums当中的下标，+1为bit中的位置
          preSum = 0  # 前缀和
          while i:
              preSum += self.BIT[i]
              i -= self.lowbit(i)
          return preSum
  
      # 区间求和
      def sumRnage(self, left: int, right: int) -> int:
          return self.preSum(right) - self.preSum(left - 1)  # right 对应的前缀和
  
      # 更新元素位置
      def update(self, index: int, val: int) -> None:
          preVal = self.sumRnage(index, index)  # 求BIT 当中原来的值
          diff = val - preVal  # 变更值
          pos = index + 1
          while pos < len(self.BIT):
              self.BIT[pos] += diff
              pos += self.lowbit(pos)
  ```

  PS: # 208/211 如何按照题意进行递归搜索

# 运行资源管理

## 内存释放&管理

参考[内容](https://blog.csdn.net/yigeng3663/article/details/90611744)

### 对象内存的使用

* 使用id函数返回对象的内存地址

  ```
  A = 1
  print(id(A))
  print(hex(id(A)))
  ```

* 用 **is** **关键字来判断两个引用是否相同**---相同数值的引用会引用到同一个空间

  ```
  A=1
  B=1
  print(A is B)
  ```

* getrefcount 查看某个引用对象的计数

  从基本原理上来说：当python的某个对象的引用次数降为0时，说明没有任何引用指向该对象，该对象就会成为垃圾回收的对象。

**Conclusion: python通过变量的计数来确定该变量申请的内存是否应该被回收。**

### 内存自动回收机制

​      由于手动del 和频繁的垃圾回收将大大降低python工作效率。故python会在特定条件下启动回收垃圾：**当python运行时，会记录其中分配对象（object allocation）和取消分配对象（object deallocation）次数，当两者差值高于某个阈值，垃圾回收机制启动。**

* 阈值查看方法：使用gc模块 的 get_threshold()查看该阈值：

```
import gc
print(gc.get_threshold()) # 返回值（700，10，10）
```

**700即为自动回收的阈值，两个10为分代回收的参数。**

* 分代回收：存活时间越久的对象，越不可能在后面的程序中变成垃圾。出于信任和效率，对于这些长期存活的对象，默认相信它们的用处，减少在内存回收过程中扫描他们的频率【是减少，不是为0】

* Python 将所有对象分为0，1，2三代，所有新建对象都是0代，当某一代对象经历过垃圾回收，依然存活，那么它就被归入下一代对象。垃圾回收启动时，一定会扫描所有的0代对象。如果0代经过一定次数垃圾回收，那么就启动对0代和1代的扫描清理。当1代也经历了一定次数的垃圾回收后，那么会启动对0，1，2，即对所有对象进行扫描。

### 删除元素后的内存释放

```python
import gc
del x_train, x_test  # 仅仅是del 不能真正释放内存
gc.collect()  # 执行这一步才是真正的释放内存
```

# 性能相关

## 多进程

### multiprocessing

多进程的python库，用于并发&进程间数据共享

* 构造方法：Process(target = xxx目标方法xx，args = xxx目标方法的参数xxxx)

* 实例方法：

--- is_alive() 返回进程是否正在运行

  --- join（timeout=xxx）设置每个进程被阻塞后等待的时间，单位：s

  ---Start（）； # 进程准备就绪，等待CPU调度。

  --- Run(); # start 调用run 方法。

  --- Terminate（）； 不管任务是否完成，立即停止工作进程。

* 数据共享--manager() 方法

* multiprocessing.Pool()  构建进程池，获取进程处理任务直到没有空闲进程后等待。

  ```
  import multiprocessing
  from multiprocessing import Pool
  
  
  def task2pool(current_round_tasks, update_round):
      # 向进程池中非阻塞添加及执行任务，通过进程池管理任务状态,最后一个逗号是必须的
      for i in range(max_process):
          async_result = pool.apply_async(func=fun, args=(
              par1, par2))
          # 为了检查进程状态
          result.append(async_result)
  
  
  if __name__ == "__main__":
      result = list()
      max_process = multiprocessing.cpu_count()  # 最大进程数
      pool = Pool()
      task2pool(max_process)
  ```

  

## 多线程



```
import threading

t = threading.Thread(target="函数",args=("param",))
t.join() # 阻塞线程直到完成
```

* setDaemon(True) 设置守护线程，star之前使用。若不设置为守护线程，程序将会被无限挂起。（当我们在程序运行中，执行一个主线程，如果主线程又创建一个子线程，主线程和子线程 就分兵两路，分别运行，那么当主线程完成想退出时，会检验子线程是否完成。如果子线程未完成，则主线程会等待子线程完成后再退出。但是有时候我们需要的是只要主线程完成了，不管子线程是否完成，都要和主线程一起退出，这时就可以 用setDaemon方法）



## 高并发相关参数

* semaphore 信号量：

  * 内置计数器：

  ​      1）每当调用acquire（）时，内置计数器-1；每当调用release() 的时候内置计数器+1；

  ​      2）计数器不能小于0，当计数器为0时，acquire() 将阻塞线程直到其他线程调用release()

* 锁

  * 全局解释器锁GIL:Python 中的线程是操作系统的原生线程，为了支持多线程机制，**一个基本要求就是要实现不同线程对共享资源访问的互斥**。因此GIL被提出：在一个线程拥有了解释器的访问权后，其他所有线程都必须等待它释放解释器的访问权，即使这些线程的下一条指令并不会互相影响。

    1） 优点：避免大量加锁解锁操作； 缺点：多处理器退化为单处理器（组合为1个处理器）；

    2） 影响：无论启多少个线程，有多少个CPU, python在执行一个进程的时候在同一个时刻，只能允许一个线程运行。因此，python无法利用多核CPU实现多线程。

    PS:**这种情况对计算密集型任务效果不如串行（无大量切换）,但是对IO密集型的任务效率有显著提升。**

  * 同步锁：**常用于实现对共享资源的同步访问，为每一个共享资源创建一个lock****对象，当需要访问该资源时，调用acquire****方法来获取锁对象（如果其他线程已经获得了该锁，则当前线程需要等待其被释放），待资源访问完后，再调用release** **访问释放锁**

  * 死锁：**两个或两个以上进程或线程再执行过程中，因争夺资源而造成相互等待的现象**。若无外力作用，他们都将无法推进下去，此时称系统处于死锁状态或系统产生了死锁，这些永远再互相等待的进程成为死锁进程。【Solution】Python中为了多次请求同一资源，可以设置重入锁RLock，其内部维护一个lock和一个counter变量，counter记录请求资源的次数，从而使得资源可以被多次请求，**直到所有acquire被release之后其他线程才能获得资源，用Rlock替换lock之后不会发生死锁**。

## queue 模块多进程数据交换

```
import queue

q = queue.Queue()
q.get(item) # 从队列中拿数据
q.put(item) # 向队列中放数据
q.join() & task_done() # 阻塞进程直到任务完成
q.qsize()  # 队列大小
q.empty() # 队列是否为空
q.full() # 队列是否为满
q.get_nowait() # 相当于q.get(False) 非阻塞
q.put_nowait(item="111") # 相当于q.put(False) 非阻塞
```

## asyncio/trio 异步模块

经过封装后的异步非阻塞python库

### 分布式进程

[参考](https://blog.csdn.net/lilong117194/article/details/76051843)

将process进程分布到多台机器上，在python 中仍然需要利用multiprocessing 模块。

Multiprocessing 模块不仅支持多进程，其中的managers 子模块还支持把多进程分到多台机器上。可以写一个服务进程作为调度，将任务分布到其他子进程中，依靠网络通信管理。

创建分布式进程需要分为6个步骤：

1）建立Queue队列，用来进行进程间的通信，服务进程创建任务队列task_queue,用来回传任务给任务进程通道；服务进程创建结果队列 result_queue作为任务进程完成后回复服务进程的通道。在分布式多进程环境下，必须通过由QueueManager获得的Queue接口来添加任务。

2）把第一步中建立的队列在网络上注册，暴露给其他进程，注册后获得网络队列，相当于本地队列的映像

3）建立第一个对象Queuemanager（Base manager）manager，绑定端口和验证口令。

4） 启动第三部中建立的实例，即启动管理manager，监管信息通道。

5） 通过管理实例的方法获得通过网络访问Queue对象，即再把网络队列实例化成可以使用的本地队列。

6）创建任务到“本地”队列，自动上传任务到网络队列中，分配给任务进程进行处理

在Thread 和 process 中，优先选择Process,因为process 更稳定，且能够分不到多台机器上，Thread 只能分不到同一台机器的多个CPU上。可以通过multiprocessing 的manager子模块将任务分布到多台子机器上，一个服务进程作为任务调度者，将任务分布到其他多个进程中，依靠网络通信。

PS：manager 模块封装较好，可以直接使用，编写分布式多进程程序。

## 协程

协程又称微线程，纤程，一种用户态的轻量级线程。[参考](https://www.cnblogs.com/yuanchenqi/articles/6755717.html)

协程拥有自己的寄存器上下文和栈。调度切换时，将寄存器上下文和栈保存到其他地方，在切换回来的时候，恢复先前保存的寄存器上下文和栈。因此：协程能够保留上一次调用时候的状态（即：所有局部状态的一个特定组合），每次过程重入时，就相当于进入上一次调用的状态（上一次离开时所处逻辑流的位置）

优点:1) 无需线程上下文切换的开销； 2）无需原子操作锁定及同步开销；3）方便切换控制流，简化编程模型。4）高并发+高扩展性+低成本： 一个CPU支持上万个协程都不是问题，很适合高并发处理。

缺点：1） 无法利用多核资源：协程的本质是个单线程，它不能同时将单个cpu的多核利用上，需要和进程配合才能用在多个CPU上，当然常见的绝大部分应用没有这个必要，除非是CPU密集型应用。

2） 进行阻塞操作（IO）时会阻塞掉整个程序。

## 遇到的问题记录

* 不同系统允许的最大并发不同：windows 512， linux 1024，导致loop能够发送的任务量不一致，可以通过修改变化

  PS1: ulimit -n 查看并发数 & 可以永久修改系统最大链接数（最大并发数）

  PS2: 在不永久修改最大链接、并发数的情况下的解决办法，采用sem 对selector 的数量进行限制， windows 限制在500，linux 限制在1000。一个进程的当中的Loop任务达到该数量级之后，进程开始等待，直到loop当中的任务数量级降低再继续执行。

* 异步进程卡顿：执行某一个异步非阻塞task 时，使用 asyncio.wait_for(future，timeout=) 当timeout 超时之后，该过程仅仅时取消请求，但wait_for 仍然可能在协程当中运行切返回。[参见](https://bugs.python.org/issue32751)

  1）python multiprocessing库下Process 进程是否可以设置超时

  2）process 经常卡顿可能是由于内存不足；

  3）进程启动时定时回收所有开启的子进程（使用work.kill(), 替代 kill -9）

  

# 常用库记录

## cpython--python的C拓展库

* 安装 ：pip3 install Cython / conda install -c anaconda cython

* 文件扩展后缀：.pyx

* 1、 同级目录下创建setup.py,该文件负责编译上述pyx 文件生成.c 和 .so 文件

  -- touch setup.py

* 编译

## collection

容器类—实现特定的目标容器，提供python标准内建容器dict，list，set和tuple的替代 ，具体参考[内容](https://docs.python.org/zh-cn/3/library/collections.html#defaultdict-objects)

| [`namedtuple()`](https://docs.python.org/zh-cn/3/library/collections.html#collections.namedtuple) | 创建命名元组子类的工厂函数                                   |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [`deque`](https://docs.python.org/zh-cn/3/library/collections.html#collections.deque) | 类似列表(list)的容器，实现了在两端快速添加(append)和弹出(pop) |
| [`ChainMap`](https://docs.python.org/zh-cn/3/library/collections.html#collections.ChainMap) | 类似字典(dict)的容器类，将多个映射集合到一个视图里面         |
| [`Counter`](https://docs.python.org/zh-cn/3/library/collections.html#collections.Counter) | dict subclass for counting [hashable](https://docs.python.org/zh-cn/3/glossary.html#term-hashable) objects |
| [`OrderedDict`](https://docs.python.org/zh-cn/3/library/collections.html#collections.OrderedDict) | 字典的子类，保存了他们被添加的顺序                           |
| [`defaultdict`](https://docs.python.org/zh-cn/3/library/collections.html#collections.defaultdict) | 字典的子类，提供了一个工厂函数，为字典查询提供一个默认值，后续按照字典处理 |
| [`UserDict`](https://docs.python.org/zh-cn/3/library/collections.html#collections.UserDict) | 封装了字典对象，简化了字典子类化                             |
| [`UserList`](https://docs.python.org/zh-cn/3/library/collections.html#collections.UserList) | 封装了列表对象，简化了列表子类化                             |
| [`UserString`](https://docs.python.org/zh-cn/3/library/collections.html#collections.UserString) | 封装了字符串对象，简化了字符串子类化                         |

## copy 深浅拷贝

* copy.copy(list) or list.copy() # 浅拷贝，传的只是地址

* copy.deepcopy(list) # 深拷贝，全新的数组

**深拷贝：全新数组，浅拷贝：原来数组的地址**

## filter：对整个数据进行筛选

*  从list 当中去掉所有空字符串 data = list(filter(None,list))

## re 正则匹配库

* re.match(pattern,string) # 从第一个位置开始搜索
* re.search(pattern,string) # 搜索整个字符串返回第一个

## matplotlib -matlab画图库

* 修改横轴密度 Import matplotlib.ticker as ticker

## argparse -- 自带脚本启动参数解析库

python 用于解析命令行参数和选项的标准模块，用于代替已经过时的optparse模块，[参考](https://docs.python.org/3/library/argparse.html)

## request 

* 下载url对应的数据内容并转为str格式response = requests.request("GET", self.DNSBL_Spam).text

## networkx--画网格图

```
import network as nx
G = nx.graph() # 创建空的简单图
G = nx.DiGraph()
G = nx.MultiDiGraph() # 空的多图
G = nx.MultiDiGraph() # 创建空的有向图
```

## folium -- 可视化地图库

[示例代码](https://github.com/JingtaoWang1996/folium_journeyMap)

# 问题记录

* 报错：pkg_resources.DistributionNotFound: The ‘module‘ distribution

​       解决方案：python –m pip install module

* 报错：kafka 库使用报错---python操作[kafka](https://so.csdn.net/so/search?q=kafka&spm=1001.2101.3001.7020)报错：return '<SimpleProducer batch=%s>' % self.async

​       原因：因为py3.7里面async已经变成了关键字。所以导致了不兼容。[参见](https://blog.csdn.net/ChailangCompany/article/details/121777925)

​       解决方案：使用最新的kafka版本，但是pyPI上的kafka还没有被替换成最新的，可以使用下面的方法升级kafka python：pip install kafka-python

* 报错：time 库计时问题

​       解决方案：使用 int(time.time())做计时器进行定时让任务时，当小数位精度过高的时候，int 会出现多加1位的情况，导致计时的时候（time.time()-start）会变成-1

* 报错：os 库执行linux 命令，os.system(command)无返回值

​      解决方案：改用os.popen(command）

* 内存和缓存问题

  * 问题现象：DNS项目当中在本地15上断网的时候跑docker服务用docker stats 和 free –h 观察发现内存会逐步上升，缓存也会上升

  * 初步排查后发现：内存docker长时间运行后会产生docker stats 内存占满的情况

  * 缓存：linux清除缓存命令进行排查后发现pagecache过大。

  * 解决方案：内存问题通过下面内容[启发，根据业务需求的每30](https://blog.csdn.net/sinat_41667855/article/details/117217678）启发，根据业务需求的每30)分钟重读数据，对docker资源进行释放后申请，确认内存未再增加。 https://blog.csdn.net/sinat_41667855/article/details/117217678；缓存：通过排查注释掉发现kafka部分代码和全局变量移入主函数中进行释放，缓存未上升。**[****缓存不必关注，主要是看内存占用]**

  ​       TIPS: 在有性能要求，长期跑的服务上尽可能减少全局变量申请的内存资源，改为写在主函数中

# 其他

## 后端

### Django

* 本身是一个由python写的开放源码的web框架，基于MVC模型（model模型、视图view、controller控制器的涉及模式）

* Model：代码应有的功能，负责业务对象与数据库的映射。

​       View：图形界面，将html展示给用户。

​       Controller：转发请求，对请求进行处理。

* MTV 模型（T：template, 展示html页面）

#### 安装

* pip install django

* windows 系统环境变量Path 下增加：

​      *C:\Python33\Lib\site-packages\django;C:\Python33\Scripts

​      *如果上述参数找不到，则直接path中新增：python路径\Lib\site-packages\django

* 检查是否安装成功：import django   &  django.get_version()

  ps: 清华源下载Django：sudo pip3 install Django -i https://pypi.tuna.tsinghua.edu.cn/simple

### Flask

[参考]()

#### 安装

* pip install flask 

* Backend 工程 testFlask.py 是一个简单的demo
* 运行之后，浏览器登录 http://127.0.0.1:5000/ 就能看到hello方法的返回值

#### 使用

```python
@app.route("/hello/<name>") # <name> 动态传参，
def hello():
    return "flask app1"
```

除去默认字符串变量部分以外，url还可以使用以下转换器构建规则：

| string | （缺省值） 接受任何不包含斜杠的文本 |
| ------ | :---------------------------------- |
| int    | 接受正整数                          |
| float  | 接受正浮点数                        |
| path   | 类似 string ，但可以包含斜杠        |
| uuid   | 接受 UUID 字符串                    |

在上述例子中，url‘/hello’ 绑定到hello_world() 函数，访问http://127.0.0.1:5000/hello 可以查看hello接口具体返回值。

* Backend 工程 testFlask.py 是一个简单的demo
* 运行之后，浏览器登录 http://127.0.0.1:5000/ 就能看到hello方法的返回值
* flask静态文件：一般是css 和 JS。理想情况下，服务器已经配置好了提供静态文件的服务，但flask同样能完成配置。 


------