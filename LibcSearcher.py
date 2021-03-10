from pwnlib.elf import ELF
from pwnlib.rop import ROP
from pwn import *
import os


class LibcSearcher:

    _condition = {}
    _archsMap = {
        'amd64': 'amd64',
        'i386': 'i386',
        'aarch64': 'arm64',
        'powerpc64': 'ppc64el',
        'arm': 'armhf',
        'em_s390': 's390x',
    }
    _prefer = []
    useCache: bool
    dbPath: str
    decidedELF: ELF = None

    def __init__(self, useCache: bool = True, dbPath: str = None):
        self.useCache = useCache
        if dbPath == None:
            self.dbPath = os.path.join(os.path.realpath(
                os.path.dirname(__file__)), "db/")
        else:
            self.dbPath = dbPath
        self.cachePath = os.path.join(os.path.realpath(
            os.path.dirname(__file__)), ".cache")

    def condition(self, func: str, addr: int):
        self._condition[func] = addr
        return self

    def prefer(self, *name):
        for i in name:
            self._prefer.append(i)
        return self

    def __decideInList(self, versions, res):
        possibeVersion = []
        for files in versions:
            fpath = os.path.join(self.dbPath, files, 'symbols')
            if not os.path.exists(fpath):
                continue
            fd = open(fpath, "rb")
            data = fd.read().decode(errors='ignore').split("\n")
            if all([x in data for x in res]):
                possibeVersion.append(files)
            fd.close()
        length = len(possibeVersion)
        if length == 0:
            return None
        elif length == 1:
            return possibeVersion[0]
        else:
            print("Multi Results:")
            for i, f in enumerate(possibeVersion):
                print('[%2d] %s' % (i, f))
            while True:
                try:
                    i = int(input('Choice: '))
                    if i >= 0 and i < length:
                        break
                except ValueError:
                    pass
                print('Input error,try again.')
            return possibeVersion[i]

    def __decide(self):
        res = []
        for name, address in self._condition.items():
            res.append("%s %x" % (name, address & 0xfff))
        if self.useCache and os.path.exists(self.cachePath):
            with open(self.cachePath, 'r') as cFile:
                r = cFile.readlines()
            if len(r) > 1:
                version = r[0][:-1]
                r = r[1:]
                result = 0
                for i, con in enumerate(res):
                    result ^= i+1
                    for j, conCache in enumerate(r):
                        if conCache[:-1] == con:
                            result ^= j+1
                            continue
                if result == 0:
                    self.__setELF(version)
                    return
        if len(self._prefer) != 0:
            v = self.__decideInList(self._prefer, res)
            if v != None:
                self.__setELF(v)
                return
        versionList = [f for f in os.listdir(self.dbPath)
                       if context.arch not in self._archsMap or
                       f.endswith(self._archsMap[context.arch])
                       ]

        v = self.__decideInList(versionList, res)
        if v == None:
            raise LookupError(
                'No matched libc, please add more libc or try others')
        else:
            self.__setELF(v)

    def __setELF(self, version):
        elf = ELF(os.path.join(
            self.dbPath, version, 'libc.so.6'), False)
        self.decidedELF = elf
        base = 0
        for name, address in self._condition.items():
            if base == 0:
                base = address-elf.symbols[name]
            elif base != address-elf.symbols[name]:
                raise LookupError(
                    'No matched libc, please add more libc or try others')
        elf.address = base
        with open(self.cachePath, 'w') as cFile:
            cFile.write(version+'\n')
            for name, address in self._condition.items():
                cFile.write("%s %x\n" % (name, address & 0xfff))

    def elf(self) -> ELF:
        if self.decidedELF == None:
            self.__decide()
        return self.decidedELF

    def rop(self) -> ROP:
        return ROP(self.elf())
