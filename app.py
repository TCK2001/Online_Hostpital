# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, send_file
import smtplib
import qrcode
from io import BytesIO
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import openai
import tkinter as tk
from tkinter import *
from tkcalendar import Calendar
from PIL import ImageGrab
import datetime

app = Flask(__name__)

# 파일을 불러오는 함수 .
# render_template에서 template은 무조건 현재 페이지에서 templates라는 파일이 있어야 한다, 
# 얘는 이 안에 있는 모든 파일을 읽음.
@app.route('/')
def index():
    return render_template('email.html') 

# /send_email -> 라우터가 처리하는 URL 경로. 
# method는 route 함수를 정의하는데 사용되는 됨.
# HTTP 요청방법 [POST, GET, PUT, DELETE]이 있음.
# 즉 POST 방식의 HTTP의 요청이 오면 send_email을 실행 !
 
@app.route('/send_email', methods=['POST'])
def send_email():
    email_address = 'Your email'                                                # 이메일을 보낼 사람의 이메일.
    email_password = 'Your email password'                                       # 이메일을 보낼 사람의 비밀번호.
                                                                                # 구글의 보안이 강해서,
                                                                                # 앱 비밀번호를 따로 받아야함.
                                                                                # 보안에 들어가면 있음 + 2차 인증 한 계정한에서.           

    # 메일 서버 정보
    mail_server = 'smtp.gmail.com'                                              # gmail의 서버정보.          
    mail_port = 587                                                             # 그냥 고정임.

    # 이메일 정보
    from_address = email_address                                                # 위에서 입력한 보낼 사람의 이메일.
    to_address = request.form['email']                                          # POST 요청으로 얻은 데이터중 email의 필드 값을 얻어오는것.
    
    subject = 'Reservation Result'                                              # 이메일의 제목.
    encoding_subject = subject.encode('utf-8')                                  # 영어나 숫자가 아닐경우 encoding해서 메세지 출력. (굳히 할 필요 X)
    
    body = request.form['message']                                              # 같은 원리 POST 요청으로 얻은 데이터중 message의 필드 값을 얻어오는것.
    encoding_body = body.encode('utf-8')                                        # 내용은 encoding 해줘야함. 영어가 아닐떄가 있어서.

    # QR 코드 생성
    qr = qrcode.QRCode(version=1, box_size=10, border=5)                        # box_size 각각 정사각형의 크기, border 주변 여백의 크기, version 생성된 QR 코드의 버전.
                                                                                # version 1 ~ 40 까지 있고, 버전이 높을 수록 더 많은 데이터를 담을 수 있다.
                                                                                # 하지만 높은 버전의 QR 코드는 인식이 어려울 수가 있음.
                                                                                
    qr.add_data(body)                                                           # 생성한 QR 코드객체에 우리가 입력한 데이터 (body)를 입력함.
    qr.make(fit=True)                                                           # QR 코드를 생성, 
                                                                                # 만약 fit = True일떄는 내용이 어떻던 내용을 전부 담을 수 있게 QR 코드의 사이즈를 자동 설정함.
    img = qr.make_image(fill='black', back_color='white')                       # 함수로 생성된 QR 코드(qr)를 이미지로 변환,
                                                                                # QR 코드의 색상은 검은색으로 하고, 주변 여백의 색상을 흰색으로 함. (우리가 평상시에 보던 QR 코드)
                                                                                
    img_io = BytesIO()                                                          # QR 코드 사진을 저장하기 위해 byte객체를 생성함.
    img.save(img_io, 'PNG')                                                     # 생성한 이미지를 PNG 형태로 byte객체에 저장함.
    img_io.seek(0)                                                              # byte 객체의 파일 포인터를 파일 시작으로 이동시킴, 초기화라고 보면됨.

    # 이메일 보내기
    try:
        # 이메일 서버 연결 설정
        server = smtplib.SMTP(mail_server, mail_port)                           # 서버랑 연결을 합니다 , SMTP 객체 생성, 
                                                                                # mail_server는 서버의 주소,
                                                                                # mail_port는 서버의 포트 번호.
        server.ehlo()                                                           # SMTP 서버와의 연결을 확인함, 성공 or 실패.
        server.starttls()                                                       # SMTP 서버와의 연결을 암호화 하기위해 TLS 연결을 시작함.
        server.ehlo()                                                           # TLS 연결하고 다시한번 연결하여 서버가 TLS 연결을 지원하는지 봄.

        # 이메일 계정 로그인
        server.login(email_address, email_password)

        # 이메일 보내기
        message = f'Subject: {encoding_subject}\n\n{encoding_body}'             # 그냥 간단한 내용 입력.
        server.sendmail(from_address, to_address, message)                      # 이메일 보내기. (보내는 사람, 받는 사람, 내용).

        # QR 코드 파일 첨부해서 이메일 보내기
        attachment = ('qrcode.png', img_io.read(), 'image/png')                 # 위에서 얻은 QR 코드를 다시 불러옴.
        message_with_attachment = MIMEMultipart()                               # MIMEMultipart이라는 객체 생성,
                                                                                # 이메일을 작성 할때 , 텍스트 , 이미지와 같은 첨부파일을 함께 넣을 수 있음.                        
        message_with_attachment.attach(MIMEText(body))                          # 우리가 쓴 message 내용을 담은 MIMEText객체 생성.
        attachment_file = MIMEImage(attachment[1], name=attachment[0])          # 위에서 불러온 첨부 파일을 MIMEImage 객체에 담음.
                                                                                # attachment[1]은 내용, attachment[0]은 사진의 이름.
                                                                                
        message_with_attachment.attach(attachment_file)                         # 위에서 생성한 이미지 객체를 첨부함.
        message_with_attachment['From'] = email_address                         # 이메일의 발신자 주소를 설정함.
        message_with_attachment['To'] = to_address                              # 이메일의 수신자 주소를 설정함.
        message_with_attachment['Subject'] = subject                            # 이메일의 제목을 설정함.

        # SMTP 서버를 이용해 이메일을 보냄, 안에 내용은 (보내는 사람, 수신하는 사람, 그리고 내용).
        # 내용을 string으로 변환하는거 잊지 말기.
        server.sendmail(from_address, to_address, message_with_attachment.as_string())

        # 이메일 보내기 성공 메시지 출력
        print('Email sent successfully !!')

    except Exception as e:
        # 이메일 보내기 실패 메시지 출력
        print(f'Email sending failed: {e}')

    finally:
        # 이메일 서버 연결 종료
        server.quit()

    return 'Warning !'

