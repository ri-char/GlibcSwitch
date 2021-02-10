# GlibcSwitch

CTF Pwn中堆利用的题往往对glibc的版本要求比较严格，因此这个脚本可以通过patch ELF文件，便捷的切换ELF文件所使用的glibc的版本，同时支持多种架构。

## 安装与使用

1. 安装patchelf: 参见[NixOS/patchelf](https://github.com/NixOS/patchelf)
2. `git clone https://github.com/ri-char/GlibcSwitch.git`
3. 下载glibc`./download /path/to/db all i386,amd64` 参数为储存目录
4. `./glibcswitch /path/to/db version target`

## download

`download`命令用于联网下载glibc库：

1. `/path/to/db`: glibc库的储存目录
1. `Download Type` :选择是否下载调试信息。`all`表示带调试信息，`bin`表示不带调试信息下载，`dbg`表示仅下载调试信息(前提是已经下过不带调试信息的库)
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

## 便捷使用

可以在bashrc中取别名，使用时就可以只需要两个参数

```
alias glibcswitch=/xxx/glibcswitch /path/to/db
```