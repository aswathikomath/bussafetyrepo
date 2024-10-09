import os

import pymysql
from flask import *
from werkzeug.utils import secure_filename

bus=Flask(__name__)
bus.secret_key="123"
con=pymysql.connect(host="localhost",user="root",password="root",port=3306,db="bus_safety",charset="utf8")
cmd=con.cursor()
@bus.route("/")
def login():
    return render_template("Login.html")


@bus.route("/logincheck", methods=['POST', 'GET'])
def logincheck():
    username = request.form["username"]
    passw = request.form["password"]

    # Use parameterized queries to prevent SQL injection
    cmd.execute("SELECT * FROM login WHERE username=%s AND password=%s", (username, passw))
    ans = cmd.fetchone()

    print(ans)

    if ans is None:
        return '''<script>alert("Invalid username or password"); window.location="/"</script>'''

    user_type = ans[3]  # Assuming the user type is in the fourth column of the result

    if user_type == 'admin':
        return render_template("Admin.html")
    # elif user_type == 'user':  # Check for regular user
    #     return render_template("user.html")
    # elif user_type == 'moderator':  # Check for moderator
    #     return render_template("moderator.html")
    else:
        return '''<script>alert("Unauthorized user type"); window.location="/"</script>'''


@bus.route("/addbus")
def addbus():
    return render_template("vechiclereg.html")

@bus.route("/addbusdetails", methods=['post'])
def addbusdetails():
    busname = request.form["bus_name"]
    busregnum = request.form["registration_number"]
    ownername = request.form["name_of_owner"]
    mobnu = request.form["monb"]
    useranme = request.form["useranme"]
    password = request.form["password"]

    from_location = request.form["from_location"]
    to_location = request.form["to_location"]
    departure = request.form["departure"]
    arrival = request.form["arrival"]
    trh = request.form["trh"]
    fileupload = request.files['fileField']
    fi = secure_filename(fileupload.filename)
    fileupload.save(os.path.join("static/images", fi))
    facility = request.form.getlist('facilities')
    fac = ','.join(facility)

    cmd.execute( "insert into login values(null,'" + useranme + "','"+password+"','pending')")
    id=cmd.lastrowid

    cmd.execute( "insert into bus_details values(null,'" + busname + "','" + busregnum + "','" + ownername + "','" + mobnu + "','" + from_location + "','" + to_location + "','" + departure + "','"+arrival+"','"+trh+"','"+fi+"','"+fac+"','"+str(id)+"')")
    con.commit()
    return '''<script>alert("inserted successfully");window.location="viewbus"</script>'''

@bus.route("/viewbus")
def viewbus():
    cmd.execute("select * from bus_details")
    result=cmd.fetchall()
    print(result)
    return render_template("vehicleview.html",values=result)

@bus.route("/deletebus")
def deletebus():
    id = request.args.get("id")
    print(id,"fghjkl")
    cmd.execute("DELETE FROM bus_details WHERE bus_id='" + str(id) + "'")
    con.commit()
    return '''<script>alert("bus deleted successfully");window.location="viewbus"</script>'''

@bus.route("/editbus")
def editbus():
    rid=request.args.get("id")
    session["busid"]=rid
    print(rid)
    cmd.execute("select * from bus_details where bus_id='"+str(rid)+"'")
    an=cmd.fetchone()
    print(an)
    return render_template("updatebus.html",val=an)
@bus.route("/updatebus",methods=['post'])
def updatebus():
    rid=session["busid"]
    busname = request.form["bus_name"]
    busregnum = request.form["registration_number"]
    ownername = request.form["name_of_owner"]
    mobnu = request.form["monb"]
    from_location = request.form["from_location"]
    to_location = request.form["to_location"]
    departure = request.form["departure"]
    arrival = request.form["arrival"]

    facility = request.form.getlist('facilities')
    fac = ','.join(facility)

    cmd.execute( "UPDATE bus_details SET bus_name=%s, bus_regno=%s, owner_name=%s, mobile_number=%s, `from`=%s, `to`=%s, depature=%s, arrival=%s, fac=%s WHERE bus_id=%s",(busname, busregnum, ownername, mobnu, from_location, to_location, departure, arrival, fac, rid))
    return '''<script>alert("updated successfully");window.location="/viewbus"</script>'''