@app.route('/qrcode')                                                           # 위에 QR 코드를 생성할떄 씀 + 생성 버튼 누를떄 사용됨.
def generate_qrcode():
    body = request.args.get('body', '')                                         # 함수이기에 body 변수 값을 받아옴, 없는 경우 '' 을 사용.
    qr = qrcode.QRCode(version=1, box_size=10, border=5)                        # 위랑 같음.
    qr.add_data(body)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)                                                              # 여기까지 같음.

    return send_file(img_io, mimetype='image/png')                              # 사진의 형태 + PNG 형태를 img_io라는 이름에 넣어 Return.


openai.api_key = "Your openai_api"
messages = []

@app.route('/run_tkinter')   
def ask_ai():
    def aitext():
        user_content = entry.get()
        
        messages.append({"role": "user", "content": f"{user_content}"})

        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

        assistant_content = completion.choices[0].message["content"].strip()

        messages.append({"role": "assistant", "content": f": {assistant_content}"})
        
        label.config(state="normal") 
        label.delete("1.0", "end") 
        label.insert("end", assistant_content) 
        label.config(state="disabled")

    def temp_text(e):
        entry.delete(0,"end")
            
    window = tk.Tk()
    window.geometry("800x400")
    window.title("Minichatgpt by TCK")

    label_frame = tk.Frame(window)
    label_frame.pack(side="top", fill="both", expand=True)

    label_scroll = tk.Scrollbar(label_frame)
    label_scroll.pack(side="right", fill="y")

    label = tk.Text(label_frame, font=("Arial", 14), wrap="word", height=10, width=50, bg="gray", state="disabled", yscrollcommand=label_scroll.set)
    label.pack(side="left", fill="both", expand=True)
    label.config(state="normal") 
    label.delete("1.0", "end") 
    notice = '''[한글]\n버튼을 누르고 좀 기달리시면 원하던 답변이 출력 됩니다. 감사합니다 \n\n[English]\nIf you press the button and wait for a while, the answer you want is printed out. thank you\n\n[中文]\n按完ASK鍵後請稍等一下就會顯示想要的答案在畫面了. 謝謝\n'''
    label.insert("end", notice) 
    label.config(state="disabled")

    label_scroll.config(command=label.yview)

    entry = tk.Entry(window, font=("Arial", 14), width=50)
    entry.insert(0, "Ask something to AI !")
    entry.pack(side="bottom")
    entry.bind("<FocusIn>", temp_text) 

    button = tk.Button(window, text="Ask AI", font=("Arial", 14), command=aitext)
    button.pack(side="bottom")

    window.attributes('-topmost',True) 
    window.mainloop()
    return render_template('email.html')

