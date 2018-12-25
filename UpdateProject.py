# -*- coding:utf-8 -*-

import sys
import os,shutil


class Package(object):
    def __init__(self, upgrade_package, project):
        self.upgrade_package = upgrade_package
        self.project = project
        self.upgrade_files = []
        self.need_upgrade_files = []

    def get_updata_file(self, dir):
        files = os.listdir(dir)
        for _file in files:
            file_path = os.path.join(dir, _file)
            if os.path.isdir(file_path):
                self.get_updata_file(file_path)
            else:
                self.upgrade_files.append((file_path, _file))

    def get_projeck_file(self):
        for _file in self.upgrade_files:
            self.need_upgrade_files.append((_file[0].replace(self.upgrade_package, self.project), _file[1]))


    def upgrade(self):
        file_len=len(self.upgrade_files)
        for i in xrange(0,file_len):
            shutil.move(self.upgrade_files[i][0],self.need_upgrade_files[i][0])



def app():
    try:
        upgrade_package,project=sys.argv[1:]
    except Exception as e:
        print ("******err:缺少必要参数******")
        return
    package = Package(upgrade_package, project)
    package.get_updata_file(package.upgrade_package)
    package.get_projeck_file()
    l = len(package.upgrade_files)
    if l==0:
        print ("err:*****升级包暂无文件*****")
        return
    print ("********以下文件将会被升级覆盖*******")
    for i in xrange(0, l):
        print ("{0}-------->{1}".format(package.upgrade_files[i][0], package.need_upgrade_files[i][0]))
    confirm=raw_input("请确认y/n: ")
    if confirm=="n":
        return
    package.upgrade()
    print ("---------升级完成---------")

if __name__ == '__main__':
    app()
