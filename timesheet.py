import script
import credentials
from flask import Flask, render_template, url_for, redirect
from forms import TimesheetForm

app = Flask(__name__)

app.config['SECRET_KEY'] = credentials.SECRET_KEY

@app.route("/", methods=['GET', 'POST'])
def timesheet():
        form = TimesheetForm()
        if form.validate_on_submit():
                credentials.NAME = form.name.data
                credentials.USERNAME = form.username.data
                credentials.PASSWORD = form.password.data
                credentials.HOURS = form.hours_worked.data
                script.segments()
                script.selenium_script()
                return redirect(url_for('timesheetcomplete'))
        return render_template('timesheet.html', title='Trouble Crew Time Sheets', form=form)

@app.route("/timesheet/completion")
def timesheetcomplete():
        return render_template('timesheetinprogress.html', title='Trouble Crew Time Sheets')

if __name__ == '__main__':
        app.run(debug=True)