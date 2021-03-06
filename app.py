import os
from flask import Flask
from flask import render_template 
from flask import request 
from flask import redirect 
from Models import db
from Models import User
from flask import session 
app = Flask(__name__)

@app.route('/')
def mainpage():
    return render_template('main.html')
    

@app.route('/signup/signup.html', methods=['GET','POST']) #GET(정보보기), POST(정보수정) 메서드 허용
def signup():
    if request.method == "GET":
        return render_template('login.html')#오류확인용
    
    else:
        userid = request.form.get('Uname')
        password = request.form.get('Pass')
        username=request.form.get('name')
        if not(userid and password and username):
            return "입력되지 않은 정보가 있습니다"
        else:
            usertable=User() #user_table 클래스
            usertable.userid = userid
            usertable.username = username
            usertable.password = password
            db.session.add(usertable)
            db.session.commit()
            return redirect('/')

@app.route('/loginpage/Loginpage.html', methods=['GET','POST'])	
def login():
	if request.method=="GET":
		return render_template('signup.html') #오류확인용
	else:
		uid = request.form['Uname']
		passw = request.form['Pass']
		try:
			data = User.query.filter_by(userid=uid, password=passw).first()	# ID/PW 조회Query 실행
			if data is not None:
				session['userid'] = uid	# userid를 session에 저장한다. #오류
				return redirect('/')
			else:
				return 'Dont Login'	# 데이터가 없으면 출력
		except:
			return "dont login"	# 예외 상황 발생 시 출력

@app.route('/logout',  methods=['GET'])
def logout():
	session.pop('userid', None)
	return redirect('/')

if __name__ == "__main__":
    #데이터베이스---------
    basedir = os.path.abspath(os.path.dirname(__file__)) #현재 파일이 있는 디렉토리 절대 경로
    dbfile = os.path.join(basedir, 'db.sqlite') #데이터베이스 파일을 만든다

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True #사용자에게 정보 전달완료하면 teadown. 그 때마다 커밋=DB반영
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #추가 메모리를 사용하므로 꺼둔다
    app.config['SECRET_KEY']='asdfasdfasdfqwerty' #해시값은 임의로 적음

    db.init_app(app) #app설정값 초기화
    db.app = app #Models.py에서 db를 가져와서 db.app에 app을 명시적으로 넣는다
    db.create_all() #DB생성

    app.run(host="127.0.0.1", port=5000, debug=True)