@app.route('/simple_ask')
def simple():
    def name_del(e):
        name_entry.delete(0,"end")
    def explain_del(e):
        explain_entry.delete("1.0","end") 
    
    # tkinter 윈도우 생성
    window = tk.Tk()
    window.geometry("450x600")  # 창 크기 설정

    # 이름
    name_entry = Entry(window)
    name_entry.insert(0, "Name")
    name_entry.bind("<FocusIn>", name_del)
    
    # 성별 입력
    # radio_var = StringVar()  # 선택된 값을 저장할 변수
    radio_btn1 = Radiobutton(window, text="Man", value="option1")
    radio_btn2 = Radiobutton(window, text="Woman", value="option2")
    # variable=radio_var 이거 쓰면 이상하게 시작때 모든 점이 선택 되어있음.

    name_entry.place(x=0, y=0)
    radio_btn1.place(x=100, y=0)
    radio_btn2.place(x=150, y=0)

    def print_selected_date():
        selected_date = birthday.selection_get()
        calvalue.delete(0, END)  # 입력창 초기화
        calvalue.insert(0, selected_date)  # 선택한 날짜 입력
        
    def clickbirthday():
        btn1.destroy()
        birthday.place(x=0, y=50)
        birthday_button.place(x=220, y=190)
        calvalue.place(x=290, y=195)
        
    def draw(event):
        # Canvas에 선을 그립니다.
        canvas.create_line(event.x, event.y, event.x+1, event.y+1, fill="black")

    def clear_canvas():
        # Canvas에 그려진 그림을 지웁니다.
        canvas.delete("all")
        
    def take_screenshot():
        # 스크린샷 캡처
        image = ImageGrab.grab()
        # 현재 시간을 파일 이름으로 사용
        filename = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S") + " treatment" + ".png"
        # 파일 저장
        image.save(filename)    
    # 생일 버튼
    btn1 = Button(window, text="birthday", command=clickbirthday)
    birthday = Calendar(window, selectmode='day', year=2023, month=4, day=1)
    birthday_button = Button(window, text="Confirm", command=print_selected_date)
    calvalue = Entry(window, width=15)
    btn1.place(x=0, y=50)

    # 설명
    explain_entry = tk.Text(window, width=60, height=10)
    explain_entry.place(x=0, y=220)
    scrollbar = tk.Scrollbar(window)
    explain_entry.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=explain_entry.yview)

    explain_entry.insert("end", "Describe your symptoms")
    explain_entry.bind("<FocusIn>", explain_del)
    explain_entry.place(x=0, y=220)

    # 싸인
    sign_label = Label(window, text="Patient Sign")
    sign_label.place(x=0, y=365)

    canvas = tk.Canvas(window, width=200, height=100, bg="white")
    canvas.place(x=0, y=380)
    canvas.bind("<B1-Motion>", draw)

    clear_button = tk.Button(window, text="Clear", command=clear_canvas)
    clear_button.place(x=205, y=455)
    
    button = tk.Button(window, text="Take Screenshot", command=take_screenshot)
    button.place(x=0, y=480)
    
    window.attributes('-topmost',True) 
    window.mainloop()
    return render_template('email.html')

if __name__ == '__main__':                                                      # 앱의 Main함수.
    app.run()

