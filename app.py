from flask import Flask, flash, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
from flask_session import Session
from config import app
from wxconv import WXC
import MySQLdb.cursors
import re
from config import mysql
import os
import json
from flask_cors import CORS, cross_origin

# from client.src.Navigation import login
# from flask_restx import Api, Resource, fields
# import jwt
# from .models import db, Users
# from flask_restx import Api, Resource, fields
# import jwt
# from .models import db, Users

Session(app)
CORS(app)


# http://127.0.0.1:9999/एक शेर जंगल में सो रहा था। वो चूहे पर बहुत गुस्सा करता है। चूहा उससे विनती करता है कि वह उसे जाने दे। एक दिन वह उसकी सहायता करेगा। चूहे की बात सुनकर शेर हंसता है। एक दिन वह उसकी सहायता करेगा।
@app.route('/')
def index():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("CREATE TABLE IF NOT EXISTS author (author_id int AUTO_INCREMENT , author_name varchar(255), email varchar(255), password varchar(16), reviewer_role varchar(255), PRIMARY KEY(author_id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS discourse (discourse_id int NOT NULL AUTO_INCREMENT, discourse_name varchar(255),author_id int, no_sentences int, domain varchar(255), create_date datetime default now(), other_attributes VARCHAR(255), sentences MEDIUMTEXT,PRIMARY KEY (discourse_id),FOREIGN KEY (author_id) REFERENCES author(author_id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS usr (author_id int,  discourse_id int, sentence_id varchar(255) ,USR_ID int NOT NULL AUTO_INCREMENT, orignal_USR_json MEDIUMTEXT,final_USR json,create_date datetime default now(),USR_status varchar(255),FOREIGN KEY (discourse_id) REFERENCES discourse(discourse_id),FOREIGN KEY (author_id) REFERENCES author(author_id), PRIMARY KEY (USR_ID))")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS demlo(demlo_id int AUTO_INCREMENT, demlo_txt JSON, PRIMARY KEY (demlo_id))")
    mysql.connection.commit()
    return jsonify(message='all good!')


@app.route('/signup', methods=['GET', 'POST'])
@cross_origin()
def signup():
    msg = ''
    if request.method == 'POST' and 'author_name' in request.form and 'email' in request.form and 'password' in request.form and 'reviewer_role' in request.form:
        session["author_name"] = request.form['author_name']
        session["email"] = request.form['email']
        session["password"] = request.form['password']
        session["reviewer_role"] = request.form['reviewer_role']
        email = session.get('email')
        author_name = session.get('author_name')
        password = session.get('password')
        reviewer_role = session.get('reviewer_role')
        # author_name = request.form['author_name']
        # email = request.form['email']
        # password = request.form['password']
        # reviewer_role = request.form['reviewer_role']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM author WHERE author_name = % s', (author_name, ))
        author = cursor.fetchone()
        if author:
            flash('author already exists !')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address !')
        # elif not re.match(r'[A-Za-z]+', author_name):
        #     msg = 'author_name must contain only characters !'
        elif not author_name or not password or not email:
            flash('Please fill out the form !')
        else:
            # hashed_password = generate_password_hash(password)
            cursor.execute('INSERT INTO author VALUES (NULL, % s, % s, % s, % s)',
                           (author_name, email, password, reviewer_role))
            mysql.connection.commit()
            flash('You have successfully registered !')
            # return redirect(url_for(login))
            return redirect('http://localhost:3000/login')
    elif request.method == 'POST':
        flash('Please fill out the form !')
    return jsonify(message='signup')


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        session['email'] = request.form['email']
        password = request.form['password']
        email = session.get('email')
        # password = generate_password_hash(password)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('CREATE TABLE IF NOT EXISTS author (author_id int AUTO_INCREMENT , author_name varchar(255), email varchar(255), password varchar(16), reviewer_role varchar(255), PRIMARY KEY(author_id)) ')
        cursor.execute(
            'SELECT * FROM author WHERE email = % s AND password = % s', (email, password, ))
        author = cursor.fetchone()
        if author:
            session['loggedin'] = True
            session['author_id'] = author['author_id']
            session['email'] = author['email']
            msg = 'Logged in successfully !'
            flash('Logged in successfully')
            # return jsonify(message='login')
            return redirect('http://localhost:3000/usrgenerate')
            # return jsonify(message='login')

        else:
            flash('Incorrect loginId / password !')
    # return redirect('http://localhost:3000/usrgenerate')


@app.route('/logout')
def logout():
    session["email"] = None
    return redirect("http://localhost:3000/")
    # if request.method == 'GET':
    #     if session['loggedin'] == True:
    #         session['loggedin'] = False
    #         return redirect('http://localhost:3000/')
    #     else:
    #         return redirect('http://localhost:3000/')
    # return redirect('http://localhost:3000/usrgenerate')


