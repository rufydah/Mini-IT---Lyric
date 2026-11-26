from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
app.secret_key = 'lyric_secret_key' #needed for admin login sess
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = "password123"
@app.route('/')
def home():
    return render_template ('user_login.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'Invalid admin credentials. Try again.'
            return render_template('admin_login.html', error=error)
    
    return render_template('admin_login.html', error=error)

@app.route('/admin/dashboard')
def admin_dashboard ():
    if not session.get ('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template ('admin_dashboard.html')
@app.route ('/admin/logout')
def admin_logout ():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))
@app.route('/binder')
def fan_binder():
    return render_template('fan_binder.html')
if __name__=='__main__':
    app.run(debug=True)


@app.route('admin/forgot', methods=['GET','POST'])
def admin_forgot():
    global ADMIN_PASSWORD
    message = None
    error = None
    if request.method == 'POST':
        username = request.form['username']
        recovery_code = request.form ['recovery_code']
        new_password = request.form ['new_password']
        if username == ADMIN_USERNAME and recovery_code == 'LYRIC2026':
            ADMIN_PASSWORD = new_password
            message = 'Password updated successfully! You may now log in.'
        else:
            error = 'Invalid username or recovery code.'
    return render_template('admin_forgot.html', message=message, error=error)