@bus.route('/changeimage')
def changeimage():
    return render_template('changeimage.html')
@bus.route('/updateimage',methods=['POST'])
def updateimage():
    rid=session["busid"]
    fileupload = request.files['fileField']
    fi = secure_filename(fileupload.filename)
    fileupload.save(os.path.join("static/images", fi))
    cmd.execute("update bus_details set image='"+fi+"' where bus_id ='"+rid+"'")
    con.commit()
    return '''<script>alert("image updated");window.location='/viewbus'</script>'''

@bus.route('/addhospital')
def addhospital():

    return render_template('hospitalreg.html')
@bus.route('/addhospitaldetails', methods=['post'])
def addhospitaldetails():
    hos_name = request.form["hos_name"]
    hos_plc = request.form["hos_plc"]
    monb = request.form["monb"]
    lati = request.form["lati"]
    longi = request.form["longi"]
    fileupload = request.files['fileField']
    fi = secure_filename(fileupload.filename)
    fileupload.save(os.path.join("static/images", fi))
    cmd.execute( "insert into hospital_details values(null,'" + hos_name + "','" + hos_plc + "','" + monb + "','" + lati + "','" + longi + "','" + fi + "')")
    con.commit()
    return '''<script>alert("inserted successfully");window.location="viewbus"</script>'''
@bus.route('/viewhospital')
def viewhospital():
    cmd.execute("select * from hospital_details")
    result = cmd.fetchall()
    print(result)
    return render_template("hospitalview.html",value=result)
@bus.route("/deleletehospital")
def deleletehospital():
    id = request.args.get("id")
    print(id)
    cmd.execute("DELETE FROM hospital_details WHERE h_id='" + str(id) + "'")
    con.commit()
    return '''<script>alert("bus deleted successfully");window.location="/viewhospital"</script>'''

@bus.route("/edithospital")
def edithospital():
    rid=request.args.get("id")
    session["hid"]=rid
    print(rid)
    cmd.execute("select * from hospital_details where h_id='"+str(rid)+"'")
    an=cmd.fetchone()
    print(an)
    return render_template("updatehos.html",value=an)
@bus.route("/updatehos",methods=['post'])
def updatehos():
    rid=session["hid"]
    hos_name = request.form["hos_name"]

    hos_plc = request.form["hos_plc"]
    monb = request.form["monb"]
    lati = request.form["lati"]
    longi = request.form["longi"]
    cmd.execute( "UPDATE hospital_details SET hos_name='"+hos_name+"', place='"+hos_plc+"', mobile_number='"+monb+"',latitude='"+lati+"',longitude='"+longi+"'  WHERE h_id='"+rid+"'")
    con.commit()
    return '''<script>alert("updated successfully");window.location="/viewhospital"</script>'''
@bus.route('/changeimagehospital')
def changeimagehospital():
    return render_template('changeimagehospitals.html')
@bus.route('/changeimagehos',methods=['POST'])
def changeimagehos():
    rid=session["hid"]
    fileupload = request.files['fileField']
    fi = secure_filename(fileupload.filename)
    fileupload.save(os.path.join("static/images", fi))
    cmd.execute("update hospital_details set image='"+fi+"' where h_id ='"+rid+"'")
    con.commit()
    return '''<script>alert("image updated");window.location='/viewhospital'</script>'''
@bus.route('/addpolice')
def addpolice():

    return render_template('policestationreg.html')
