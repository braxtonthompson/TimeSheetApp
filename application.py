import script
import time
from config import config
from flask import Flask, render_template, url_for, redirect, session
from forms import TimesheetForm

application = app = Flask(__name__)

app.config['SECRET_KEY'] = config['secret_key']

@app.route("/", methods=['GET', 'POST'])
def timesheet():
        form = TimesheetForm()
        if form.validate_on_submit():
                start_time = time.time()
                try:
                        script.Auto(form.username.data, form.password.data, form.hours_worked.data)
                except Exception as e:
                        print(e)
                finished_time = (time.time() - start_time)
                print(f'Finished in {round(finished_time, 2)} seconds.')
                return redirect(url_for('timesheetcomplete'))
        return render_template('timesheet.html', form=form)

@app.route("/complete")
def timesheetcomplete():
        return render_template('timesheet_complete.html', status = session['status'])

if __name__ == '__main__':
        # application.run(host='0.0.0.0')
        application.run(debug=True)
