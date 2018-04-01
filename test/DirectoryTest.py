import sys, os, os.path, pathlib
print(pathlib.Path(__file__).parent.parent / 'src')
sys.path.append(str(pathlib.Path(__file__).parent.parent / 'src'))
from Directory import Directory
import unittest
import time, datetime

class DirectoryTest(unittest.TestCase):
    # ----------------------------
    # クラスメソッド
    # ----------------------------
    def test_IsExist(self):
        self.assertTrue(Directory.IsExist(os.getcwd()))
        self.assertTrue(not Directory.IsExist('/NotExistDir'))

    def test_Create_Delete(self):
        target = '/tmp/work/__TEST__'
        self.assertTrue(not Directory.IsExist(target))
        Directory.Create(target)
        self.assertTrue(Directory.IsExist(target))
        Directory.Delete(target)
        self.assertTrue(not Directory.IsExist(target))
        target = '/tmp/work/__TEST__/A/B/C'
        self.assertTrue(not Directory.IsExist(target))
        Directory.Create(target)
        self.assertTrue(Directory.IsExist(target))
        Directory.Delete(target)
        self.assertTrue(not Directory.IsExist(target))
        target = '/tmp/work/__TEST__'
        Directory.Delete(target)

    def test_Copy_single(self):
        target = '/tmp/work/__TEST__'
        self.assertTrue(not Directory.IsExist(target))
        Directory.Create(target)
        Directory.Copy(target, '/tmp/work/__TEST_2__')
        self.assertTrue(Directory.IsExist('/tmp/work/__TEST_2__'))
        Directory.Delete(target)
        Directory.Delete('/tmp/work/__TEST_2__')

    def test_Copy_tree(self):
        target = '/tmp/work/__TEST__'
        self.assertTrue(not Directory.IsExist(target))
        Directory.Create(target)
        Directory.Create(os.path.join(target, 'A'))
        pathlib.Path(os.path.join(target, 'A/a.txt')).touch()
        self.assertTrue(not Directory.IsExist('/tmp/work/__TEST_2__'))
        Directory.Copy(target, '/tmp/work/__TEST_2__')
        self.assertTrue(Directory.IsExist('/tmp/work/__TEST_2__'))
        self.assertTrue(os.path.isfile('/tmp/work/__TEST_2__/A/a.txt'))
        Directory.Delete(target)
        Directory.Delete('/tmp/work/__TEST_2__')
    
    def test_Move_single(self):
        target = '/tmp/work/__TEST__'
        self.assertTrue(not Directory.IsExist(target))
        self.assertTrue(not Directory.IsExist('/tmp/work/__TEST_2__'))
        Directory.Create(target)
        Directory.Move(target, '/tmp/work/__TEST_2__')
        self.assertTrue(not Directory.IsExist(target))
        self.assertTrue(Directory.IsExist('/tmp/work/__TEST_2__'))
        Directory.Delete('/tmp/work/__TEST_2__')

    def test_Move_tree(self):
        target = '/tmp/work/__TEST__'
        self.assertTrue(not Directory.IsExist(target))
        self.assertTrue(not Directory.IsExist('/tmp/work/__TEST_2__'))
        Directory.Create(target)
        Directory.Create(os.path.join(target, 'A'))
        pathlib.Path(os.path.join(target, 'A/a.txt')).touch()
        
        Directory.Move(target, '/tmp/work/__TEST_2__')
        self.assertTrue(not Directory.IsExist(target))
        self.assertTrue(Directory.IsExist('/tmp/work/__TEST_2__'))
        self.assertTrue(Directory.IsExist('/tmp/work/__TEST_2__/A'))
        self.assertTrue(os.path.isfile('/tmp/work/__TEST_2__/A/a.txt'))
        Directory.Delete('/tmp/work/__TEST_2__')

    def test_Archive(self):
         self.__make_archive()
         os.remove('/tmp/work/__TEST__' + '.zip')

    def __make_archive(self):
        target = '/tmp/work/__TEST__'
        self.assertTrue(not Directory.IsExist(target))
        Directory.Create(target)
        Directory.Create(os.path.join(target, 'A'))
        pathlib.Path(os.path.join(target, 'A/a.txt')).touch()
        
        Directory.Archive(target, target + '.zip')
        self.assertTrue(os.path.isfile(target + '.zip'))
        Directory.Delete(target)

    def test_UnArchive(self):
        self.__make_archive()
        self.assertTrue(not Directory.IsExist('/tmp/work/__TEST__'))
        Directory.UnArchive('/tmp/work/__TEST__.zip')
        self.assertTrue(Directory.IsExist('/tmp/work/__TEST__'))
        self.assertTrue(Directory.IsExist('/tmp/work/__TEST__/A'))
        self.assertTrue(os.path.isfile('/tmp/work/__TEST__/A/a.txt'))
        Directory.Delete('/tmp/work/__TEST__')
        os.remove('/tmp/work/__TEST__.zip')
    
    # ----------------------------
    # Stat
    # ----------------------------
    def __MakeDummy(self, path, size):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if os.path.isfile(path): os.remove(path) # メタデータ初期化
        with open(path, 'wb') as f:
            f.write(b'\0'*size)
    # ----------------------------
    # クラスメソッド
    # ----------------------------
    def test_GetSize(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        self.assertTrue(hasattr(Directory, 'GetSize'))
        print('Dir Size is {}'.format(Directory.GetSize(target_root)))
        self.assertEqual(1024, Directory.GetSize(target_root))

        path_b = os.path.join(target_root, 'B')
        Directory.Create(path_b)
        self.__MakeDummy(os.path.join(path_b, 'b.dummy'), 1024)
        self.assertEqual(2048, Directory.GetSize(target_root))

        path_c = os.path.join(target_root, 'C')
        Directory.Create(path_c)
        self.__MakeDummy(os.path.join(path_c, 'c.dummy'), 1024)
        self.assertEqual(3072, Directory.GetSize(target_root))

        path_bb = os.path.join(target_root, 'B/BB')
        Directory.Create(path_bb)
        self.__MakeDummy(os.path.join(path_bb, 'bb.dummy'), 1024)
        self.assertEqual(4096, Directory.GetSize(target_root))

        Directory.Delete(target_root)
    
    def test_DiskUsage(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        self.assertTrue(hasattr(Directory, 'DiskUsage'))
        res = Directory.DiskUsage(target_dummy)
        self.assertTrue(hasattr(res, 'total'))
        self.assertTrue(hasattr(res, 'used'))
        self.assertTrue(hasattr(res, 'free'))
        print(Directory.DiskUsage(target_dummy))
        Directory.Delete(target_root)

    def test_Mode_Get_Set_Name(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        mode = Directory.GetMode(target_dummy)
        print(mode)
        print(oct(mode))
        Directory.SetMode(target_dummy, 0o755)
        self.assertEqual(0o100755, Directory.GetMode(target_dummy))
        self.assertEqual('-rwxr-xr-x', Directory.GetModeName(target_dummy))
        Directory.SetMode(target_dummy, '-rwxrwxrwx')
        self.assertEqual(0o100777, Directory.GetMode(target_dummy))
        Directory.SetMode(target_dummy, 0o644)
        self.assertEqual(0o100644, Directory.GetMode(target_dummy))
        self.assertEqual('-rw-r--r--', Directory.GetModeName(target_dummy))
        Directory.Delete(target_root)
    
    def test_SetModeFromName_Error(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        mode_name = 'Invalid-Text'
        with self.assertRaises(ValueError) as e:
            Directory.SetMode(target_dummy, mode_name )
        mode_names = [
            '---',
            '--x',
            '-w-',
            '-wx',
            'r--',
            'r-x',
            'rw-',
            'rwx'
        ]
        self.assertEqual('引数mode_nameが不正値です。\'{}\'。\'-rwxrwxrwx\'の書式で入力してください。owner, group, other, の順に次のパターンのいずれかを指定します。pattern={}。r,w,xはそれぞれ、読込、書込、実行の権限です。-は権限なしを意味します。'.format(mode_name, mode_names), e.exception.args[0])
        Directory.Delete(target_root)

    def test_Modified_Get_Set(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        self.assertTrue(tuple == type(Directory.GetModified(target_dummy)))
        self.assertTrue(2 == len(Directory.GetModified(target_dummy)))
        self.assertTrue(float == type(Directory.GetModified(target_dummy)[0]))
        self.assertTrue(datetime.datetime == type(Directory.GetModified(target_dummy)[1]))
        #print(type(Directory.GetModified(target_dummy)[0]))
        #print(type(Directory.GetModified(target_dummy)[1]))
        dt1 = datetime.datetime.strptime('1999/12/31 23:59:59', '%Y/%m/%d %H:%M:%S')
        dt2 = datetime.datetime.strptime('2345/01/02 12:34:56', '%Y/%m/%d %H:%M:%S')
        epoch, dt = Directory.GetModified(target_dummy)
        self.assertTrue(dt1 != dt)
        self.assertTrue(dt2 != dt)
        
        Directory.SetModified(target_dummy, dt1)
        self.assertTrue(int(time.mktime(dt1.timetuple())) == Directory.GetModified(target_dummy)[0])
        self.assertTrue(dt1 == Directory.GetModified(target_dummy)[1])
        self.assertTrue(dt1 != Directory.GetChangedMeta(target_dummy)[1])
        self.assertTrue(dt1 != Directory.GetAccessed(target_dummy)[1])
        Directory.Delete(target_root)

    def test_Accessed_Get_Set(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        self.assertTrue(tuple == type(Directory.GetAccessed(target_dummy)))
        self.assertTrue(2 == len(Directory.GetAccessed(target_dummy)))
        self.assertTrue(float == type(Directory.GetAccessed(target_dummy)[0]))
        self.assertTrue(datetime.datetime == type(Directory.GetAccessed(target_dummy)[1]))
        dt1 = datetime.datetime.strptime('1999/12/31 23:59:59', '%Y/%m/%d %H:%M:%S')
        dt2 = datetime.datetime.strptime('2345/01/02 12:34:56', '%Y/%m/%d %H:%M:%S')
        epoch, dt = Directory.GetAccessed(target_dummy)
        self.assertTrue(dt1 != dt)
        self.assertTrue(dt2 != dt)
        
        Directory.SetAccessed(target_dummy, dt1)
        self.assertTrue(int(time.mktime(dt1.timetuple())) == Directory.GetAccessed(target_dummy)[0])
        self.assertTrue(dt1 == Directory.GetAccessed(target_dummy)[1])
        self.assertTrue(dt1 != Directory.GetModified(target_dummy)[1])
        self.assertTrue(dt1 != Directory.GetChangedMeta(target_dummy)[1])
        Directory.Delete(target_root)

    def test_GetChangedMeta(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        self.assertTrue(hasattr(Directory, 'GetChangedMeta'))
        self.assertTrue(hasattr(Directory, 'GetCreated'))
        print(Directory.GetChangedMeta(target_dummy))
        print(Directory.GetCreated(target_dummy))
        Directory.Delete(target_root)

    def test_Ids(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        self.assertTrue(hasattr(Directory, 'OwnUserId'))
        self.assertTrue(hasattr(Directory, 'OwnGroupId'))
        self.assertTrue(hasattr(Directory, 'HardLinkNum'))
        self.assertTrue(hasattr(Directory, 'INode'))
        self.assertTrue(hasattr(Directory, 'DeviceId'))
        print(Directory.GetOwnUserId(target_dummy))
        print(Directory.GetOwnGroupId(target_dummy))
        print(Directory.GetHardLinkNum(target_dummy))
        print(Directory.GetINode(target_dummy))
        print(Directory.GetDeviceId(target_dummy))
        Directory.Delete(target_root)

    # ----------------------------
    # インスタンスメソッド
    # ----------------------------
    def test_Stat(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        s = Directory(target_root)
        self.assertEqual(Directory, type(s))
        self.assertEqual(os.stat_result, type(s.Stat))
        Directory.Delete(target_root)

    def test_Path(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        s = Directory(target_root)
        self.assertEqual('/tmp/work/__TEST__', s.Path)
        Directory.Delete(target_root)

    def test_Size(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        #s = Directory(target_root)
        s = Directory(target_root)
        self.assertEqual(1024, s.Size)

        path_b = os.path.join(target_root, 'B')
        Directory.Create(path_b)
        self.__MakeDummy(os.path.join(path_b, 'b.dummy'), 1024)
        self.assertEqual(2048, s.Size)

        path_c = os.path.join(target_root, 'C')
        Directory.Create(path_c)
        self.__MakeDummy(os.path.join(path_c, 'c.dummy'), 1024)
        self.assertEqual(3072, s.Size)

        path_bb = os.path.join(target_root, 'B/BB')
        Directory.Create(path_bb)
        self.__MakeDummy(os.path.join(path_bb, 'bb.dummy'), 1024)
        self.assertEqual(4096, s.Size)

        Directory.Delete(target_root)

    def test_Mode(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        s = Directory(target_root)
        s.Mode = 0o777
        self.assertEqual(0o40777, s.Mode)
        self.assertEqual('drwxrwxrwx', s.ModeName)
        s.Mode = 0o644
        self.assertEqual(0o40644, s.Mode)
        self.assertEqual('drw-r--r--', s.ModeName)
        s.Mode = '-rwxrwxrwx'
        self.assertEqual(0o40777, s.Mode)
        self.assertEqual('drwxrwxrwx', s.ModeName)
        Directory.Delete(target_root)

    def test_Modified(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        s = Directory(target_root)
        self.assertTrue(tuple == type(s.Modified))
        self.assertTrue(2 == len(s.Modified))
        self.assertTrue(float == type(s.Modified[0]))
        self.assertTrue(datetime.datetime == type(s.Modified[1]))
        dt1 = datetime.datetime.strptime('1999/12/31 23:59:59', '%Y/%m/%d %H:%M:%S')
        dt2 = datetime.datetime.strptime('2345/01/02 12:34:56', '%Y/%m/%d %H:%M:%S')
        epoch, dt = s.Modified
        self.assertTrue(dt1 != dt)
        self.assertTrue(dt2 != dt)
        
        s.Modified = dt1
        self.assertTrue(int(time.mktime(dt1.timetuple())) == s.Modified[0])
        self.assertTrue(dt1 == s.Modified[1])
        self.assertTrue(dt1 != s.Accessed[1])
        self.assertTrue(dt1 != s.Created[1])
        self.assertTrue(dt1 != s.ChangedMeta[1])
        Directory.Delete(target_root)

    def test_Accessed(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        s = Directory(target_root)
        self.assertTrue(tuple == type(s.Accessed))
        self.assertTrue(2 == len(s.Accessed))
        self.assertTrue(float == type(s.Accessed[0]))
        self.assertTrue(datetime.datetime == type(s.Accessed[1]))
        dt1 = datetime.datetime.strptime('1999/12/31 23:59:59', '%Y/%m/%d %H:%M:%S')
        dt2 = datetime.datetime.strptime('2345/01/02 12:34:56', '%Y/%m/%d %H:%M:%S')
        epoch, dt = s.Accessed
        self.assertTrue(dt1 != dt)
        self.assertTrue(dt2 != dt)
        
        s.Accessed = dt1
        self.assertTrue(int(time.mktime(dt1.timetuple())) == s.Accessed[0])
        self.assertTrue(dt1 == s.Accessed[1])
        self.assertTrue(dt1 != s.Modified[1])
        self.assertTrue(dt1 != s.Created[1])
        self.assertTrue(dt1 != s.ChangedMeta[1])
        Directory.Delete(target_root)

    def test_ChangedMeta(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        s = Directory(target_root)
        self.assertTrue(hasattr(s, 'ChangedMeta'))
        self.assertTrue(hasattr(s, 'Created'))
        print(s.ChangedMeta)
        print(s.Created)
        Directory.Delete(target_root)

    def test_Ids_Property(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        s = Directory(target_root)
        self.assertTrue(hasattr(s, 'OwnUserId'))
        self.assertTrue(hasattr(s, 'OwnGroupId'))
        self.assertTrue(hasattr(s, 'HardLinkNum'))
        self.assertTrue(hasattr(s, 'INode'))
        self.assertTrue(hasattr(s, 'DeviceId'))
        print(s.OwnUserId)
        print(s.OwnGroupId)
        print(s.HardLinkNum)
        print(s.INode)
        print(s.DeviceId)
        Directory.Delete(target_root)


if __name__ == '__main__':
    unittest.main()