@bus.route('/addpolicdetails', methods=['post'])
def addpolicdetails():
    pstn_name = request.form["pstn_name"]
    stn_plc = request.form["stn_plc"]
    mob = request.form["mob"]
    lati = request.form["lati"]
    longi = request.form["longi"]
    sid = request.form["sid"]
    uname = request.form["uname"]
    passw = request.form["passw"]
    cmd.execute( "insert into login values(null,'" + uname + "','" + passw + "','police')")
    id=cmd.lastrowid

    cmd.execute( "insert into police_details values(null,'" + pstn_name + "','" + stn_plc + "','" + mob + "','" + lati + "','" + longi + "','" + sid + "','"+str(id)+"')")
    con.commit()
    return '''<script>alert("inserted successfully");window.location="viewbus"</script>'''
@bus.route('/viewpolice')
def viewpolice():
    cmd.execute("select * from police_details")
    result = cmd.fetchall()
    print(result)
    return render_template("policeview.html",value=result)
@bus.route("/deletepolice")
def deletepolice():
    id = request.args.get("id")
    print(id)
    cmd.execute("DELETE FROM police_details WHERE p_id='" + str(id) + "'")
    con.commit()
    return '''<script>alert("bus deleted successfully");window.location="/viewpolice"</script>'''
@bus.route("/editpolice")
def editpolice():
    rid=request.args.get("id")
    session["hid"]=rid
    print(rid)
    cmd.execute("select * from police_details where p_id='"+str(rid)+"'")
    an=cmd.fetchone()
    print(an)
    return render_template("updatepolice.html",value=an)
@bus.route("/updatepolicedetails",methods=['post'])
def updatepolicedetails():
    rid=session["hid"]
    pstn_name = request.form["po_name"]
    stn_plc = request.form["ps_plc"]
    monb = request.form["monb"]
    lati = request.form["lati"]
    longi = request.form["longi"]
    sid = request.form["sid"]
    cmd.execute( "UPDATE police_details SET pstn_name='"+pstn_name+"',stn_plc='"+stn_plc+"', mob='"+monb+"', lati='"+lati+"',longi='"+longi+"',sid='"+sid+"'  WHERE p_id='"+rid+"'")
    con.commit()
    return '''<script>alert("updated successfully");window.location="/viewpolice"</script>'''
@bus.route('/blockvehiclefulldetails')
def blockvehiclefulldetails():

    cmd.execute("SELECT `bus_details`.*,`login`.* FROM `bus_details` JOIN `login` ON `bus_details`.loginid=login.id  ")
    result=cmd.fetchall()
    return render_template('blockvehicle.html', value=result)

@bus.route('/blockvehicle')
def blockvehicle():
    did = request.args.get("id")
    cmd.execute("UPDATE login SET user_type='blocked' WHERE id=%s", (did,))
    con.commit()
    return '''<script>alert("Successfully Blocked");window.location='/blockvehiclefulldetails'</script>'''
@bus.route('/unblockvehicle')
def unblockvehicle():
    cid = request.args.get("id")
    cmd.execute("UPDATE login SET user_type='bus' WHERE id=%s", (cid,))
    con.commit()
    return '''<script>alert("Successfully Unblocked");window.location='/blockvehiclefulldetails'</script>'''
@bus.route('/viewoverspeed')
def viewoverspeed():
    cmd.execute("SELECT * FROM `accident_details` WHERE speed >80")
    result=cmd.fetchall()
    return render_template('overspeedvechicle.html',value=result)
@bus.route('/sendNotification')
def sendNotification():
    ntid=request.args.get('id')
    print(ntid)
    session['nid']=ntid
    return render_template('sendnotif.html')
@bus.route('/sendnotif',methods=['post'])
def sendnotif():
    nidd=session['nid']
    print(nidd)
    notif=request.form['notif']
    print(notif)
    cmd.execute("update accident_details set notif='"+notif+"' where id='"+str(nidd)+"'")
    con.commit()
    return '''<script>alert("Successfully send");window.location='/viewoverspeed'</script>'''
@bus.route('/accidentdetails')
def accidentdetails():
    cmd.execute("select * from accident_details ")
    result=cmd.fetchall()
    return render_template('accidentdetails.html',value=result)













bus.run(debug=True)