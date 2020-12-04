import os
import mysql.connector
from models import Member
from app import app, db, encrypt_pwd
from flask import flash, abort, redirect, url_for, request, render_template
import sys
# app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost", user="greg", password="password", database="cs425test", auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()

def checkforRegistration(date, time, building, spot, lot):
   query = "SELECT * FROM `cs425test`.`reservation` `reservation` WHERE (`reservation`.`reservation_date` = '" + str(date) + "'	 ) AND (`reservation`.`reservation_time` = '" + str(time) + "') AND (`reservation`.`spot_no` = '" + str(spot) + "') AND (`reservation`.`lot_no` = '" + str(lot) + "') AND (`reservation`.`building_name` = '" + str(building) + "')"
   mycursor.execute(query)
   myresult = mycursor.fetchall()
   if len(myresult) > 0:
      return True
   else:
      return False

def createRegistration(rid, mid, nid, rdate,rtime,rbuilding,rspot,rlot):
   if checkforRegistration(rdate, rtime, building, rspot, rlot) == False:
      sql = "INSERT INTO reservation (reservation_id, member_id, non_member_id, reservation_date, reservation_time, building_name, spot_no, lot_no) VALUES (%s, %s,%s, %s,%s, %s,%s, %s)"
      val = (rid, mid, nid, rdate,rtime,rbuilding,rspot,rlot)
      mycursor.execute(sql, val)
      mydb.commit()

def getFee(building_name):
   query = "SELECT DISTINCT `building`.`fee` FROM `cs425test`.`building` `building` WHERE (`building`.`building_name` = '" + str(building_name) + "')"
   mycursor.execute(query)
   myresult = mycursor.fetchall()
   return int(myresult[0][0])

def deleteOldReservations():
   sql = "DELETE FROM `cs425test`.`reservation` `reservation` WHERE (`reservation`.`reservation_date` < CURDATE())"
   mycursor.execute(sql)
   mydb.commit()

def buildMonthlyReport(building_name, member):
   building = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0}
   fee = getFee(building_name)
   for x in range(1,13):
      if member == False:
         query = "SELECT ALL `building`.`building_name`,`building`.`fee` FROM `cs425test`.`building` `building` RIGHT OUTER JOIN `cs425test`.`reservation` `reservation` ON `building`.`building_name` = `reservation`.`building_name` WHERE (MONTH(`reservation`.`reservation_date`) = '" + str(x) + "') AND (`reservation`.`building_name` = '" + building_name + "') AND (`reservation`.`member_id` IS NULL)"
         mycursor.execute(query)
         myresult = mycursor.fetchall()
         building[x] = len(myresult) * fee
      else:
         query = "SELECT ALL `building`.`building_name`,`building`.`fee` FROM `cs425test`.`building` `building` RIGHT OUTER JOIN `cs425test`.`reservation` `reservation` ON `building`.`building_name` = `reservation`.`building_name` WHERE (MONTH(`reservation`.`reservation_date`) = '" + str(x) + "') AND (`reservation`.`building_name` = '" + building_name + "') AND (`reservation`.`non_member_id` IS NULL)"
         mycursor.execute(query)
         myresult = mycursor.fetchall()
         building[x] = len(myresult) * fee

   return building
@app.route('/', methods = ['POST', 'GET'])
def index():
   deleteOldReservations()
   if request.method == "POST":
      req = request.form

      username = req.get("nm")
      password = req.get("pass")
      usertype = req.get("userType")

      print(username)
      print(usertype)

      if usertype == "registered":
         mycursor.execute("SELECT * FROM members")
         myresult = mycursor.fetchall()
         found = False
         id=0

         for x in myresult:
            if x[5] == username and x[6] == password:
               found = True 
               id=x[2]  
         
         if found == True:
            return redirect(url_for('success', id=id, typex=usertype))
         else:
            flash('User not found!')
      if usertype == "staff":
         mycursor.execute("SELECT * FROM staff")
         myresult = mycursor.fetchall()
         found = False
         uid = 1

         for x in myresult:
            if x[2] == username and x[3] == password:
               found = True   
               uid = x[0]
         if found == True:
            return redirect(url_for('staff', id=uid))
         else:
            flash('User not found!')
      if usertype == "admin":
         mycursor.execute("SELECT * FROM administrator")
         myresult = mycursor.fetchall()
         found = False
         uid = 1
         for x in myresult:
            if x[3] == username and x[2] == password:
               found = True 
               uid = x[0]  
         
         if found == True:
            return redirect(url_for('admin', id=uid))
         else:
            flash('User not found!') 
      if usertype == "unregistered":
         mycursor.execute("SELECT * FROM non_member")
         myresult = mycursor.fetchall()
         found = False
         
         for x in myresult:
            if len(username) != 0:
               if x[0] == int(username):
                  found = True   
         
         if found == True:
            return redirect(url_for('nonmember_check', id=int(username)))
         else:
            return redirect(url_for('nonmember'))
         
   
   return render_template("login.html")

