""" Testing Flask installation """

from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/instructor_summary')
def instructor_summary():
        """ Create summary table for web page """
        DB_FILE = "./stevens.db"
        try:
                db = sqlite3.connect(DB_FILE)
        except sqlite3.OperationalError:
                return f"Error: Unable to open database at {DB_FILE}"
        else:
                query = """select i.cwid, i.name, i.dept, g.course, count(*) as NumStudents
                        from instructors i join grades g on i.cwid=g.instructorcwid
                        group by cwid, course"""
        
                data = [{'cwid': cwid, 'name': name, 'dept': dept, 'course': course, 'NumStudents': NumStudents}
                        for cwid, name, dept, course, NumStudents in db.execute(query)]
                
                db.close()

                return render_template('instructor_summary.html', \
                                        title='Stevens Repository', \
                                        table_title='Instructor Summary', \
                                        instructors=data)

app.run(debug=True)

