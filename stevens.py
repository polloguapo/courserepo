""" Testing Flask installation """

from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/instructor_summary')
def instructor_summary():
    DB_FILE = "./810_startup.db"
    db = sqlite3.connect(DB_FILE)
    data = db.execute("select i.cwid, i.name, i.dept, g.course, count(*) \
            as NumStudents from instructors i join grades g \
            on i.cwid=g.instructorcwid group by course");

    return render_template(
            'instructor_summary.html',
            title='Stevens Repository',
            table_title="Instructor Summary",
            instructors=data)

app.run(debug=True)

