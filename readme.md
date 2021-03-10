# GlibcSwitch

CTF Pwn中堆利用的题往往对glibc的版本要求比较严格，因此这个脚本可以通过patch ELF文件，支持多种架构,同时还包含一个高效好用的LibcSearch。

## 安装与使用

1. 安装patchelf: 参见[NixOS/patchelf](https://github.com/NixOS/patchelf)
1. `git clone https://github.com/ri-char/GlibcSwitch.git`
1. 下载glibc`./download /path/to/db all i386,amd64`
1. 安装LibcSearcher至python库`sudo python setup.py develop`

使用：`./glibcswitch /path/to/db version target`

## download

`download`命令用于联网下载glibc库：

1. `/path/to/db`: glibc库的储存目录
1. `Download Type` :选择功能。`all`表示带调试信息，`bin`表示不带调试信息下载，`dbg`表示仅下载调试信息(前提是已经下过不带调试信息的库)，`sym`表示重新生成搜索用的符号文件。
1. `Architectures`:选择需要下载的架构，多个架构用`,`隔开。支持的架构有
   
    - amd64
    
    - i386
    
    - arm64
    
    - armhf
    
    - ppc64el
    
    - s390x
    

注：调试信息可以用于gdb调试，如`pwngdb`的`heap`、`bins`等功能。


## glibcswitch

`glibcswitch`命令用于`patch`ELF文件，`patch`后可以无需环境变量直接运行或用`qemu-user`运行。

1. `/path/to/db`: glibc库的储存目录

1. `version`: 版本号。可以是完整目录名称，也可以是版本号或目录前缀，如`2.27`。`system`表示系统默认版本。

1. `target`: 目标elf文件

```
glibcswitch ./db 2.31 ./pwn
Avalibable Version:
[0] 2.31-0ubuntu9.1_amd64
[1] 2.31-0ubuntu9.2_amd64
[2] 2.31-0ubuntu9_amd64
Please choose one: 0
```

可以在bashrc中取别名，使用时就可以只需要两个参数

```
alias glibcswitch=/xxx/glibcswitch /path/to/db
```

## LibcSearcher

可以方便的搜索出特定版本的glibc库，返回pwntools的ELF对象或ROP对象。

该工具会通过`context.arch`筛选出相同架构的libc，因此使用前请设置好`context.arch`。

缓存会记录上一次搜索的条件和结果，若启用缓存，此次搜索的条件与上次相同，会直接返回结果，不进行完整搜索。

```python
from pwn import *
from LibcSearch import *

context.arch='amd64'

glibcELF=LibcSearcher(useCache=True,dbPath='/path/to/db') # useCache参数选择是否使用缓存(默认为True)
                                                        # dbPath参数为db所在路径(默认为LibcSearch.py同文件夹下的db目录)
    .perfer('2.23-0ubuntu3_amd64','2.27-0ubuntu1.2_amd64') # 可选，设置优先搜索的版本，可有多个参数
    .condition("fgets", 0x7ff39014bd90) # 增加搜索条件，参数为泄露的函数名称和函数地址，可多次调用
    .elf() # 返回匹配到的ELF对象

```