@app.route('/admin/<id>', methods = ['POST', 'GET'])
def admin(id):
   deleteOldReservations()
   query = "SELECT `members`.* FROM `cs425test`.`members` `members`"
   mycursor.execute(query)
   users = mycursor.fetchall()
   
   if request.method == "POST":
      # get form data
      email = request.form["uemail"]
      carplate = request.form["ulicense"]
      name = request.form["uname"]
      password = request.form["upass"]
      uid = request.form["uid"]

      mycursor.execute ("""
         UPDATE members
         SET car_plate_no=%s, full_name=%s, email=%s, password=%s
         WHERE member_id=%s
      """, (carplate, name, email, password, uid))
      return render_template("admin.html", id=id, abuildings={}, days={},)

   print(users)
   query = "SELECT * FROM `cs425test`.`parking_spot` `parking_spot`"
   mycursor.execute(query)
   myresult = mycursor.fetchall()
   totalspots = len(myresult) 
   sunday = totalspots
   monday = totalspots
   tuesday = totalspots
   wednesday = totalspots
   thursday = totalspots
   friday = totalspots
   saturday = totalspots
   query = "SELECT ALL `parking_spot`.`building_name`,`parking_spot`.`lot_no`,`parking_spot`.`spot_no`, DAYOFWEEK(`reservation`.`reservation_date`) FROM `cs425test`.`parking_spot` `parking_spot` RIGHT OUTER JOIN `cs425test`.`reservation` `reservation` ON `parking_spot`.`building_name` = `reservation`.`building_name` AND `parking_spot`.`lot_no` = `reservation`.`lot_no` AND `parking_spot`.`spot_no` = `reservation`.`spot_no` UNION SELECT ALL `parking_spot`.`building_name`,`parking_spot`.`lot_no`, `parking_spot`.`spot_no`, DAYOFWEEK(`reservation`.`reservation_date`) FROM `cs425test`.`parking_spot` `parking_spot` LEFT OUTER JOIN `cs425test`.`reservation` `reservation` ON `parking_spot`.`building_name` = `reservation`.`building_name` AND `parking_spot`.`lot_no` = `reservation`.`lot_no` AND `parking_spot`.`spot_no` = `reservation`.`spot_no`"
   mycursor.execute(query)
   myresult = mycursor.fetchall()

   mycursor.execute("SELECT DISTINCT building_name FROM parking_spot")
   buildings = mycursor.fetchall()

   result = {}

   for x in buildings:
      name = str(x[0])
      result[name] = {'r':{}, 'u':{}}
      result[name]['r'] = buildMonthlyReport(str(x[0]), True)
      result[name]['u'] = buildMonthlyReport(str(x[0]), False)
      print(result)

   for x in myresult:
      if x[3] == 1:
         sunday = sunday - 1
      if x[3] == 2:
         monday = monday - 1
      if x[3] == 3:
         tuesday = tuesday - 1
      if x[3] == 4:
         wednesday = wednesday - 1
      if x[3] == 5:
         thursday = thursday - 1
      if x[3] == 6:
         friday = friday - 1
      if x[3] == 7:
         saturday = saturday - 1
   
   
   user_login, guest_login = generate_login_report()
   return render_template("admin.html", user_login=user_login, abuildings=result, ausers=users,guest_login=guest_login, days=[sunday, monday,tuesday, wednesday, thursday, friday, saturday], uid=id)

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
         """ sql = "DELETE FROM `cs425test`.`calendar` `calendar` WHERE (`calendar`.`reservation_date` = '" + str(myresult[0][3]) + "') AND (`calendar`.`reservation_time` = '" + str(myresult[0][4]) + "')"
         mycursor.execute(sql)
         mydb.commit() """
         print("DELETED FROM CALENDAR!")
   return render_template("delete.html")

