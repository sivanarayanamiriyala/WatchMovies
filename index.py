from flask import *
import mysql.connector

app=Flask(__name__)
app.secret_key="watchmovieswebsite"
db=mysql.connector.connect(host="localhost",user="root",password="siva1234",database="watch")
@app.route('/')
def index():
	mycursor=db.cursor()
	sql="select photoname,filename,number from movies order by viewcount desc limit 5"
	mycursor.execute(sql)
	data=mycursor.fetchall()

	mycursor=db.cursor(buffered=True)
	sql1="select photoname,filename,number from movies order by year desc limit 5"
	mycursor.execute(sql1)
	data1=mycursor.fetchall()

	mycursor=db.cursor(buffered=True)
	sql2="select photoname,filename,number from movies where language=%s limit 5"
	mycursor.execute(sql2,('hindi',))
	data2=mycursor.fetchall()

	mycursor=db.cursor(buffered=True)
	sql3="select photoname,filename,number from movies where language=%s limit 5"
	mycursor.execute(sql3,('telugu',))
	data3=mycursor.fetchall()

	mycursor=db.cursor(buffered=True)
	sql4="select photoname,filename,number from movies where language=%s limit 5"
	mycursor.execute(sql4,('english',))
	data4=mycursor.fetchall()

	
	return render_template('index.html',data=data,data1=data1,data2=data2,data3=data3,data4=data4)
	


@app.route('/movieslist')
def movieslist():	
	language=request.args['language']
	mycursor=db.cursor(buffered=True)	
	sql="select CONCAT(UCASE(MID(name,1,1)),MID(name,2)),year(year),photoname,number,CONCAT(UCASE(MID(language,1,1)),MID(language,2)) from movies where language=%s"
	mycursor.execute(sql,(language,))
	data=mycursor.fetchall()
	return render_template('movies-list.html',data=data,language=language)

@app.route('/movies')
def movies():
	number=request.args['number']
	sql="select CONCAT(UCASE(MID(name,1,1)),MID(name,2)),CONCAT(UCASE(MID(directedby,1,1)),MID(directedby,2)),cast,genres,photoname,filename,CONCAT(UCASE(MID(language,1,1)),MID(language,2)),About,year(year) from movies where number=%s"
	mycursor=db.cursor(buffered=True)
	mycursor.execute(sql,(number,))
	data=mycursor.fetchall()
	mycursor=db.cursor(buffered=True)
	sql1="update movies set viewcount=viewcount+1 where number=%s"
	mycursor.execute(sql1,(number,))
	db.commit()
	return render_template('movies.html',data=data)		



@app.route('/searchmovies')
def searchmovies():
	name=request.args['name']
	sql="select CONCAT(UCASE(MID(name,1,1)),MID(name,2)),year(year),photoname,number,CONCAT(UCASE(MID(language,1,1)),MID(language,2)) from movies where name like %s"
	mycursor=db.cursor()
	mycursor.execute(sql,("%"+name+"%",))
	data=mycursor.fetchall()
	print(data)
	return render_template('searchmovies.html',data=data)

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/admin',methods=['GET','POST'])
def admin():
	if request.method=='POST':
		username=request.form.get("username")
		password=request.form.get("password")
		sql="select * from admins where username=%s and password=%s"
		mycursor=db.cursor()
		mycursor.execute(sql,(username,password,))
		data=mycursor.fetchall()
		db.commit()
		if data:
			session['name']=data[0][2]
			return redirect(url_for('adminpage'))
		else:
			flash("Invalid Details.Try Again!!!")
			return redirect(url_for('login'))
			
@app.route('/adminpage')
def adminpage():
	name=session['name']
	return render_template('admin.html',name=name)


@app.route('/saveinfo',methods=['GET','POST'])
def saveinfo():
	if request.method=='POST':
		name=request.form.get("name")
		year=request.form.get("year")
		Directedby=request.form.get("Directedby")
		cast=request.form.get("cast")
		genres=request.form.get("genres")
		photoname=request.form.get("photoname")
		filename=request.form.get("filename")
		language=request.form.get("language")
		about=request.form.get("about")
		sql="insert into movies(name,year,Directedby,cast,genres,photoname,filename,language,About) values(%s,%s,%s,%s,%s,%s,%s,%s,%s);"
		mycursor=db.cursor()
		mycursor.execute(sql,(name,year,Directedby,cast,genres,photoname,filename,language,about))
		db.commit()
		flash("Data Inserted Successfully!!!")
		return redirect(url_for('adminpage'))
			

if __name__=='__main__':
	app.run(debug=True)