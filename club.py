from flask import Blueprint, render_template, request, session
import hashlib, string, random, psycopg2, os, bcrypt, datetime, smtplib, db
from datetime import date

club_bp = Blueprint('club', __name__, url_prefix='/club')

#DB接続
def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

#サークル参加申請処理
@club_bp.route("/club_join_req", methods=["POST"])
def club_join_req():
    student_id = request.form.get("student_id")
    print(student_id)
    club_id =  request.form.get("club_id")
    session["student_id"] = student_id
    session["club_id"] = club_id
    return render_template("club_join_send.html" ,student_id = student_id, club_id=club_id)

@club_bp.route("/club_join_req2", methods=["POST"])
def club_join_req2():
    club_id = session.get("club_id")
    student_id = session.get("student_id")
    print(club_id, student_id)
    return render_template("club_join_send.html" ,student_id = student_id, club_id=club_id)

#サークル参加申請確認処理
@club_bp.route("/club_join_req3")
def club_join_req3():
    club_id = session.get("club_id")
    student_id = session.get("student_id")
    print("club_jpin_req3")
    print(student_id)
    print(club_id) #できてる
    sql = "INSERT INTO student_club (student_id, club_id, is_leader, allow) VALUES (%s, %s, %s, 0)"
    try :
        connection = get_connection()
        cursor = connection.cursor()   
        cursor.execute(sql, (student_id, club_id, False))
        connection.commit()
    except psycopg2.DatabaseError:
            count = 0
    finally :
            cursor.close()
            connection.close()     
    return render_template('club_join_reqres.html', student=student_id)

#おすすめサークル表示
def club_list():
    club = []
    for row in db.get_club_list() :
        count = db.count_joinedclub(row[0])
        club.append((row, count))
    return club

#サークル詳細表示
@club_bp.route("/club_detail", methods=['GET'])
def club_detail():
    student = request.args.get('student')
    print(student)
    club_id = request.args.get('club_id')
    club_detail = db.get_club_detail(club_id)
    member = db.get_joinedmember(club_id)
    schedule = db.get_schedule(club_id)
    schedulelist = []
    daylist = []
    memberlist = []
    for row in member:
        member = db.get_student(row)
        memberlist.append(member[1])
    for row in schedule:
        schedulelist.append(row)
    for row in schedule:
        formatted_date = row[2].strftime('%Y-%m-%d')
        daylist.append(formatted_date)
    print(club_detail)
    return render_template('club_detail.html', club_id=club_id, club_detail=club_detail, memberlist=memberlist, schedulelist=schedulelist, daylist=daylist, student=student)

#ログイン前サークル詳細表示
@club_bp.route("/club_detail_nolog", methods=['GET'])
def club_detail_nolog():
    club_id = request.args.get('club_id')
    club_detail = db.get_club_detail(club_id)
    member = db.get_joinedmember(club_id)
    schedule = db.get_schedule(club_id)
    schedulelist = []
    daylist = []
    memberlist = []
    for row in member:
        member = db.get_student(row)
        memberlist.append(member[1])
    for row in schedule:
        schedulelist.append(row)
    for row in schedule:
        formatted_date = row[2].strftime('%Y-%m-%d')
        daylist.append(formatted_date)
    return render_template('club_detail_nolog.html', club_id=club_id, club_detail=club_detail, memberlist=memberlist, schedulelist=schedulelist, daylist=daylist)

#教員サークル詳細表示
@club_bp.route("/club_detail_teacher", methods=['GET'])
def club_detail_teacher():
    club_id = request.args.get('club_id')
    club_detail = db.get_club_detail(club_id)
    member = db.get_joinedmember(club_id)
    schedule = db.get_schedule(club_id)
    schedulelist = []
    daylist = []
    memberlist = []
    for row in member:
        member = db.get_student(row)
        memberlist.append(member[1])
    for row in schedule:
        schedulelist.append(row)
    for row in schedule:
        formatted_date = row[2].strftime('%Y-%m-%d')
        daylist.append(formatted_date)
    return render_template('club_detail_teacher.html', club_id=club_id, club_detail=club_detail, memberlist=memberlist, schedulelist=schedulelist, daylist=daylist)

#リーダーサークル詳細表示
@club_bp.route("/club_detail_leader", methods=['GET'])
def club_detail_leader():
    student = request.args.get('student')
    club_id = request.args.get('club_id')
    club_detail = db.get_club_detail(club_id)
    member = db.get_joinedmember(club_id)
    schedule = db.get_schedule(club_id)
    schedulelist = []
    daylist = []
    memberlist = []
    for row in member:
        member = db.get_student(row)
        memberlist.append(member[1])
    for row in schedule:
        schedulelist.append(row)
    for row in schedule:
        formatted_date = row[2].strftime('%Y-%m-%d')
        daylist.append(formatted_date)
    return render_template('club_detail_leader.html', club_id=club_id, club_detail=club_detail, memberlist=memberlist, schedulelist=schedulelist, daylist=daylist, student=student)