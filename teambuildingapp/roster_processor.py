import xlrd
import db_util

class RosterProcessor:
    def __init__(self, file, class_id, instructor):
        self.file = file
        self.students = []
        self.instructor = instructor
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

# uncomment below for testing
#f = open('./../rosters/CS3600_roster.xls', 'rb+')
#instance = RosterProcessor(f.read(), 'CS3600_123id', 'professor0')
#instance.process()