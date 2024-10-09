import pymysql
from flask import Flask, request, jsonify

flutter = Flask(__name__)
flutter.secret_key = 'abc'
con = pymysql.connect(host='localhost', user='root', password='root', port=3306, db='bus_safety', charset='utf8')
cmd = con.cursor()

@flutter.route("/logincheck", methods=['GET', 'POST'])
def logincheck():
    user = request.args.get("email")
    print(user)
    passw = request.args.get("password")
    print(passw)
    cmd.execute("SELECT * FROM login WHERE username=%s AND password=%s", (user, passw))
    result = cmd.fetchone()
    print(result)
    if result is None:
        return jsonify({'task': "invalid"})
    return jsonify({'task': 'success', 'lid': result[0], 'type': result[3]})

@flutter.route("/user", methods=['POST'])
def user():
    data = request.json
    print(data)

    # Retrieve data from the request
    name = data.get("name")
    dob = data.get("dob")
    gender = data.get("gender")
    mstatus = data.get("mstatus")
    phone = data.get("phone")
    username = data.get("username")
    password = data.get("password")
    gurd = data.get("gurd")
    user_type = data.get("type")

    try:
        cmd.execute("INSERT INTO login VALUES (NULL, %s, %s, 'user')", (username, password))
        id = cmd.lastrowid
        cmd.execute("INSERT INTO user_details VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (name, dob, gender, mstatus, phone, gurd, user_type, str(id)))
        con.commit()
        return {'task': 'success'}
    except Exception as e:
        con.rollback()  # Rollback in case of error
        return {'task': 'error', 'message': str(e)}

@flutter.route("/userprofile",methods=['post','get'])
def userprofile():
    userid=request.args.get("lid")
    print(userid)
    cmd.execute("SELECT * FROM `user_details` WHERE `loginid`='"+userid+"'")
    result=cmd.fetchall()
    print(result)
    row_headers=[x[0] for x in cmd.description]
    json_data=[]
    print(json_data)
    for result in result: json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)


@flutter.route("/userupdate", methods=['POST'])
def userupdate():
    data = request.json
    print(data)
    ("sdfghjndfghb")

    # Retrieve data from the request
    name = data.get("name")
    dob = data.get("dob")
    gender = data.get("gender")
    mstatus = data.get("mstatus")
    phone = data.get("phone")
    gurd = data.get("gurd")
    user_type = data.get("type")
    user_id = data.get("id")
    print(user_id)# Assuming you get the user ID from the request
    cmd.execute("update user_details set name='"+name+"',dob='"+dob+"',gender='"+gender+"',mstatus='"+mstatus+"',phone='"+phone+"',guard='"+gurd+"',type='"+user_type+"' where loginid='"+str(user_id)+"'")
    con.commit()
    return {'task': 'success'}


flutter.run(host='0.0.0.0', port=5000)
