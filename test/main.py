import sys, os, os.path, pathlib
print(pathlib.Path(__file__).parent.parent / 'src')
sys.path.append(str(pathlib.Path(__file__).parent.parent / 'src'))
from Directory import Directory

if __name__ == '__main__':
    target_root = '/tmp/work/__TEST__'
    try:
        assert(True == Directory.IsExist('/'))
        assert(False == Directory.IsExist('/NotExistDir'))
        target = os.path.join(target_root, 'SUB1', 'SUB11', 'SUB111')
        print(target)
        assert('/tmp/work/__TEST__/SUB1/SUB11/SUB111' == target)
        assert(False ==  Directory.IsExist(target_root))
        Directory.Create(target)
        assert(True ==  Directory.IsExist(target))
        assert(True ==  os.path.isdir(target))
        assert(True ==  os.path.exists(target))
        
        Directory.Delete(target)
        assert(False ==  Directory.IsExist(target))
        assert(True ==  Directory.IsExist('/tmp/work/__TEST__/SUB1/SUB11'))
        
        target2 = os.path.join(target_root, '__TEST2__')
        assert(False ==  Directory.IsExist(target2))
        Directory.Copy(target_root, target2)
        assert(True ==  Directory.IsExist(target2))
        assert(True == Directory.IsExist(os.path.join(target2, 'SUB1', 'SUB11')))
        a = Directory.Archive(target_root, target_root + '.zip')
        print(a)
        print(target_root + '.zip')
        assert(a == target_root + '.zip')
        assert(os.path.isfile(a))
    finally:
        Directory.Delete(target_root)
        os.remove(target_root + '.zip')
