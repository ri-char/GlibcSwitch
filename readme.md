# GlibcSwitch

CTF Pwn中堆利用的题往往对glibc的版本要求比较严格，因此这个脚本可以通过patch ELF文件，便捷的切换ELF文件所使用的glibc的版本。

## 安装与使用

1. 安装patchelf: 参见[NixOS/patchelf](https://github.com/NixOS/patchelf)
2. `git clone https://github.com/ri-char/GlibcSwitch.git`
3. 下载glibc`./download /path/to/db` 参数为储存目录
4. `./glibcswitch /path/to/db version target`

glibcswitch参数说明:
**/path/to/db:** glibc库的储存目录
**version:** 版本号。可以是完整目录名称，也可以是版本，如`2.27`。`system`表示系统默认版本。
**target:** 目标elf文件

## 便捷使用

可以在bashrc中取别名，使用时就可以只需要两个参数

```
alias glibcswitch=/xxx/glibcswitch /path/to/db
```