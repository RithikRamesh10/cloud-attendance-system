from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3, os
from datetime import date
app=Flask(__name__); app.secret_key=os.environ.get("SECRET_KEY","demo-key")
DB=os.environ.get("DATABASE_PATH","attendance.db")
def db():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
def init():
 with db() as c:
  c.execute("""CREATE TABLE IF NOT EXISTS attendance(id INTEGER PRIMARY KEY AUTOINCREMENT,student_name TEXT NOT NULL,student_id TEXT NOT NULL,attendance_date TEXT NOT NULL,status TEXT NOT NULL CHECK(status IN ('Present','Absent')),UNIQUE(student_id,attendance_date))""")
@app.route("/",methods=["GET","POST"])
def index():
 if request.method=="POST":
  name=request.form.get("student_name","").strip(); sid=request.form.get("student_id","").strip()
  day=request.form.get("attendance_date") or date.today().isoformat(); status=request.form.get("status","Present")
  if not name or not sid or status not in ("Present","Absent"):
   flash("Please enter valid attendance details."); return redirect(url_for("index"))
  try:
   with db() as c: c.execute("INSERT INTO attendance(student_name,student_id,attendance_date,status) VALUES(?,?,?,?)",(name,sid,day,status))
   flash("Attendance saved successfully.")
  except sqlite3.IntegrityError: flash("This student already has an entry for that date.")
  return redirect(url_for("index"))
 with db() as c: rows=c.execute("SELECT * FROM attendance ORDER BY attendance_date DESC,student_name").fetchall()
 return render_template("index.html",records=rows,today=date.today().isoformat())
@app.route("/report")
def report():
 day=request.args.get("date") or date.today().isoformat()
 with db() as c:
  rows=c.execute("SELECT * FROM attendance WHERE attendance_date=? ORDER BY student_name",(day,)).fetchall()
  sums=c.execute("SELECT status,COUNT(*) n FROM attendance WHERE attendance_date=? GROUP BY status",(day,)).fetchall()
 counts={r["status"]:r["n"] for r in sums}
 return render_template("report.html",records=rows,day=day,present=counts.get("Present",0),absent=counts.get("Absent",0))
 @app.route("/delete_attendance/<int:record_id>", methods=["POST"])
def delete_attendance(record_id):
    day = request.form.get("day") or date.today().isoformat()

    with db() as c:
        c.execute(
            "DELETE FROM attendance WHERE id = ?",
            (record_id,)
        )

    flash("Attendance record deleted successfully.")
    return redirect(url_for("report", date=day))
@app.route("/health")
def health(): return {"status":"ok"},200
init()
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)))
