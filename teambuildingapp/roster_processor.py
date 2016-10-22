import xlrd
from io import BytesIO

class RosterProcessor:
    def __init__(self, file):
        self.file = file
        self.students = []
    def process(self):
        wb = xlrd.open_workbook(file_contents=self.file)
        ws = wb.sheet_by_index(0)

        for i in range(0, ws.nrows):
            r = ws.row_values(i, start_colx=0, end_colx=ws.ncols)
            if r[-1] == 'Student':
                name = r[0].split(', ')
                self.students.append( (r[1], r[2], name[1], name[0]) )

        print(self.students)

f = open('./../rosters/CS3600_roster.xls', 'rb+')
instance = RosterProcessor(f.read())
instance.process()