@app.route('/usrgenerate', methods=['GET', 'POST'])
@cross_origin()
# @login_required
def usrgenerate():
    if request.method == "POST" and 'sentences' in request.form and 'discourse_name' in request.form:
        sentences = request.form['sentences']
        discourse_name = request.form['discourse_name']
        email = session.get('email')

        # if request.form.get('Save Sentences') == 'Save discourse':
        # Saving user details to the discourse table
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT author_id FROM author WHERE email = %s", [email])
        author_id = (cursor.fetchone())['author_id']
        cursor.execute("INSERT INTO discourse(author_id, sentences, discourse_name) VALUES(%s, %s, %s)",
                       (author_id, sentences, discourse_name))
        mysql.connection.commit()
        row_id = cursor.lastrowid
        list_usr = list(displayUSR(sentences))

        # saving generated usr in database in usr table
        for i in range(len(list_usr)):
            cursor.execute("INSERT INTO usr(author_id,discourse_id,sentence_id,orignal_USR_json) VALUES(%s,%s,%s,%s)",
                           (author_id, row_id, 1, displayUSR(sentences)[i]))
        #    {'Concept': ['eka_1', 'Sera_1', 'jaMgala_1', 'so_1-0_rahA_WA_1'], 'Index': [1, 2, 3, 4], 'SemCateOfNouns': ['', '', '', ''], 'GNP': ['', '[m sg a]', '[m sg a]', ''], 'DepRel': ['2:card', '4:k1', '4:k7p', '0:main'], 'Discourse': ['', '', '', ''], 'SpeakersView': ['', '', '', ''], 'Scope': ['', '', '', ''], 'SentenceType': ['affirmative']}))

        mysql.connection.commit()

        # saving sentence entered by user in updatedSentence.txt
        with open("client/public/updatedSentence.txt", "w") as sentfile:
            str2 = ""
            str_end = ["।", "|", "?", "."]
            for word in sentences:
                str2 += word
                if word in str_end:
                    str2 = str2.strip()
                    sentfile.write(str2+"\n")
                    str2 = ""

        # saving generated usr in data.json
        with open("client/src/data/data.json", "w") as f:
            f.write(str(list_usr).replace("'", '"'))
            f.close()
            flash("USR Generated")

        return jsonify(message='USR Generated!')


@app.route('/about')
def about():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * from discourse')
    discourse = cursor.fetchall()
    dis = len(discourse)
    cursor.execute('SELECT * from usr')
    usr = cursor.fetchall()
    us = len(usr)
    response = jsonify(discourse_count=dis, usr_count=us)
    response.status_code = 200
    return response


@app.route('/authName')
def authName():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    author_id = session.get('author_id')
    cursor.execute(
        'SELECT author_name FROM author WHERE author_id = % s ', (author_id, ))
    author_name = cursor.fetchone()
    respone = jsonify(author_name)
    respone.status_code = 200
    return respone


@app.route('/dash_out', methods=['GET'])
def dash_out():
    if request.method == 'GET':
        # session['email'] = request.form['email']
        email = session.get('email')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT author_id FROM author WHERE email = %s", [email])
        author_id = (cursor.fetchone())['author_id']
        print(author_id)
        cursor.execute(
            "SELECT orignal_USR_json FROM usr WHERE author_id = %s", [author_id])
        sentences = cursor.fetchall()
        mysql.connection.commit()
        print(sentences)
        print(len(sentences))
        cursor.execute(
            'SELECT author_name FROM author WHERE author_id = % s ', (author_id, ))
        author_name = cursor.fetchone()
        cursor.execute('SELECT * from discourse')
        discourse = cursor.fetchall()
        dis = len(discourse)
        cursor.execute('SELECT * from usr')
        usr = cursor.fetchall()
        us = len(usr)
        response = jsonify(discourse_count=dis, usr_count=us)
        response.status_code = 200
        return response
        # return redirect('http://localhost:3000/dashboard')


