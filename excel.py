# !/usr/bin/env python
# coding=utf-8

# ==============================================================================
#
#       Filename:  demo.py
#    Description:  excel operat
#        Created:  2018.10.17
#         Author:  刘帅
#
# ==============================================================================
from xlwt import *
import xlrd


# 写入excel模块
class Excel(object):
    def __init__(self, write_file=None, read_file=None, encoding="utf-8", table_name="data"):
        self.write_file = write_file
        self.read_file = read_file
        self.encoding = encoding
        self.table_name = table_name
        self.file_p = None
        self.read_file_p = None
        if self.write_file:
            self.workbook = Workbook(self.encoding)
            self.file_p = self.workbook.add_sheet(self.table_name)
        if self.read_file:
            # 待开发 本次只需要写 所以读我就不写了 啦啦啦啦啦...
            self.read_file_p = xlrd.open_workbook(filename=self.read_file)

    # 写入文件
    def write(self, field_list, data_list):
        if not self.write_file:
            raise ValueError("Write_file can not be none")
        if not data_list:
            raise ValueError("Data can not be none")
        field_len = 0
        p = 0
        # 写入字段
        if field_list:
            if not isinstance(field_list, tuple):
                print field_list
                raise TypeError("Must be an iterable object")
            field_len = len(field_list)
            for i in range(field_len):
                self.file_p.write(0, i, field_list[i])

        # 写入内容
        # 可以根据传来的数据指针类型定制不同的写入策略
        # 这里只写了针对元祖列表
        if isinstance(data_list, list):
            rows = len(data_list)
            cols = len(data_list[0])
            if field_len != cols:
                raise RuntimeError("The header does not match the number of content columns")
            for r in range(p, rows):
                if (not isinstance(data_list[r], list)) and (not isinstance(data_list[r], tuple)):
                    raise TypeError("Must be an iterable object")
                for c in range(cols):
                    # 写入excel
                    # 参数对应 行, 列, 值
                    self.file_p.write(r + 1, c, data_list[r][c])

    # 2019.12.12 新增读取
    def read_all(self, start_colx=0, end_colx=None):
        # 针对数据量少
        if not self.read_file_p:
            raise ValueError("read_file can not be none")
        sheet = self.read_file_p.sheet_by_index(0)
        n = sheet.nrows
        data_group = [sheet.row_values(rowx=i, start_colx=start_colx, end_colx=end_colx) for i in xrange(1, n)]
        return data_group

    def read_row(self, row, start_colx=0, end_colx=None):
        if not self.read_file_p:
            raise ValueError("read_file can not be none")
        sheet = self.read_file_p.sheet_by_index(0)
        return sheet.row_values(rowx=row, start_colx=start_colx, end_colx=end_colx)

    def save(self):
        self.workbook.save(self.write_file)


# 测试用例

def main():
    fields = ("姓名", "性别", "年龄", "公司")
    file_name = "C:\\Users\\dell\\Desktop\\file.xlsx"
    data = [("小刘", "男", 22, "xxxxx"),
            ("小刘", "男", 22, "xxxxx"),
            ("小刘", "男", 22, "xxxxx"),
            ("小刘", "男", 22, "xxxxx"),
            ("小刘", "男", 22, "xxxxx"),
            ("小刘", "男", 22, "xxxxx")]
    excel = Excel(write_file=file_name, table_name="log")
    excel.write(fields, data)
    excel.save()

    read_excel = Excel(read_file=file_name)
    print read_excel.read_row(2)


if __name__ == "__main__":
    main()
