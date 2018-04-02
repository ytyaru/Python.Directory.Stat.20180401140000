import os, os.path, pathlib, shutil
from Stat import Stat

class Directory(Stat):
    def __init__(self, path):
        if not os.path.isabs(path): raise ValueError('引数pathは絶対パスにしてください。path=\'{}\''.format(path))
        super().__init__(path)

    def mk(self, path=None):
        if path is not None and os.path.isabs(path) and self.Path not in path:
            raise ValueError('引数pathは未指定か次のパスの相対パス、または次のパス配下を指定してください。{}'.format(self.Path))
        elif path is None: self.Create(self.Path)
        elif os.path.isabs(path): self.Create(path)
        else: self.Create(os.path.join(self.Path, path))
        self.__make_first(self.Path)
    def __make_first(self, path):
        if self.Stat is None: self.Path = path
    def rm(self, path=None):
        if path is not None and os.path.isabs(path) and self.Path not in path: raise ValueError('引数pathは未指定か次のパスの相対パス、または次のパス配下を指定してください。{}'.format(self.Path))
        elif path is None: self.Delete(self.Path)
        elif os.path.isabs(path): self.Delete(path)
        else: self.Delete(os.path.join(self.Path, path))
    def cp(self, dst): return self.Copy(self.Path, dst)
    def mv(self, dst):
        self.Path = self.Move(self.Path, dst)
        return self.Path
    def pack(self, dst): return self.Archive(self.Path, dst)
    def unpack(self, src, dst=None): self.UnArchive(src, dst)

    @classmethod
    def IsExist(cls, path): return os.path.isdir(path)
    @classmethod
    def Create(cls, path): os.makedirs(path, exist_ok=True)
    @classmethod
    def Copy(cls, src, dst): return shutil.copytree(src, dst)
    @classmethod
    def Delete(cls, path):
        if cls.IsExist(path): shutil.rmtree(path)
    @classmethod
    def Move(cls, src, dst): return shutil.move(src, dst)
    @classmethod
    def Archive(cls, src, dst):
        ext = os.path.splitext(dst)[1][1:]
        archive_exts = [f[0] for f in shutil.get_archive_formats()]
        if ext not in archive_exts : raise Exception('拡張子\'{}\'は不正値です。アーカイブ拡張子は次のいずれかのみ可能です。{}'.format(ext, archive_exts))
        head, tail = os.path.split(src)
        base_name = os.path.join(os.path.dirname(dst), tail)
        root_dir = os.path.join(os.path.dirname(dst), head)
        base_dir = tail
        return shutil.make_archive(base_name, ext, root_dir=root_dir, base_dir=base_dir)
    @classmethod
    def UnArchive(cls, src, dst=None):
        d = dst
        if dst is None: d = os.path.dirname(src)
        shutil.unpack_archive(src, d)
