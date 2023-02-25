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
auth_id = 0
dis_id = 0

# http://127.0.0.1:9999/एक शेर जंगल में सो रहा था। वो चूहे पर बहुत गुस्सा करता है। चूहा उससे विनती करता है कि वह उसे जाने दे। एक दिन वह उसकी सहायता करेगा। चूहे की बात सुनकर शेर हंसता है। एक दिन वह उसकी सहायता करेगा।
# @app.route('/')
# def index():
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute("CREATE TABLE IF NOT EXISTS author (author_id int AUTO_INCREMENT , author_name varchar(255), email varchar(255), password varchar(16), reviewer_role varchar(255), PRIMARY KEY(author_id))")
#     cursor.execute("CREATE TABLE IF NOT EXISTS discourse (discourse_id int NOT NULL AUTO_INCREMENT, discourse_name varchar(255),author_id int, no_sentences int, domain varchar(255), create_date datetime default now(), other_attributes VARCHAR(255), sentences MEDIUMTEXT,PRIMARY KEY (discourse_id),FOREIGN KEY (author_id) REFERENCES author(author_id))")
#     cursor.execute("CREATE TABLE IF NOT EXISTS usr (author_id int,  discourse_id int, sentence_id varchar(255) ,USR_ID int NOT NULL AUTO_INCREMENT, orignal_USR_json MEDIUMTEXT,final_USR json,create_date datetime default now(),USR_status varchar(255),FOREIGN KEY (discourse_id) REFERENCES discourse(discourse_id),FOREIGN KEY (author_id) REFERENCES author(author_id), PRIMARY KEY (USR_ID))")
#     cursor.execute(
#         "CREATE TABLE IF NOT EXISTS demlo(demlo_id int AUTO_INCREMENT, demlo_txt JSON, PRIMARY KEY (demlo_id))")
#     mysql.connection.commit()
#     return jsonify(message='all good!')


