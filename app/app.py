from flask import Flask, render_template, redirect, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import dbconfig
import threading
import os
import classes


app = Flask(__name__)
bcrypt = Bcrypt(app)

login_manager = LoginManager() # Allow our app and flask_login to work together to handle things when logging in
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader # User load callback - used to reload this objects from the user id stored in the session
def load_user(user_id):
    conn = dbconfig.dbConnection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM system_users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if(user):
        return User(user["id"],user["username"],user["password"])
    else:
        return None


app.config['SECRET_KEY'] = '4f8b92c10d3a7e5f6e8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f' 

# conn = mysql.connect()
# cursor = conn.cursor()
# cursor.execute("SELECT * FROM usuarios")
# dados = cursor.fetchall()
# cursor.close()
# conn.close()


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(),Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

    # def validate_username(self, ):
    #     # Verify if user already exits
    #     return 0
    
class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    email = StringField(validators=[InputRequired(),Length(min=10, max=50)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(),Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")





@app.route("/")
def home():
    return render_template("main.html")

@app.route("/homePage")
@login_required
def homePage():
    return render_template("homePage.html",username=current_user.username)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()

    if (form.validate_on_submit()):
        conn = dbconfig.dbConnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM system_users WHERE username = %s",(form.username.data,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if(user):
            if (bcrypt.check_password_hash(user["password"] , form.password.data,)):
                login_user(User(user["id"], user["username"], user["password"]))
                return redirect(url_for('homePage'))

    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route("/register", methods=['GET','POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # Create a hashed version of the password;

        try:
            conn = dbconfig.dbConnection()
            cursor = conn.cursor()

            cursor.execute("INSERT INTO system_users(username,email,password,role)VALUES(%s,%s,%s,%s)", (form.username.data, form.email.data, hashed_password, "admin"))
            conn.commit()
            cursor.close()
        except Exception as e:
            print(f"ERROR: {e}")

        return redirect(url_for('login'))


    return render_template("register.html", form=form)


@app.route("/monitoring", methods=['GET','POST'])
def monitoring():
    return render_template("monitoringPage.html")


# -------------- API -------------------------
@app.route("/api/<resource>")
def get_resource(resource):

    if resource == "homePageData":
        speedTestData = classes.SpeedTestData.getSpeedTestData()
        numberOfDevices = classes.Devices.getNumberOfDevices()
        packetStats = classes.IOCounters.getPacketStats()
        devicesData = classes.Devices.getDevicesData()
        alerts = classes.Alerts.getAlerts()

        data = [speedTestData,numberOfDevices,packetStats, devicesData, alerts]

    elif resource == "monitoringPageData":
       
        speedTestData = classes.SpeedTestData.getSpeedTestData()
        devicesData = classes.Devices.getDevicesData()
        IOCountersData = classes.IOCounters.getIOCountersData()
        deviceSpecifications = classes.DiviceEspecifications.getSpecifications()
        cpuTimes = classes.CPUTimes.getCPUTimes()
        cpuStats = classes.CPUTStats.getCPUStats()
        cpuFrequency = classes.CPUFrequency.getCPUFrequency()
        avgSysLoad = classes.AverageSystemLoad.getAVGSystemLoad()
        virtualMemory = classes.VirtualMemory.getVirtualMemory()
        swapMemory = classes.SwapMemory.getSWAPMemory()
        diskUsage = classes.DiskUsage.getDiskUsage()
        otherMetrics = classes.OtherMetrics.getOtherMetrics()
        defaultGateway = classes.DefaultGateway.getDefaultGatewayData()
        defaultGatewayInterfaces = classes.DefaultGateway.getDefaultGatewayInterfacesData(5)

        data = [speedTestData, devicesData, IOCountersData, deviceSpecifications, cpuTimes, cpuStats, cpuFrequency, avgSysLoad, virtualMemory, swapMemory, diskUsage, otherMetrics, defaultGateway, defaultGatewayInterfaces]

    else:
        return {"error": "Recurso não existe"}, 404


    return jsonify(data)
 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True)