# @app.route('/dash_out', methods=['GET'])
# def dash_out():
#     if request.method == 'GET':
#         # session['email'] = request.form['email']
#         email = session.get('email')
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute(
#             "SELECT author_id FROM author WHERE email = %s", [email])
#         author_id = (cursor.fetchone())['author_id']
#         print(author_id)
#         cursor.execute(
#             "SELECT sentences FROM discourse WHERE author_id = %s", [author_id])
#         sentences = cursor.fetchall()
#         mysql.connection.commit()
#         print(sentences)
#         print(len(sentences))
#         return redirect('http://localhost:3000/dashboard')


@app.route('/authors')
def author():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT author_id, author_name, email, password, reviewer_role FROM author")
        authRows = cursor.fetchall()
        respone = jsonify(authRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)


@app.route('/author/<author_id>')
def auth_details(author_id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT author_id , author_name, email, password, reviewer_role FROM author WHERE author_id =%s", author_id)
        authRow = cursor.fetchone()
        respone = jsonify(authRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)


@app.route('/usr/<discourse_name>')
def usrin_details(discourse_name):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        row_id = cursor.lastrowid
        print(row_id)
        cursor.execute("SELECT discourse_id FROM discourse WHERE discourse_name = %s", [
                       discourse_name])
        dis_row = cursor.fetchone()
        d_id = dis_row.get("discourse_id")
        cursor.execute(
            "SELECT author_id, discourse_id, sentence_id, orignal_USR_json FROM usr  WHERE discourse_id  =%s", [d_id])
        authRow = cursor.fetchall()
        respone = jsonify(authRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)


@app.route('/discourse')
def discourse():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT discourse_id, author_id, no_sentences, domain,create_date, other_attributes, sentences, discourse_name FROM discourse")
        disRows = cursor.fetchall()
        respone = jsonify(disRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)


@app.route('/dash_data')
def dash_data():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT discourse.discourse_id, discourse.author_id, discourse.no_sentences, discourse.domain,discourse.create_date, discourse.other_attributes, discourse.sentences, discourse.discourse_name,usr.author_id, usr.discourse_id, usr.sentence_id, usr.USR_ID, usr.orignal_USR_json, usr.final_USR, usr.create_date, usr.USR_status FROM discourse JOIN usr ON discourse.discourse_id=usr.discourse_id")
        datarows = cursor.fetchall()
        respone = jsonify(datarows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)


@app.route('/USR')
def USR():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM usr")
        usrRows = cursor.fetchall()
        respone = jsonify(usrRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)


@app.route('/USR/<USR_ID>')
def usr_details(USR_ID):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT author_id, discourse_id, sentence_id, USR_ID, orignal_USR_json, final_USR, create_date, USR_status FROM usr WHERE discourse_id =%s", [USR_ID])
        usrRow = cursor.fetchall()
        respone = jsonify(usrRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str("Invalid URL")), 404


def displayUSR(corpus_for_usr):
    # Pre-processing of the corpus for USR generation.
    str1 = corpus_for_usr
    if corpus_for_usr is None:
        return jsonify("Not a Valid Sentence")

    f = open(
        "/home/var31/parser/sentences_for_USR", "w")
    # f = open(
    #     "/mnt/c/Users/gupta/OneDrive/Desktop/USR_GENERATOR/parser/sentences_for_USR", "w")
    str_end = ["।", "|", "?", "."]
    str2 = ""
    sent_id = 0
    for word in str1:
        str2 += word
        if word in str_end:
            str2 = str2.strip()
            f.write(str(sent_id)+"  "+str2+"\n")
            sent_id += 1
            str2 = ""
    f.close()
    # Clean up bulk USRs directory
    # for file in os.listdir("/mnt/c/Users/gupta/OneDrive/Desktop/USR_GENERATOR/parser/bulk_USRs"):
    #     os.remove(
    #         "/mnt/c/Users/gupta/OneDrive/Desktop/USR_GENERATOR/parser/bulk_USRs/"+file)
    # with open("/mnt/c/Users/gupta/OneDrive/Desktop/USR_GENERATOR/parser/sentences_for_USR", "r") as f:
    for file in os.listdir("/home/var31/parser/bulk_USRs"):
        os.remove(
            "/home/var31/parser/bulk_USRs/"+file)
    with open("/home/var31/parser/sentences_for_USR", "r") as f:
        for data in f:
            file_to_paste = open("/home/var31/parser/txt_files/bh-1", "w")
            # "/mnt/c/Users/gupta/OneDrive/Desktop/USR_GENERATOR/parser/txt_files/bh-1", "w")

            file_to_paste_temp = open("/home/var31/parser/bh-2", "w")

            sent = data.split("  ")[1]
            s_id = data.split("  ")[0]
            file_to_paste.write(sent)
            file_to_paste_temp.write(sent)
            file_to_paste_temp.close()
            file_to_paste.close()
            # os.system("cd /home/var31/parser")
            # os.system("ls")
            os.system(
                "python3 /home/var31/parser/sentence_check.py")
            os.system(
                "sh /home/var31/parser/makenewusr.sh /home/var31/parser/txt_files/bh-1")
            os.system(
                "python3 /home/var31/parser/generate_usr.py>/home/var31/parser/bulk_USRs/"+s_id)
            os.system(
                "python3 /home/var31/parser/delete_1.py")
    generated_usrs = {}
    gs = []
    for file in os.listdir("/home/var31/parser/bulk_USRs"):
        usr_file = open("/home/var31/parser/bulk_USRs/"+file, "r")
        usr_list = usr_file.readlines()
        usr_dict = {}
        # usr_dict["sentence_id"]=0,
        # usr_dict['sentence']=usr_list[0].strip()
        usr_dict['Concept'] = usr_list[2].strip().split(",")
        usr_dict['Index'] = [int(x) for x in usr_list[3].split(",")]
        usr_dict['SemCateOfNouns'] = usr_list[4].strip().split(",")
        usr_dict['GNP'] = usr_list[5].strip().split(",")
        usr_dict['DepRel'] = usr_list[6].strip().split(",")
        usr_dict['Discourse'] = usr_list[7].strip().split(",")
        usr_dict['SpeakersView'] = usr_list[8].strip().split(",")
        usr_dict['Scope'] = usr_list[9].strip().split(",")
        usr_dict['SentenceType'] = usr_list[10].strip().split(",")
        # generated_usrs[file]=usr_dict
        gs.append(usr_dict)
    # print(gs[0])
    print(gs)
    return gs
    # return jsonify(generated_usrs)


# sent = "एक समय की बात है।"
# print(displayUSR(sent))