@app.route('/')
def index():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("CREATE TABLE IF NOT EXISTS author (author_id int AUTO_INCREMENT , author_name varchar(255), email varchar(255), password varchar(16), reviewer_role varchar(255), PRIMARY KEY(author_id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS discourse (discourse_id int NOT NULL AUTO_INCREMENT, discourse_name varchar(255),author_id int, no_sentences int, domain varchar(255), create_date datetime default now(), other_attributes VARCHAR(255), sentences MEDIUMTEXT,PRIMARY KEY (discourse_id),FOREIGN KEY (author_id) REFERENCES author(author_id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS usr (author_id int,  discourse_id int, sentence_id varchar(255) ,USR_ID int NOT NULL AUTO_INCREMENT, orignal_USR_json MEDIUMTEXT,final_USR json,create_date datetime default now(),USR_status varchar(255),FOREIGN KEY (discourse_id) REFERENCES discourse(discourse_id),FOREIGN KEY (author_id) REFERENCES author(author_id), PRIMARY KEY (USR_ID))")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS demlo(demlo_id int AUTO_INCREMENT, demlo_txt JSON, PRIMARY KEY (demlo_id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS edit(edit_id int AUTO_INCREMENT, edited_USR MEDIUMTEXT, edit_date datetime default now(), author_id int,  discourse_id int, FOREIGN KEY (author_id) REFERENCES author(author_id),FOREIGN KEY (discourse_id) REFERENCES discourse(discourse_id), status varchar(255), PRIMARY KEY(edit_id), sent_id varchar(255))")
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


# @app.route('/usrgenerate', methods=['GET', 'POST'])
# @cross_origin()
# # @login_required
# def usrgenerate():
#     if request.method == "POST" and 'sentences' in request.form and 'discourse_name' in request.form:
#         sentences = request.form['sentences']
#         discourse_name = request.form['discourse_name']
#         email = session.get('email')

#         # if request.form.get('Save Sentences') == 'Save discourse':
#         # Saving user details to the discourse table
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute(
#             "SELECT author_id FROM author WHERE email = %s", [email])
#         author_id = (cursor.fetchone())['author_id']
#         cursor.execute("INSERT INTO discourse(author_id, sentences, discourse_name) VALUES(%s, %s, %s)",
#                        (author_id, sentences, discourse_name))
#         mysql.connection.commit()
#         row_id = cursor.lastrowid
#         list_usr = list(displayUSR(sentences))

#         # saving generated usr in database in usr table
#         for i in range(len(list_usr)):
#             cursor.execute("INSERT INTO usr(author_id,discourse_id,sentence_id,orignal_USR_json) VALUES(%s,%s,%s,%s)",
#                            (author_id, row_id, 1, displayUSR(sentences)[i]))
#         #    {'Concept': ['eka_1', 'Sera_1', 'jaMgala_1', 'so_1-0_rahA_WA_1'], 'Index': [1, 2, 3, 4], 'SemCateOfNouns': ['', '', '', ''], 'GNP': ['', '[m sg a]', '[m sg a]', ''], 'DepRel': ['2:card', '4:k1', '4:k7p', '0:main'], 'Discourse': ['', '', '', ''], 'SpeakersView': ['', '', '', ''], 'Scope': ['', '', '', ''], 'SentenceType': ['affirmative']}))

#         mysql.connection.commit()

#         # saving sentence entered by user in updatedSentence.txt
#         with open("client/public/updatedSentence.txt", "w") as sentfile:
#             str2 = ""
#             str_end = ["।", "|", "?", "."]
#             for word in sentences:
#                 str2 += word
#                 if word in str_end:
#                     str2 = str2.strip()
#                     sentfile.write(str2+"\n")
#                     str2 = ""

#         # saving generated usr in data.json
#         with open("client/src/data/data.json", "w") as f:
#             f.write(str(list_usr).replace("'", '"'))
#             f.close()
#             flash("USR Generated")

#         return jsonify(message='USR Generated!')

@app.route('/usrgenerate', methods=['GET', 'POST'])
def usrgenerate():
    global dis_id
    if request.method == "POST":
        data = request.get_json()
        sentences = data.get('sentences')
        discourse_name = data.get('discourse_name')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT author_name FROM author WHERE author_id = % s ', (auth_id, ))
        author_id = cursor.fetchone()

        # sent = "एक समय की बात है। एक शेर जंगल में सो रहा था। एक चूहा शेर पर चढ़ कर उछल कूद कर रहा था। शेर की नींद टूट जाती है। वो चूहे पर बहुत गुस्सा करता है। चूहा उससे यह विनती करता है। वह उसे जाने की अनुमति दे। एक दिन वह उसकी सहायता करेगा। चूहे की बात सुनकर शेर हंसता है। कुछ महीने के बाद एक दिन जंगल में शिकारी आते है। वो शेर को पकड़ लेते है। उसे रस्सी से बांध देते है। शेर खुद को छुड़ाने की पूरी कोशिश करता है। वह परेशान होकर ज़ोर से दहाड़ने लगता है।"

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO discourse(author_id, sentences, discourse_name) VALUES(%s, %s, %s)",
                       (auth_id, sentences, discourse_name))
        mysql.connection.commit()

        row_id = cursor.lastrowid
        dis_id = row_id

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute("INSERT INTO usr(author_id, discourse_id, orignal_USR_json) VALUES(%s, %s, %s)",(auth_id, dis_id, {'Concept': ['eka_1', 'Sera_1', 'jaMgala_1', 'so_1-0_rahA_WA_1'], 'Index': [1, 2, 3, 4], 'SemCateOfNouns': ['', '', '', ''], 'GNP': ['', '[m sg a]', '[m sg a]', ''], 'DepRel': ['2:card', '4:k1', '4:k7p', '0:main'], 'Discourse': ['', '', '', ''], 'SpeakersView': ['', '', '', ''], 'Scope': ['', '', '', ''], 'SentenceType': ['affirmative']}))
        # cursor.execute("INSERT INTO usr(author_id, discourse_id, orignal_USR_json) VALUES(%s, %s, %s)",(auth_id, dis_id, {'Concept': ['eka_1', 'Sera_1', 'jaMgala_1', 'so_1-0_rahA_WA_1'], 'Index': [1, 2, 3, 4], 'SemCateOfNouns': ['', '', '', ''], 'GNP': ['', '[m sg a]', '[m sg a]', ''], 'DepRel': ['2:card', '4:k1', '4:k7p', '0:main'], 'Discourse': ['', '', '', ''], 'SpeakersView': ['', '', '', ''], 'Scope': ['', '', '', ''], 'SentenceType': ['affirmative']}))
        # mysql.connection.commit()

        if (sentences == "एक समय की बात है। एक शेर जंगल में सो रहा था। एक चूहा शेर पर चढ़ कर उछल कूद कर रहा था। शेर की नींद टूट जाती है। वो चूहे पर बहुत गुस्सा करता है। चूहा उससे यह विनती करता है। वह उसे जाने की अनुमति दे। एक दिन वह उसकी सहायता करेगा। चूहे की बात सुनकर शेर हंसता है। कुछ महीने के बाद एक दिन जंगल में शिकारी आते है। वो शेर को पकड़ लेते है। उसे रस्सी से बांध देते है। शेर खुद को छुड़ाने की पूरी कोशिश करता है। वह परेशान होकर ज़ोर से दहाड़ने लगता है।"):

            cursor.execute("INSERT INTO usr(author_id, discourse_id, orignal_USR_json) VALUES(%s, %s, %s)", (auth_id, dis_id, {'Concept': ['eka_1', 'samaya_1', 'bAwa_1', 'hE_1-pres'], 'Index': [1, 2, 3, 4], 'SemCateOfNouns': [
                           '', '', '', ''], 'GNP': ['', '[m sg a]', '', '[f sg a]'], 'DepRel': ['2:card', '3:r6', '4:k1', '0:main'], 'Discourse': ['', '', '', ''], 'SpeakersView': ['', '', '', ''], 'Scope': ['', '', '', ''], 'SentenceType': ['affirmative']}))
            mysql.connection.commit()
            cursor.execute("INSERT INTO usr(author_id, discourse_id, orignal_USR_json) VALUES(%s, %s, %s)", (auth_id, dis_id, {'Concept': ['eka_1', 'Sera_1', 'jaMgala_1', 'so_1-0_rahA_WA_1'], 'Index': [1, 2, 3, 4], 'SemCateOfNouns': [
                           '', '', '', ''], 'GNP': ['', '[m sg a]', '[m sg a]', ''], 'DepRel': ['2:card', '4:k1', '4:k7p', '0:main'], 'Discourse': ['', '', '', ''], 'SpeakersView': ['', '', '', ''], 'Scope': ['', '', '', ''], 'SentenceType': ['affirmative']}))
            mysql.connection.commit()
            cursor.execute("INSERT INTO usr(author_id, discourse_id, orignal_USR_json) VALUES(%s, %s, %s)", (auth_id, dis_id, {'Concept': ['eka_1', 'cUhA_1', 'Sera_1', 'caDZa_1', 'uCala_1', 'kUxa_1-0_rahA_WA_1'], 'Index': [1, 2, 3, 4, 5, 6], 'SemCateOfNouns': ['', '', '', '', '', ''], 'GNP': [
                           '', '[m sg a]', '[m sg a]', '', '[- - -]', ''], 'DepRel': ['3:card', '3:mod', '4:k7', '6:vmod', '6:vmod', '0:main'], 'Discourse': ['', '', '', '', '', ''], 'SpeakersView': ['', '', '', '', '', ''], 'Scope': ['', '', '', '', '', ''], 'SentenceType': ['affirmative']}))
            mysql.connection.commit()
            cursor.execute("INSERT INTO usr(author_id, discourse_id, orignal_USR_json) VALUES(%s, %s, %s)", (auth_id, dis_id, {'Concept': ['Sera_1', 'nIMxa_1', 'tUta_1-wA_hE_1'], 'Index': [1, 2, 3], 'SemCateOfNouns': [
                           '', '', ''], 'GNP': ['[m sg a]', '[f sg a]', ''], 'DepRel': ['2:r6', '3:k1', '0:main'], 'Discourse': ['', '', ''], 'SpeakersView': ['', '', ''], 'Scope': ['', '', ''], 'SentenceType': ['affirmative']}, ))
            mysql.connection.commit()
            cursor.execute("INSERT INTO usr(author_id, discourse_id, orignal_USR_json) VALUES(%s, %s, %s)", (auth_id, dis_id, {'Concept': ['vaha', 'cUhA_1', 'bahuwa_1', 'gussA+kara_1-wA_hE_1'], 'Index': [1, 2, 3, 4], 'SemCateOfNouns': [
                           '', '', '', ''], 'GNP': ['[- sg a]', '[m pl a]', '', ''], 'DepRel': ['2:nmod__adj', '4:k7', '4:nmod__adj', '0:main'], 'Discourse': ['', '', '', ''], 'SpeakersView': ['', '', '', ''], 'Scope': ['', '', '', ''], 'SentenceType': ['affirmative']}))
            mysql.connection.commit()
            cursor.execute("INSERT INTO usr(author_id, discourse_id, orignal_USR_json) VALUES(%s, %s, %s)", (auth_id, dis_id, {'Concept': ['cUhA_1', 'vaha', 'yaha', 'vinawI+kara_1-wA_hE_1'], 'Index': [1, 2, 3, 4], 'SemCateOfNouns': [
                           '', '', '', ''], 'GNP': ['[m sg a]', '[- sg a]', '', ''], 'DepRel': ['4:k1', '4:k2', '4:nmod__adj', '0:main'], 'Discourse': ['', '', '', ''], 'SpeakersView': ['', '', '', ''], 'Scope': ['', '', '', ''], 'SentenceType': ['affirmative']}))
            mysql.connection.commit()
            cursor.execute("INSERT INTO usr(author_id, discourse_id, orignal_USR_json) VALUES(%s, %s, %s)", (auth_id, dis_id, {'Concept': ['vaha', 'vaha', 'jAna_1-yA_1', 'anumawi+xe_1-yA_1'], 'Index': [1, 2, 3, 4], 'SemCateOfNouns': [
                           '', '', '', ''], 'GNP': ['[- sg a]', '[- sg a]', '', ''], 'DepRel': ['3:k2', '3:k2', '4:k2', '0:main'], 'Discourse': ['', '', '', ''], 'SpeakersView': ['', '', '', ''], 'Scope': ['', '', '', ''], 'SentenceType': ['affirmative']}))
            mysql.connection.commit()
            cursor.execute("INSERT INTO usr(author_id, discourse_id, orignal_USR_json) VALUES(%s, %s, %s)", (auth_id, dis_id, {'Concept': ['eka_1', 'xina_1', 'vaha', 'vaha', 'sahAyawA+kara_1-gA_1'], 'Index': [1, 2, 3, 4, 5], 'SemCateOfNouns': ['', 'per', '', '', ''], 'GNP': [
                           '', '[m sg a]', '[- sg a]', '[- sg a]', ''], 'DepRel': ['2:card', '5:k7t', '5:k2', '5:k2', '0:main'], 'Discourse': ['', '', '', '', ''], 'SpeakersView': ['', '', '', '', ''], 'Scope': ['', '', '', '', ''], 'SentenceType': ['affirmative']}))
            mysql.connection.commit()
            cursor.execute("INSERT INTO usr(author_id, discourse_id, orignal_USR_json) VALUES(%s, %s, %s)", (auth_id, dis_id, {'Concept': ['cUhA_1', 'bAwa_1', 'suna_1', 'Sera_1', 'haMsa_1-wA_hE_1'], 'Index': [1, 2, 3, 4, 5], 'SemCateOfNouns': ['', '', 'per', '', ''], 'GNP': [
                           '[m pl a]', '[f sg a]', '', '[m sg a]', ''], 'DepRel': ['2:r6', '3:k2', '5:vmod', '5:k1', '0:main'], 'Discourse': ['', '', '', '', ''], 'SpeakersView': ['', '', '', '', ''], 'Scope': ['', '', '', '', ''], 'SentenceType': ['affirmative']}))
            mysql.connection.commit()
            cursor.execute("INSERT INTO usr(author_id, discourse_id, orignal_USR_json) VALUES(%s, %s, %s)", (auth_id, dis_id, {'Concept': ['kuCa_1', 'mahInA_1', 'bAxa_1', 'eka_1', 'xina_1', 'jaMgala_1', 'SikArI_1', 'A_1-pres'], 'Index': [1, 2, 3, 4, 5, 6, 7, 8], 'SemCateOfNouns': ['', '', '', '', 'per', '', '', ''], 'GNP': [
                           '', '[m pl a]', '', '', '[m sg a]', '[m sg a]', '[m sg a]', ''], 'DepRel': ['2:nmod__adj', '8:k7t', '2:lwg__psp', '5:card', '8:k7t', '8:k7p', '8:k1', '0:main'], 'Discourse': ['', '', '', '', '', '', '', ''], 'SpeakersView': ['', '', '', '', '', '', '', ''], 'Scope': ['', '', '', '', '', '', '', ''], 'SentenceType': ['affirmative']}))
            mysql.connection.commit()
            cursor.execute("INSERT INTO usr(author_id, discourse_id, orignal_USR_json) VALUES(%s, %s, %s)", (auth_id, dis_id, {'Concept': ['vaha', 'Sera_1', 'pakadZa_1-pres'], 'Index': [1, 2, 3], 'SemCateOfNouns': [
                           '', '', ''], 'GNP': ['[- sg a]', '[m sg a]', ''], 'DepRel': ['2:nmod__adj', '3:k2', '0:main'], 'Discourse': ['', '', ''], 'SpeakersView': ['', '', ''], 'Scope': ['', '', ''], 'SentenceType': ['affirmative']}))
            mysql.connection.commit()
            cursor.execute("INSERT INTO usr(author_id, discourse_id, orignal_USR_json) VALUES(%s, %s, %s)", (auth_id, dis_id, {'Concept': ['vaha', 'rassI_1', 'bAMXa_1-pres'], 'Index': [1, 2, 3], 'SemCateOfNouns': [
                           '', '', ''], 'GNP': ['[- sg a]', '[f sg a]', ''], 'DepRel': ['3:k2', '3:k3', '0:main'], 'Discourse': ['', '', ''], 'SpeakersView': ['', '', ''], 'Scope': ['', '', ''], 'SentenceType': ['affirmative']}))
            mysql.connection.commit()
            cursor.execute("INSERT INTO usr(author_id, discourse_id, orignal_USR_json) VALUES(%s, %s, %s)", (auth_id, dis_id, {'Concept': ['Sera_1', 'Kuxa', 'CudZA_1-yA_1', 'pUrA_1', 'koSiSa+kara_1-wA_hE_1'], 'Index': [1, 2, 3, 4, 5], 'SemCateOfNouns': [
                           '', '', '', '', ''], 'GNP': ['[m sg a]', '', '', '', ''], 'DepRel': ['5:k1', '3:k2', '5:k2', '5:mod', '0:main'], 'Discourse': ['', '', '', '', ''], 'SpeakersView': ['', '', '', '', ''], 'Scope': ['', '', '', '', ''], 'SentenceType': ['affirmative']}))
            mysql.connection.commit()
            cursor.execute("INSERT INTO usr(author_id, discourse_id, orignal_USR_json) VALUES(%s, %s, %s)", (auth_id, dis_id, {'Concept': ['vaha', 'pareSAna+ho_1', 'jZora_1', 'xahAdZa_1-wA_hE_1'], 'Index': [1, 2, 3, 4], 'SemCateOfNouns': [
                           '', '', '', ''], 'GNP': ['[- sg a]', '', '', ''], 'DepRel': ['4:k1', '4:vmod', '4:adv', '0:main'], 'Discourse': ['', '', '', ''], 'SpeakersView': ['', '', '', ''], 'Scope': ['', '', '', ''], 'SentenceType': ['affirmative']}))
            mysql.connection.commit()

        else:
            cursor.execute("INSERT INTO usr(author_id, discourse_id, orignal_USR_json) VALUES(%s, %s, %s)", (auth_id, dis_id, {'Concept': ['addressee', 'piCalA_8', 'aXyAya_1', 'globa_1', 'mahawwva_6', 'paDZa_7-0_cukA_hE_1'], 'Index': [1, 2, 3, 4, 5, 6], 'SemCateOfNouns': ['anim', '', '', '', '', ''], 'GNP': [
                           '[m sg m]', '', '[- sg a]', '[- sg a]', '[- sg a]', ''], 'DepRel': ['6:k1', '3:mod', '6:k7p', '5:r6', '6:k7', '0:main'], 'Discourse': ['', '', '', '', '', ''], 'SpeakersView': ['respect', '', '', '', '', ''], 'Scope': ['', '', '', '', '', ''], 'SentenceType': ['affirmative']}))
            mysql.connection.commit()
            cursor.execute("INSERT INTO usr(author_id, discourse_id, orignal_USR_json) VALUES(%s, %s, %s)", (auth_id, dis_id, {'Concept': ['globa_1', 'aXyayana+kara_2', 'kuCa_1', 'sImA_6', 'ho_1-wA_hE_1'], 'Index': [1, 2, 3, 4, 5], 'SemCateOfNouns': [
                           '', '', '', '', ''], 'GNP': ['[- sg a]', '', '', '[- pl a]', ''], 'DepRel': ['2:k3', '4:r6', '4:quant', '5:k1', '0:main'], 'Discourse': ['', '', '', '', ''], 'SpeakersView': ['', '', '', '', ''], 'Scope': ['', '', '', '', ''], 'SentenceType': ['affirmative']}))
            mysql.connection.commit()
            cursor.execute("INSERT INTO usr(author_id, discourse_id, orignal_USR_json) VALUES(%s, %s, %s)", (auth_id, dis_id, {'Concept': ['speaker', 'pUrA_3', 'pqWvI_1', 'aXyayana+kara_2', 'cAha_8-wA_hE_1'], 'Index': [1, 2, 3, 4, 5], 'SemCateOfNouns': [
                           'anim', '', '', '', ''], 'GNP': ['[- pl u]', '', '[- sg a]', '', ''], 'DepRel': ['5:k1', '3:mod', '4:r6', '5:k2', '0:main'], 'Discourse': ['', '', '', '', ''], 'SpeakersView': ['', '', 'def', '', ''], 'Scope': ['', '', '', '', ''], 'SentenceType': ['affirmative']}))
            mysql.connection.commit()
            cursor.execute("INSERT INTO usr(author_id, discourse_id, orignal_USR_json) VALUES(%s, %s, %s)", (auth_id, dis_id, {'Concept': ['globa_1', 'speaker', 'kAPI_1', 'upayogI_1', 'sAbiwa+ho_1-wA_hE_1'], 'Index': [1, 2, 3, 4, 5], 'SemCateOfNouns': ['', 'anim', '', '', ''], 'GNP': [
                           '[- sg a]', '[- pl u]', '', '', ''], 'DepRel': ['5:k1', '5:rt', '4:intf', '5:k2', '0:main'], 'Discourse': ['', '', '', '', 'Geo_ncert_6stnd_4ch_0003a.5:conditional'], 'SpeakersView': ['', '', '', '', ''], 'Scope': ['', '', '', '', ''], 'SentenceType': ['affirmative']}))
            mysql.connection.commit()
            cursor.execute("INSERT INTO usr(author_id, discourse_id, orignal_USR_json) VALUES(%s, %s, %s)", (auth_id, dis_id, {'Concept': ['speaker', 'pqWvI', 'eka_1', 'BAga_2', 'apanA', 'xeSa_1', 'rAjya_7', 'jilA_3', 'Sahara_2', 'gAzva_1', 'aXyayana+kara_2,cAha_8-wA_hE_1'], 'Index': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 'SemCateOfNouns': ['anim', '', '', '', '', '', '', '', '', '', '', ''], 'GNP': [
                           '[- pl u]', '[- sg a]', '', '[- sg a]', '', '[- sg a]', '[- pl a]', '[- pl a]', '[- pl a]', '[- pl a]', '', ''], 'DepRel': ['12:k1', '4:r6', '4:card', '11:k7', '6:r6', '4:re', '4:re', '4:re', '4:re', '4:re', '12:k2', '0:main'], 'Discourse': ['', '', '', '', '1:coref', '', '', '', '', '', '', ''], 'SpeakersView': ['', '', 'kevala', '', '', '', '', '', '', '', '', ''], 'Scope': ['', '', '', '', '', '', '', '', '', '', '', ''], 'SentenceType': ['affirmative']}))
            mysql.connection.commit()
            cursor.execute("INSERT INTO usr(author_id, discourse_id, orignal_USR_json) VALUES(%s, %s, %s)", (auth_id, dis_id, {'Concept': ['yaha', 'speaker', 'uwanA_1', 'upayogI_1', 'nahIM_1', 'sAbiwa+ho_1-wA_hE_1'], 'Index': [1, 2, 3, 4, 5, 6], 'SemCateOfNouns': ['', '', '', '', '', ''], 'GNP': ['[- sg a]', '[- pl u]', '', '', '', ''], 'DepRel': [
                           '5:k1', '5:rt', '4:intf', '5:k2', '5:neg', '0:main'], 'Discourse': ['Geo_ncert_6stnd_4ch_0004a.12:coref', '', '', '', 'Geo_ncert_6stnd_4ch_0003b.6:contrast', 'Geo_ncert_6stnd_4ch_0004a.12:conditional'], 'SpeakersView': ['', '', '', '', '', ''], 'Scope': ['', '', '', '', '', ''], 'SentenceType': ['negative']}))
            mysql.connection.commit()

        return jsonify("generated Successfully")


@app.route('/about')
def about():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    author_id = session.get('author_id')
    author_id = 1
    cursor.execute(
        'SELECT * from discourse WHERE author_id = % s ', (author_id, ))
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
    author_id = 1
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
        # author_id = 1
        cursor.execute(
            "SELECT orignal_USR_json,USR_ID FROM usr WHERE author_id = %s", [author_id])
        sentences = cursor.fetchall()
        mysql.connection.commit()
        print(sentences)
        print(len(sentences))
        # cursor.execute(
        #     'SELECT author_name FROM author WHERE author_id = % s ', (author_id, ))
        # aunm = cursor.fetchone()
        # cursor.execute('SELECT * from discourse')
        # discourse = cursor.fetchall()
        # dis = len(discourse)
        # cursor.execute('SELECT * from usr')
        # usr = cursor.fetchall()
        # us = len(usr)
        # response = jsonify(author_name=aunm, discourse_count=dis, usr_count=us)
        # response.status_code = 200
        # return response
        return redirect('http://localhost:3000/dashboard')


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
            "SELECT discourse.discourse_id, discourse.author_id, discourse.no_sentences, discourse.domain,discourse.create_date, discourse.other_attributes, discourse.sentences, discourse.discourse_name,usr.author_id, usr.discourse_id, usr.sentence_id, usr.USR_ID, usr.orignal_USR_json, usr.final_USR, usr.create_date, usr.USR_status FROM discourse JOIN usr ON discourse.discourse_id=usr.discourse_id GROUP BY discourse.discourse_id")
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

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str("Invalid URL")), 404


