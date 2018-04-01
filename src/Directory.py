import os, os.path, pathlib, shutil
from Stat import Stat

class Directory(Stat):
    def __init__(self, path):
        super().__init__(path)
        if not os.path.isdir(str(path)): raise ValueError('引数pathには存在するディレクトリを指定してください。path={}'.format(path))
    #def __getattr__(self, name):
    #    for n in dir(super()):
    #        if n == name: super().
    @classmethod
    def IsExist(cls, path): return os.path.isdir(path)
    @classmethod
    def Create(cls, path): os.makedirs(path, exist_ok=True)
    @classmethod
    def Copy(cls, src, dst): return shutil.copytree(src, dst)
    @classmethod
    def Delete(cls, path): shutil.rmtree(path)
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
    def UnArchive(cls, src, dst=None): shutil.unpack_archive(src, dst)