@app.route('/staff/<id>', methods = ['POST', 'GET'])
def staff(id):
   deleteOldReservations()
   query = "SELECT `members`.* FROM `cs425test`.`members` `members`"
   mycursor.execute(query)
   users = mycursor.fetchall()
   #Open spots
   mycursor.execute("SELECT `parking_spot`.`lot_no`,`parking_spot`.`spot_no`,`parking_spot`.`building_name` FROM `cs425test`.`parking_spot` `parking_spot` LEFT OUTER JOIN `cs425test`.`reservation` `reservation` ON `parking_spot`.`lot_no` = `reservation`.`lot_no` AND `parking_spot`.`spot_no` = `reservation`.`spot_no` AND `parking_spot`.`building_name` = `reservation`.`building_name` WHERE (`reservation`.`reservation_id` IS NULL) ORDER BY `parking_spot`.`building_name` ASC, `parking_spot`.`lot_no` ASC")
   openspots = mycursor.fetchall()
   #Building names
   mycursor.execute("SELECT DISTINCT building_name FROM parking_spot")
   buildings = mycursor.fetchall()

   if request.method == "POST":
      if request.form['submit_button'] == 'Update user':
         # get form data
         email = request.form["uemail"]
         carplate = request.form["ulicense"]
         name = request.form["uname"]
         password = request.form["upass"]
         uid = request.form["uid"]

         mycursor.execute ("""
            UPDATE members
            SET car_plate_no=%s, full_name=%s, email=%s, password=%s
            WHERE member_id=%s
         """, (carplate, name, email, password, uid))
         return render_template("staff.html", id=id, users=users,reservations=openspots, availbuildings=buildings)
      if request.form['submit_button'] == 'Make reservation':
         rbuilding = request.form["building"]
         rdate = request.form["date"]
         rtime = request.form["time"]
         rspot = request.form["spot"]
         rlot = request.form["lot"]
         rid = request.form["uid"]
         createRegistration(None, rid, None, rdate, rtime, rbuilding, rspot, rlot)
   return render_template("staff.html", id=id, users=users,reservations=openspots, availbuildings=buildings)

@app.route('/nonmember', methods=['POST', 'GET'])
def nonmember():
   #Open spots
   mycursor.execute("SELECT `parking_spot`.`lot_no`,`parking_spot`.`spot_no`,`parking_spot`.`building_name` FROM `cs425test`.`parking_spot` `parking_spot` LEFT OUTER JOIN `cs425test`.`reservation` `reservation` ON `parking_spot`.`lot_no` = `reservation`.`lot_no` AND `parking_spot`.`spot_no` = `reservation`.`spot_no` AND `parking_spot`.`building_name` = `reservation`.`building_name` WHERE (`reservation`.`reservation_id` IS NULL) ORDER BY `parking_spot`.`building_name` ASC, `parking_spot`.`lot_no` ASC")
   openspots = mycursor.fetchall()
   #Building names
   mycursor.execute("SELECT DISTINCT building_name FROM parking_spot")
   buildings = mycursor.fetchall()
   #return render_template("thank_you.html", reason="Registering!")
   if request.method == "POST":
         try:
            req = request.form
            rdate = req.get("date")
            name = req.get("name")
            rtime = req.get("time")
            rlot = req.get("lot")
            rspot = req.get("spot")
            rbuilding = req.get("building")
            if checkforRegistration(rdate, rtime, rbuilding, rspot, rlot) == False:
               mycursor.execute("SELECT * FROM non_member")
               myresult = mycursor.fetchall()
               id = len(myresult) + 1

               sql = "INSERT INTO non_member (non_member_id, full_name) VALUES (%s, %s)"
               val = (id, name)
               mycursor.execute(sql, val)
               mydb.commit()

               """ sql = "INSERT INTO calendar (reservation_date, reservation_time) VALUES (%s, %s)"
               val = (rdate, rtime)
               mycursor.execute(sql, val)
               mydb.commit()
               print("Record inserted into Calander!") """
            
               sql = "INSERT INTO reservation (reservation_id, member_id, non_member_id, reservation_date, reservation_time, building_name, spot_no, lot_no) VALUES (%s, %s,%s, %s,%s, %s,%s, %s)"
               val = (None, None, id, rdate, rtime,rbuilding, rspot, rlot)
               mycursor.execute(sql, val)
               mydb.commit()
               print("INSERTED RESERVATION!")
               return render_template("thank_you.html", reason="Registering! Your id is: " + str(id) + " use this to log in with no password.")
         except:
            flash(sys.exc_info()[0])
   else:
      print("")
   return render_template("nonmember.html", result=openspots, availbuildings=buildings)

@app.route('/nonmember_check/<id>', methods=['POST', 'GET'])
def nonmember_check(id):
   deleteOldReservations()
   query = "SELECT * FROM reservation WHERE non_member_id = " + str(id)
   mycursor.execute(query)
   myreservations = mycursor.fetchall()
   #Building names
   mycursor.execute("SELECT DISTINCT building_name FROM parking_spot")
   buildings = mycursor.fetchall()
   return render_template("nonmember_check.html", result=myreservations, availbuildings=buildings)

@app.route('/success/<typex>/<id>', methods = ['POST', 'GET'])
def success(id, typex):
   deleteOldReservations()
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
            if checkforRegistration(rdate, rtime, rbuilding, rspot, rlot) == False:
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
   deleteOldReservations()
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

      password_plain = password
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

      sql = "INSERT INTO members (car_plate_no, temp_plate_no, member_id, full_name, fee_paid, email, password) VALUES (%s,%s,%s,%s,%s,%s,%s)"
      val = (carplate, None, None, firstname + " " + lastname, 0, email,password_plain)
      mycursor.execute(sql, val)

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
   return user_login, guest_login

if __name__ == '__main__':
#    app.secret_key = os.urandom(24)
   app.run(debug=True)
