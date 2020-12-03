import os
import mysql.connector
from .models import Member
from .app import app, db, encrypt_pwd
from flask import flash, abort, redirect, url_for, request, render_template

# app = Flask(__name__)


mydb = mysql.connector.connect(
    host="localhost", user="greg", password="password", database="cs425test", auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()


@app.route('/', methods = ['POST', 'GET'])
def index():
   if request.method == "POST":
      req = request.form

      username = req.get("nm")
      usertype = req.get("userType")

      print(username)
      print(usertype)

      if usertype == "registered":
         mycursor.execute("SELECT * FROM members")
         myresult = mycursor.fetchall()
         found = False

         for x in myresult:
            if x[2] == int(username):
               found = True   
         
         if found == True:
            return redirect(url_for('success', id=username, typex=usertype))
         else:
            flash('User not found!')
      if usertype == "staff":
         mycursor.execute("SELECT * FROM staff")
         myresult = mycursor.fetchall()
         found = False

         for x in myresult:
            if x[0] == int(username):
               found = True   
         
         if found == True:
            return redirect(url_for('success', id=username, typex=usertype))
         else:
            flash('User not found!')
      if usertype == "admin":
         mycursor.execute("SELECT * FROM administrator")
         myresult = mycursor.fetchall()
         found = False

         for x in myresult:
            if x[0] == int(username):
               found = True   
         
         if found == True:
            return redirect(url_for('admin', id=username))
         else:
            flash('User not found!') 
      else:
         mycursor.execute("SELECT * FROM non_member")
         myresult = mycursor.fetchall()
         found = False

         for x in myresult:
            if x[0] == int(username):
               found = True   
         
         if found == True:
            return redirect(url_for('success', id=username, typex=usertype))
         else:
            flash('User not found!')
         
   
   return render_template("login.html")

@app.route('/admin/<id>', methods = ['POST', 'GET'])
def admin(id):
   user_login, guest_login = generate_login_report()
   return render_template("admin.html", user_login=user_login, guest_login=guest_login)

@app.route('/delete/', methods = ['POST', 'GET'])
def delete():
   if request.method == "POST":
      req = request.form
      rid = req.get("rid")
      sql = "SELECT * FROM reservation WHERE reservation_id =" + "'" + rid+"'"
      mycursor.execute(sql)
      myresult = mycursor.fetchall()
      if len(myresult) > 0:
         sql = "DELETE FROM `cs425test`.`reservation` `reservation` WHERE (`reservation`.`reservation_id` = " + rid +")"
         mycursor.execute(sql)
         mydb.commit()
         print(str(myresult[0][3]))
         print(str(myresult[0][4]))
         sql = "DELETE FROM `cs425test`.`calendar` `calendar` WHERE (`calendar`.`reservation_date` = '" + str(myresult[0][3]) + "') AND (`calendar`.`reservation_time` = '" + str(myresult[0][4]) + "')"
         mycursor.execute(sql)
         mydb.commit()
         print("DELETED FROM CALENDAR!")
   return render_template("delete.html")

@app.route('/registration', methods = ['POST', 'GET'])
def registration():
   return ""

@app.route('/success/<typex>/<id>', methods = ['POST', 'GET'])
def success(id, typex):
   query = "SELECT * FROM reservation WHERE member_id = " + str(id)
   mycursor.execute(query)
   myreservations = mycursor.fetchall()
   #Open spots
   mycursor.execute("SELECT `parking_spot`.`lot_no`,`parking_spot`.`spot_no`,`parking_spot`.`building_name` FROM `cs425test`.`parking_spot` `parking_spot` LEFT OUTER JOIN `cs425test`.`reservation` `reservation` ON `parking_spot`.`lot_no` = `reservation`.`lot_no` AND `parking_spot`.`spot_no` = `reservation`.`spot_no` AND `parking_spot`.`building_name` = `reservation`.`building_name` WHERE (`reservation`.`reservation_id` IS NULL) ORDER BY `parking_spot`.`building_name` ASC, `parking_spot`.`lot_no` ASC")
   openspots = mycursor.fetchall()
   #Building names
   mycursor.execute("SELECT DISTINCT building_name FROM parking_spot")
   buildings = mycursor.fetchall()
   if request.method == "POST":
      if typex == "registered":
         try:
            req = request.form
            rdate = req.get("date")
            rtime = req.get("time")
            rlot = req.get("lot")
            rspot = req.get("spot")
            rbuilding = req.get("building")
            sql = "INSERT INTO calendar (reservation_date, reservation_time) VALUES (%s, %s)"
            val = (rdate, rtime)
            mycursor.execute(sql, val)
            mydb.commit()
            print("Record inserted into Calander!")
            sql = "INSERT INTO reservation (reservation_id, member_id, non_member_id, reservation_date, reservation_time, building_name, spot_no, lot_no) VALUES (%s, %s,%s, %s,%s, %s,%s, %s)"
            val = (None, id, None, rdate, rtime,rbuilding, rspot, rlot)
            mycursor.execute(sql, val)
            mydb.commit()
            print("INSERTED RESERVATION!")
         except:
            flash('Error making reservation!')
      else:
         print("")
   return render_template("reservations.html", result=openspots, reservations=myreservations, availbuildings=buildings, uid=id, utype=typex)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("registration.html")

    if request.method == "POST":
        # get form data
        email = request.form["email"]
        carplate = request.form["carplate"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        password = request.form["psw"]
        password_repeat = request.form["psw-repeat"]

        if password != password_repeat:
            # TODO - use javascript in html
            abort(400, description="Password Confirmation Failed")

        password = encrypt_pwd(password)

        # check if user exist
        exists = Member.query.filter_by(email=email).first()

        if exists is not None:
            abort(404, description="This email has already registered")

        member = Member(
            carplate=carplate,
            lastname=lastname,
            firstname=firstname,
            email=email,
            password=password,
        )

        db.session.add(member)
        db.session.commit()
        return render_template("thank_you.html", reason="Registering!")

def generate_login_report():
   member_sql = """
   select distinct member_id, login_time, logout_time
   from login
   where member_id is not null
   order by login_time desc
   """

   user_login = mycursor.execute(member_sql)
   user_login = mycursor.fetchall()

   non_member_sql = """
   select distinct non_member_id, login_time, logout_time
   from login
   where non_member_id is not null
   order by login_time desc
   """

   guest_login = mycursor.execute(non_member_sql)
   guest_login = mycursor.fetchall()

if __name__ == '__main__':
#    app.secret_key = os.urandom(24)
   app.run(debug=True)