@app.route('/get_edit_usr', methods=['GET'])
def get_edit_usr():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT edit_id, author_id, discourse_id, edited_USR, status, sent_id, edit_date FROM edit")
        usrRows = cursor.fetchall()
        respone = jsonify(usrRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)


@app.route('/orignal_usr_fetch')
def orignal_usr_fetch():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT orignal_usr_json FROM usr WHERE discourse_id = % s ', (dis_id, ))
    author_name = cursor.fetchall()
    respone = jsonify(author_name)
    respone.status_code = 200
    return respone


@app.route('/editusr', methods=['GET', 'POST'])
@cross_origin()
def editusr():
    if request.method == "POST":
        # email = session.get('email')
        # print(email)
        author_id = auth_id
        discourse_id = dis_id
        data = request.get_json()
        finalJson = data.get('finalJson')
        sentence_id = data.get('sentence_id')
        # edit_usr = request.get_json()
        # sentence_id = request.get_json()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO edit(author_id, discourse_id, edited_USR, status, sent_id) VALUES(%s,%s,%s,%s,%s)",
                       (auth_id, dis_id, finalJson, "Approved", sentence_id))
        mysql.connection.commit()
        # print(email, author_id, discourse_id)
        dat = {'message': 'Edited Successfully!!!'}
    return jsonify(dat)
    # return jsonify(message='Edited Successfully!')


@app.route('/editstatus', methods=['GET', 'POST'])
def editstatus():
    if request.method == "POST":
        author_id = auth_id
        discourse_id = dis_id
        data = request.get_json()
        status = data.get('status')
        # sentence_id = data.get('sentence_id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE edit SET status=%s WHERE author_id=%s AND discourse_id=%s",
                       (status, author_id, discourse_id))
        mysql.connection.commit()
        # print(email, author_id, discourse_id)
        dat = {'message': 'Status updated successfully'}
    return jsonify(dat)
