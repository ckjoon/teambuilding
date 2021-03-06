import xlrd
import db_util

class RosterProcessor:
    def __init__(self, file, class_id=None):
        self.file = file
        self.students = []
        self.class_id = class_id

    def process(self):
        wb = xlrd.open_workbook(file_contents=self.file)
        ws = wb.sheet_by_index(0)

        for i in range(0, ws.nrows):
            r = ws.row_values(i, start_colx=0, end_colx=ws.ncols)
            if r[-1] == 'Student':
                name = r[0].split(', ')
                self.students.append( (r[1], r[2], name[1], name[0]) )
        #print(self.students)

    def export_to_db(self):
        db_util.enroll_from_roster(self.students, self.class_id)

f = open('./../rosters/csxxxx_roster.xls', 'rb+') 
instance = RosterProcessor(f.read(), 1) #replace 1 with class ID used in the DB
instance.process()
instance.export_to_db()

def process_roster(fname):
    with open(fname, 'rb+'):
        instance = RosterProcessor(f.read())
        instance.process()
        instance.export_to_db() 
