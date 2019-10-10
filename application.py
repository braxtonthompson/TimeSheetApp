import script
import credentials
from flask import Flask, render_template, url_for, redirect
from forms import TimesheetForm

application = app = Flask(__name__)

app.config['SECRET_KEY'] = credentials.SECRET_KEY

@app.route("/", methods=['GET', 'POST'])
@app.route("/timesheet", methods=['GET', 'POST'])
def timesheet():
        form = TimesheetForm()
        if form.validate_on_submit():
                script.Automation(form.username.data, form.password.data, form.hours_worked.data)
                return redirect(url_for('timesheetcomplete'))
        return render_template('timesheet.html', form=form)

@app.route("/timesheet/complete")
def timesheetcomplete():
        return render_template('timesheet_complete.html')

if __name__ == '__main__':
        application.run(host='0.0.0.0')