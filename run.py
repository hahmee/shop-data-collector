import sys
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from crawl.shop import WebCrawling as wc
from crawl.kakao import KakaoCrawling as kc
from crawl.sinsang import SinsangCrwaling as sc
from crawl.naver import NaverCrawling as nc

from PyQt5 import QtGui,QtCore
from PyQt5.QtWidgets import QInputDialog,QApplication, QWidget, QListWidget, QLabel, QVBoxLayout
import pickle
import os
import re
import time
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QProcess, QTextCodec
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QApplication, QPlainTextEdit


class All_SetIdPass(QDialog):

    def __init__(self):
        super().__init__()
        
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle('전체 아이디/비번 설정')
        #self.setWindowIcon(QIcon('pengsu.jpg'))
        self.setGeometry(300, 200, 500, 100)

     
        layout = QGridLayout()
        #layout.addStretch(1)#공간 띄기
    
        label_id = QLabel("ID : ")
        font = label_id.font()
        font.setPointSize(13)
        label_id.setFont(font)
        self.label_id = label_id
         
        label_pass = QLabel("Password : ")
        font = label_pass.font()
        font.setPointSize(13)
        label_pass.setFont(font)
        self.label_pass = label_pass
        
        label_id_input= QLineEdit()
        label_id_input = QLineEdit()
        label_pass_input  = QLineEdit()
        label_pass_input.setEchoMode(QLineEdit.Password)#패스워드로 설정        
        

        #딕셔너리에 통합id/pw 있는지 확인 - > index = 3
        try: 
            file = open('IdPw.txt', 'rb')
            
        except FileNotFoundError as e :
            #파일 생성
            file = open("IdPw.txt", 'w', encoding='UTF8')
            file.close()
            file = open('IdPw.txt', 'rb')

                    
        try:
            a= pickle.load(file) #
            
        except EOFError: # file이 비었을때
            a={}
            
        if(3 in a): #index 3의 값이 scores 딕셔너리안에 있다면
            #print(a[3][0])
            label_id_input.setText(a[3][1])
            label_pass_input.setText(a[3][2])       

#
        
        font = label_id_input.font()
        font.setPointSize(13)
        label_id_input.setFont(font)
        self.label_id_input = label_id_input

    
      
        font = label_pass_input.font()
        font.setPointSize(13)
        label_pass_input.setFont(font)
        self.label_pass_input = label_pass_input
        
 
        subLayout = QHBoxLayout()
        
        btnOK = QPushButton("저장")
        font = btnOK.font()
        font.setPointSize(11)
        btnOK.setFont(font)
        btnOK.clicked.connect(self.onOKButtonClicked)
 
        btnCancel = QPushButton("취소")
        font = btnCancel.font()
        font.setPointSize(11)
        btnCancel.setFont(font)        
        btnCancel.clicked.connect(self.onCancelButtonClicked)

     
        layout.addWidget(label_id_input,0,1)
        layout.addWidget(label_pass_input,1,1)
        layout.addWidget(label_id,0,0)
        layout.addWidget(label_pass,1,0)

        #layout.addStretch(1)
        subLayout.addWidget(btnOK)
        subLayout.addWidget(btnCancel)
        
        layout.addLayout(subLayout,2,0,2,2) # grid인 layout에 sublayout을 추가시킴 
        
        layout.setRowStretch(2,10)
 
        self.setLayout(layout)
#


    def onOKButtonClicked(self): # 저장할때 파일 쓰기 
        #self.accept()
        label_id_input = self.label_id_input.text().strip()
        label_pass_input = self.label_pass_input.text().strip()

        if label_id_input =="" or label_pass_input== "" :
            print('빈칸입니다. 다시 해주세요')#빈칸입니다. 알림
            QMessageBox.about(self, "warning", "빈칸입니다. 다시 해주세요")#바로 실행 

        else: #빈칸 아니면
            ##첨부터 IdPw.txt에 걍 쓰게하기 *리셋
            
                     
            f = open("./shops.txt", 'r',  encoding='UTF8')
            data = f.read().strip().split('\n')
            f.close()
            data_len = int(len(data)/2)
            
            #길이 알아내고
            #0 1 2 가 있다면 저장해두기 

            scores = {}
            
            #인덱스3은 지정 해주기 
            scores[3] = ['통합idpw',label_id_input,label_pass_input]
            

           # scores[self.index] = value_list
            
            
            for i in range(data_len):#2개가 있음 0 1
               
                value_list = []
                value_list.append(data[i*2])#가우디 0 2
                value_list.append(label_id_input)#통합 아이디 
                value_list.append(label_pass_input)#통합 비번
            
                scores[i+4] = value_list
                
                
                
                #print(scores) #이 scores를 이제 james.txt 파일을 열어서 쓰기


            
            #print(a)
            #통합 아이디 있는지 확인 index->3
            
            

            
                    
            for i in range(data_len):
                
                #wb면 첨부터 다시 쓰는 거니까.. 가가오스토리, 신상맠[ㅅ, 네이버는 저장해두기 
                with open('IdPw.txt', 'wb') as file:    # james.p 파일을 바이너리 쓰기 추가 모드(ab)로 열기
                    pickle.dump(scores, file) #딕셔너리 저장

            
                

            
                    
                    


                
            
    

            
        
            
            
            
            print('아이디/비밀번호가 완료되었습니다.')
            QMessageBox.about(self, "message", "아이디/비밀번호가 완료되었습니다.")#바로 실행
            
            self.accept()
            
    def onCancelButtonClicked(self):
        self.reject()
 
     
 
    def showModal(self):
        return super().exec_()
    

class SetIdPass2(QDialog):

    def __init__(self,shop):
        super().__init__()
      
        self.shop = shop
       
        data = MyTabWidget.shops_file_open(self)
        
        try:
            index = data.index(shop)# shops.txt에서 index 찾기(4,5,6,7,8,9,10...)
            #(0,2,4,6)-->(4,5,6,7,8,),(0,1,2,3,4)
        
        except ValueError: # 해당 text가 shops에 없다면
            print('shops.txt에 해당 거래처가 없습니다.')
            print('다시 실행해주세요')
            index = 0 #...?
            
    
       
        #/2를 한 후 +4
        #index/2
        self.index = int(index/2+4)
        #print(self.index)#2 -->5 
        #index +=4

        
        
            

        self.initUI()
 
    def initUI(self):
        self.setWindowTitle('{} 아이디/비번 설정'.format(self.shop))
        self.setGeometry(300, 200, 500, 100)
       

        
     
        layout = QGridLayout()    
        label_id = QLabel("ID : ")
        font = label_id.font()
        font.setPointSize(13)
        label_id.setFont(font)
        self.label_id = label_id
        
        label_pass = QLabel("Password : ")
        font = label_pass.font()
        font.setPointSize(13)
        label_pass.setFont(font)
        self.label_pass = label_pass
        
        label_id_input= QLineEdit()
        label_id_input = QLineEdit()
        label_pass_input  = QLineEdit()
        label_pass_input.setEchoMode(QLineEdit.Password)#패스워드로 설정 


        #딕셔너리의 해당 key 가 안에 있는지 조사
        try: 
            file = open('IdPw.txt', 'rb')
        except FileNotFoundError as e :
            #파일 생성
            file = open("IdPw.txt", 'w')
            file.close()
            file = open('IdPw.txt', 'rb')
            
            
        #else:
            
        try:
            scores= pickle.load(file) #딕셔너리 저장
            print(scores)
            
                
        except EOFError: # 더 이상 로드 할 데이터가 없으면 
             scores={}
             
        

            
                 

        if(self.index in scores): #index 값이 scores 딕셔너리안에 있다면 
            
            
            label_id_input.setText(scores[self.index][1])
            label_pass_input.setText(scores[self.index][2])


            
        

        
        font = label_id_input.font()
        font.setPointSize(13)
        label_id_input.setFont(font)
        self.label_id_input = label_id_input

    
      
        font = label_pass_input.font()
        font.setPointSize(13)
        label_pass_input.setFont(font)
        self.label_pass_input = label_pass_input
        
 
        subLayout = QHBoxLayout()
        
        btnOK = QPushButton("저장")
        font = btnOK.font()
        font.setPointSize(11)
        btnOK.setFont(font)
        btnOK.clicked.connect(self.onOKButtonClicked)
 
        btnCancel = QPushButton("취소")
        font = btnCancel.font()
        font.setPointSize(11)
        btnCancel.setFont(font)        
        btnCancel.clicked.connect(self.onCancelButtonClicked)

     
        layout.addWidget(label_id_input,0,1)
        layout.addWidget(label_pass_input,1,1)
        layout.addWidget(label_id,0,0)
        layout.addWidget(label_pass,1,0)

        #layout.addStretch(1)
        subLayout.addWidget(btnOK)
        subLayout.addWidget(btnCancel)
        
        layout.addLayout(subLayout,2,0,2,2) # grid인 layout에 sublayout을 추가시킴 
        
        layout.setRowStretch(2,10)
 
        self.setLayout(layout)
     
    def onOKButtonClicked(self): # 저장할때 파일 쓰기 
        #self.accept()
        label_id_input = self.label_id_input.text().strip()
        label_pass_input = self.label_pass_input.text().strip()

        if label_id_input =="" or label_pass_input== "" :
            print('빈칸입니다. 다시 해주세요')#빈칸입니다. 알림
            QMessageBox.about(self, "warning", "빈칸입니다. 다시 해주세요")#바로 실행 

        else: #빈칸 아니면 
            
            scores = {} #ex) {0:["가우디","아이디","비번"]}


            value_list = []
            value_list.append(self.shop)#가우디
            value_list.append(label_id_input)#아이디
            value_list.append(label_pass_input)#비번
           
            scores[self.index] = value_list 

            
            #한번 열고
            
            with open('IdPw.txt', 'rb') as file:    # james.p 파일을 바이너리 쓰기 추가 모드(ab)로 열기
                try:
                    a= pickle.load(file) #딕셔너리 저장
                    
                except EOFError: # file이 비었을때
                    a={}
            
                
                
            
            
            a.update(scores)#다시 딕셔너리 병합 --> key 값이 같으면 맨 마지막에 들어온게 저장됨 
            
            
            #다시 써야함 

            with open('IdPw.txt', 'wb') as file:    # james.p 파일을 바이너리 쓰기 추가 모드(ab)로 열기
                pickle.dump(a, file) #딕셔너리 저장
                
                #{4: ['라임', 'qq', 'qq'], 5:['뇨뇨','tt','zz']}
                
                
            
        
            
            
            
            print('아이디/비밀번호가 완료되었습니다.')
            QMessageBox.about(self, "message", "아이디/비밀번호가 완료되었습니다.")#바로 실행
            
            self.accept()
            
    def onCancelButtonClicked(self):
        self.reject()
 
    def showModal(self):
        return super().exec_()
    
class SetIdPass(QDialog):

    def __init__(self,index,shop):
        super().__init__()
        self.index = index
        self.shop = shop
        
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle('{} 아이디/비번 설정'.format(self.shop))
        self.setGeometry(300, 200, 500, 100)

        #원래 저장된 아이디와 비번 파일 읽기 
        #f = open("./idpassword.txt", 'r',  encoding='UTF8')
        #self.primary_key = f.readline()    # 3줄씩 읽고 프라이머리 키 획득

        #처음과 뒤에 띄어쓰기나 공백 문자 제거 
        #lines = f.read().strip().split('\n') # 리스트 ["0","가우디","ASDFAAAAA","ASDFASDF",3,"디스티","아이이이","비비비비"]
        
        
        #print(lines)
        #f.close()
       

        
     
        layout = QGridLayout()
        #layout.addStretch(1)#공간 띄기
    
        label_id = QLabel("ID : ")
        font = label_id.font()
        font.setPointSize(13)
        label_id.setFont(font)
        self.label_id = label_id
        
        label_pass = QLabel("Password : ")
        font = label_pass.font()
        font.setPointSize(13)
        label_pass.setFont(font)
        self.label_pass = label_pass
        
        label_id_input= QLineEdit()
        label_id_input = QLineEdit()
        label_pass_input  = QLineEdit()
        label_pass_input.setEchoMode(QLineEdit.Password)#패스워드로 설정 


        #딕셔너리의 해당 key 가 안에 있는지 조사
        try: 
            file = open('IdPw.txt', 'rb')
        except FileNotFoundError as e :
            #파일 생성
            file = open("IdPw.txt", 'w',encoding='UTF8')
            file.close()
            file = open('IdPw.txt', 'rb')
            
            
        #else:
            
        try:
            scores= pickle.load(file) #딕셔너리 저장
            print(scores)
            
                
        except EOFError: # 더 이상 로드 할 데이터가 없으면 
             scores={}
             
        

            
                 

        if(self.index in scores): #index 값이 scores 딕셔너리안에 있다면 
            
            
            label_id_input.setText(scores[self.index][1])
            label_pass_input.setText(scores[self.index][2])


            
        

        
        font = label_id_input.font()
        font.setPointSize(13)
        label_id_input.setFont(font)
        self.label_id_input = label_id_input

    
      
        font = label_pass_input.font()
        font.setPointSize(13)
        label_pass_input.setFont(font)
        self.label_pass_input = label_pass_input
        
 
        subLayout = QHBoxLayout()
        
        btnOK = QPushButton("저장")
        font = btnOK.font()
        font.setPointSize(11)
        btnOK.setFont(font)
        btnOK.clicked.connect(self.onOKButtonClicked)
 
        btnCancel = QPushButton("취소")
        font = btnCancel.font()
        font.setPointSize(11)
        btnCancel.setFont(font)        
        btnCancel.clicked.connect(self.onCancelButtonClicked)

     
        layout.addWidget(label_id_input,0,1)
        layout.addWidget(label_pass_input,1,1)
        layout.addWidget(label_id,0,0)
        layout.addWidget(label_pass,1,0)

        #layout.addStretch(1)
        subLayout.addWidget(btnOK)
        subLayout.addWidget(btnCancel)
        
        layout.addLayout(subLayout,2,0,2,2) # grid인 layout에 sublayout을 추가시킴 
        
        layout.setRowStretch(2,10)
 
        self.setLayout(layout)
     
    def onOKButtonClicked(self): # 저장할때 파일 쓰기 
        #self.accept()
        label_id_input = self.label_id_input.text().strip()
        label_pass_input = self.label_pass_input.text().strip()

        if label_id_input =="" or label_pass_input== "" :
            print('빈칸입니다. 다시 해주세요')#빈칸입니다. 알림
            QMessageBox.about(self, "warning", "빈칸입니다. 다시 해주세요")#바로 실행 

        else: #빈칸 아니면 
            
            scores = {} #ex) {0:["가우디","아이디","비번"]}


            value_list = []
            value_list.append(self.shop)#가우디
            value_list.append(label_id_input)#아이디
            value_list.append(label_pass_input)#비번
           
            scores[self.index] = value_list 

            
            #한번 열고
            
            with open('IdPw.txt', 'rb') as file:    # james.p 파일을 바이너리 쓰기 추가 모드(ab)로 열기
                try:
                    a= pickle.load(file) #딕셔너리 저장
                    
                except EOFError: # file이 비었을때
                    a={}
            
                
                
            
            
            a.update(scores)#다시 딕셔너리 병합 --> key 값이 같으면 맨 마지막에 들어온게 저장됨 
            
            
            #다시 써야함 

            with open('IdPw.txt', 'wb') as file:    # james.p 파일을 바이너리 쓰기 추가 모드(ab)로 열기
                pickle.dump(a, file) #딕셔너리 저장
                
                #{4: ['라임', 'qq', 'qq'], 5:['뇨뇨','tt','zz']}
                
                
            
        
            
            
            
            print('아이디/비밀번호가 완료되었습니다.')
            QMessageBox.about(self, "message", "아이디/비밀번호가 완료되었습니다.")#바로 실행
            
            self.accept()
            
    def onCancelButtonClicked(self):
        self.reject()
 
    def showModal(self):
        return super().exec_()
    

#거래처 수정 
class SubWindow2(QDialog):
    
    def __init__(self, item):
        super().__init__()
        self.item = item   
        self.data = MyTabWidget.shops_file_open(self)
    
        try:
            self.index = self.data.index(self.item)#shops.txt에서 index 찾기
            self.url = self.data[self.index+1]

        
        except ValueError: # 해당 text가 shops에 없다면
            print('shops.txt에 해당 거래처가 없습니다.')
            print('다시 실행해주세요')
            self.index =0 #???
            self.url = ""


        self.initUI()
           
    def initUI(self):
        
        self.setWindowTitle('{0} 거래처 수정'.format(self.item))
        self.setGeometry(100, 100, 500, 100)
        
        layout = QGridLayout()



        client_name = QLabel("거래처 이름 : ")
        font = client_name.font()
        font.setPointSize(13)
        client_name.setFont(font)
        self.client_name = client_name
        
        client_url = QLabel("거래처 url : ")
        font = client_url.font()
        font.setPointSize(13)
        client_url.setFont(font)
        self.client_url = client_url

        
 
        client_name_input = QLineEdit()
        font = client_name_input.font()
        font.setPointSize(13)
        client_name_input.setFont(font)
        client_name_input.setText(self.item)
        self.client_name_input = client_name_input 


    
        client_url_input  = QLineEdit()
        font = client_url_input.font()
        font.setPointSize(13)
        client_url_input.setFont(font)
        client_url_input.setText(self.url)#파일을 읽고 
        self.client_url_input = client_url_input
        
 
        subLayout = QHBoxLayout()
        
        btnOK = QPushButton("저장")
        btnOK.clicked.connect(self.onOKButtonClicked)
 
        btnCancel = QPushButton("취소")
        btnCancel.clicked.connect(self.onCancelButtonClicked)

     
        layout.addWidget(client_name_input,0,1)
        layout.addWidget(client_url_input,1,1)
        layout.addWidget(client_name,0,0)
        layout.addWidget(client_url,1,0)
        subLayout.addWidget(btnOK)
        subLayout.addWidget(btnCancel)
        
        
        layout.addLayout(subLayout,2,0,2,2) # grid인 layout에 sublayout을 추가시킴 
        #layout.addStretch(1)
        layout.setRowStretch(2,10)
 
        self.setLayout(layout)
 
    def onOKButtonClicked(self):

        client_name_input = self.client_name_input.text().strip()
        client_url_input = self.client_url_input.text().strip()
        
        def check_joongbok():
            #수정 시, 있는 상점이면 경고 창
            #자신의 것을 제외하고,
            for i in range(0,len(self.data),2): # 0 2 4 6 
                
                if ((i != self.index) and (self.data[i] == client_name_input)):
                    print('이름이 중복되었어요..수정할 수 없습니다.')
                    QMessageBox.about(self, "warning", "이름이 중복되었어요..수정할 수 없습니다.")#바로 실행 
                    return True
                else:
                    pass

            return False

        if client_name_input =="" or client_url_input== "" :
            print('빈칸입니다. 다시 해주세요')#빈칸입니다. 알림
            QMessageBox.about(self, "warning", "빈칸입니다. 다시 해주세요")#바로 실행 

        else: #빈칸 아니면 
            #있는 상점인지 확인하고
            if not check_joongbok(): #중복 아냐 
                # w모드로 고쳐서 다시 쓰기
                
                self.data[self.index] = client_name_input
                self.data[(self.index+1)] = client_url_input
                
                #self.data리스트 다시 쓰기
                f = open('./shops.txt', 'w', encoding='UTF8')
                f.seek(0)
                f.write('\n'.join(self.data))
                f.close()
                print('거래처 정보가 수정되었습니다.')
                QMessageBox.about(self, "message", "거래처 정보가 수정되었습니다.")#바로 실행
                self.accept()
            
    def onCancelButtonClicked(self):
        self.reject()

    
    
    def showModal(self):
        return super().exec_()





#거래처 추가 
class SubWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        
        self.setWindowTitle('거래처 추가')
        self.setGeometry(350, 300, 500, 100)#중간에 뜨게 하기 
 
        layout = QGridLayout()



        client_name = QLabel("거래처 이름 : ")
        font = client_name.font()
        font.setPointSize(13)
        client_name.setFont(font)
        self.client_name = client_name
        
        client_url = QLabel("거래처 url : ")
        font = client_url.font()
        font.setPointSize(13)
        client_url.setFont(font)
        self.client_url = client_url

        
 
        client_name_input = QLineEdit()
        font = client_name_input.font()
        font.setPointSize(13)
        client_name_input.setFont(font)
        self.client_name_input = client_name_input

    
        client_url_input  = QLineEdit()
        font = client_url_input.font()
        font.setPointSize(13)
        client_url_input.setFont(font)
        self.client_url_input = client_url_input
        
 
        subLayout = QHBoxLayout()
        
        btnOK = QPushButton("저장")
        btnOK.clicked.connect(self.onOKButtonClicked)
 
        btnCancel = QPushButton("취소")
        btnCancel.clicked.connect(self.onCancelButtonClicked)

     
        layout.addWidget(client_name_input,0,1)
        layout.addWidget(client_url_input,1,1)
        layout.addWidget(client_name,0,0)
        layout.addWidget(client_url,1,0)
        #layout.addWidget(btnOK,2,0)
        #layout.addWidget(btnCancel,2,1)
        subLayout.addWidget(btnOK)
        subLayout.addWidget(btnCancel)
        
        
        layout.addLayout(subLayout,2,0,2,2) # grid인 layout에 sublayout을 추가시킴 
        #layout.addStretch(1)
        layout.setRowStretch(2,10)
 
        self.setLayout(layout)
 
    def onOKButtonClicked(self):

        client_name_input = self.client_name_input.text().strip()
        client_url_input = self.client_url_input.text().strip()

        if client_name_input =="" or client_url_input== "" :
            print('빈칸입니다. 다시 해주세요')#빈칸입니다. 알림
            QMessageBox.about(self, "warning", "빈칸입니다. 다시 해주세요")#바로 실행 

        else:
            data = MyTabWidget.shops_file_open(self)
            data_len = len(data)
            joongbok = False
            
            for d in data:
                
                if d == client_name_input:
                    print("중복됨")
                    joongbok = True
                    break
                    
            if joongbok:
                #중복 저장 방지 
                #가우디있다면 가우디(1)로 저장.
                chk=0
                r = re.compile("{}[(][0-9]+[)]$".format(client_name_input)) # 가우디(1)가우디(2)
                for i in data:
                    m = r.search(i)
                    if m:
                        chk+=1 

                if(chk>0):
                    client_name_input = "{0}({1})".format(client_name_input,chk+1).strip()

                else:
                    client_name_input = "{0}({1})".format(client_name_input,1).strip()               
                
                print('\'{0}\'로 저장되었습니다.'.format(client_name_input))
                QMessageBox.about(self, "message", client_name_input+"로 저장되었습니다.")#바로 실행

            
        
            
           
            f = open('./shops.txt', 'a', encoding='UTF8')
            #커서가 enter해서 다음줄로 오도록
            f.seek(0)
            f.write("\n"+client_name_input)
            f.write("\n"+client_url_input)
            f.close()
            print('새로운 거래처가 추가되었습니다.')
            
            QMessageBox.about(self, "message", "새로운 거래처가 추가되었습니다.")#바로 실행


            data = MyTabWidget.shops_file_open(self)           
            self.name_new = data[len(data)-2]

            self.accept()
            
    def onCancelButtonClicked(self):
        self.reject()
 
    def showModal(self):
        return super().exec_()


            
               
    
class Addclient(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        self.setGeometry(500,200,300, 100)
        self.setWindowTitle('거래처 추가')
        
        self.client_name = QLabel("거래처 이름 : ")
        self.client_name_input  = QLineEdit()
        self.client_url = QLabel("거래처 url : ")
        self.client_url_input  = QLineEdit()
        self.pushButton = QPushButton("저장")
        
        self.layout = QGridLayout()
        self.layout.addWidget(self.client_name,0,0)
        self.layout.addWidget(self.client_name_input,0,1)
        self.layout.addWidget(self.client_url,1,0)
        self.layout.addWidget(self.client_url_input,1,1)
        self.layout.addWidget(self.pushButton,2,1)
        
        self.setLayout(self.layout)
        self.pushButton.clicked.connect(self.saving2)
        
        self.show()
        
    def saving2(self):
        
        client_name_input = self.client_name_input.text().strip()
        client_url_input = self.client_url_input.text().strip()

        if client_name_input =="" or client_url_input== "" :
            print('빈칸입니다. 다시 해주세요')#빈칸입니다. 알림
            QMessageBox.about(self, "warning", "빈칸입니다. 다시 해주세요")#바로 실행 

        else: #빈칸 아니면 
            #a모드로 글 추가
            f = open('./shops.txt', 'a', encoding='UTF8')
            f.seek(0)
            f.write("\n"+client_name_input)
            f.write("\n"+client_url_input)
            f.close()
            print('새로운 거래처가 추가되었습니다.')
            QMessageBox.about(self, "message", "새로운 거래처가 추가되었습니다.")#바로 실행



            #밑에도 추가되게
            #MyTabWidget.chuga()
        
            

            #self.a = MyTabWidget(self)
            #self.setCentralWidget()#생성자 접근
            #print(self.a.result)
            #self.a = MyTabWidget(self)
            #print(self.a.result)


        
     
            
            
        
class App(QMainWindow):

    def __init__(self):
        super().__init__()

        #UI
        self.setGeometry(300,100,750, 700) #(x좌표, y좌표, 윈도우 폭, 윈도우 높)

        self.tab_widget = MyTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        self.show()

        
    
        
        

        
class MyTabWidget(QWidget):
    
    #try: 
    #    f = open('./download_path.txt', 'r',  encoding='UTF8')
    
    #except FileNotFoundError as e :
        #파일 생성
    #    f = open("./download_path.txt", 'w',  encoding='UTF8')
    #    f.close()
    #    f = open('./download_path.txt',  'r',  encoding='UTF8')

    #f = open("./download_path.txt", 'r',  encoding='UTF8')
    #path = f.readline()       #path -> 전역변수  파일의 첫 번째 줄을 읽어  
    #f.close()




                
    def __init__(self, parent, proList= None):#생성자
    
    
        super(QWidget, self).__init__(parent)
        self.layout = QHBoxLayout()#전체 레이아웃을 수평으로 
        dt = str(datetime.today()).split(' ')[0]
        # path = 'C:\\Users\\hkchoi\\Desktop\\쇼핑몰\\00_제품사진\\1_의류\\'
        # path = "C:\\Users\\Seoyoung\\Downloads\\"
        # path = "D:\\이연주"
        #개별 설정
        
        
        #path = "..\\" + dt + '\\' #오늘날짜로 초기설정 

        
        
     
        #shops.txt.가 없다면 만들기
        if not (os.path.isfile("./shops.txt")):
            f = open("shops.txt", 'w', encoding='UTF8')
            f.close()
            
        #생김 
        f = open("./shops.txt", 'r',  encoding='UTF8')
        data = f.read().strip().split('\n')
        f.close()

        
        #리스트로 가나다라 정렬


        #튜
        shopes = {}
        #튜플-리스트 만들기 

        #정렬하기 전에 고유의 index 값 설정해주기
        index = 0
        for i in range(len(data)):
            if len(data)>= 2 and i%2 == 0:
                shopes[data[i]] = [data[i+1],index] #딕셔너리 만드는 과정
                index+=1

        #전체 shop 개수 
        self.shop_number = index

                
        
            

        #print(shopes)
        #가나다라마바사- 정렬 
        sorted_shopes = sorted(shopes.items())

        

        
        # Initialize tab screen
        #self.result =QTextEdit(readOnly=True) # 결과 보여주는 창 
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs = QTabWidget()
        
        
        # create connection
        #self.result.returnPressed.connect(self.run_command)        

        #전체 글자 크기 확대 
        font1 = self.tabs.font()
        font1.setPointSize(13)
        #font1.setBold(True)
        self.tabs.setFont(font1)
        #탭 사이즈 다시
    
        # Add tabs
        self.tabs.addTab(self.tab1, "거래처")
        self.tabs.addTab(self.tab2, "기타")


        
        # Create first tab
        #tab1의 레이아웃은 수직 레이아웃 
        self.tab1.layout = QVBoxLayout(self) # 수직레이아웃  
        
        #Scrollbar
        #self.download_url = QLineEdit()


        self.groupbox1 = QGroupBox("다운로드 경로 지정")
      # self.groupbox1.l1 = QLable("다운로드 경로 지정")
        self.gbox = QGridLayout()
        
        

        self.groupbox1.setLayout(self.gbox) #groupbox1를 그리드 레이아웃으로 설정 
        
       # self.l1 = QLabel('다운로드 경로 지정', self) #이미지나 텍스트 출
       # self.l1.setText('다운로드 경로 지정')
      

        #self.gbox2.addWidget(QCheckBox("check box #1"))
        #self.gbox2.addWidget(QCheckBox("check box #2"))
        #self.gbox2.addWidget(QCheckBox("check box #3"))
       
                
        #self.l1 = QLabel("다운로드 경로 지정",self)
        self.NormalPath = QLineEdit()
        self.normal_path = self.set_path("./download_path.txt","거래처")
        self.NormalPath.setText(self.normal_path)
        self.load = QPushButton('경로')
        self.save = QPushButton('저장') # 저장버튼 누름
        

        
        
       # self.gbox.addWidget(self.l1, 0, 0) 
        self.gbox.addWidget(self.NormalPath, 1, 0)        
        self.gbox.addWidget(self.load, 1, 1)        
        self.gbox.addWidget(self.save, 1, 2) 

        #self.shop_number=0
        
        #self.l2 = QLabel('전체 쇼핑몰 ({}개)'.format('zzz'), self) #이미지나 텍스트 출
        
        #fileButton1 = QPushButton('쇼핑몰 추가',self)
        #fileButton1.resize(50,50)
          
        #self.gbox2.addWidget(self.l2)
        #self.gbox2.addWidget(self.l3)
        #self.gbox2.addWidget(fileButton1)
        
        self.tab1.layout.addWidget(self.groupbox1)#탭1에 groupbox1을 넣자
        #self.tab1.layout.addWidget(self.groupbox5)
        #self.tab1.layout.addWidget(self.groupbox2)
        
            
        #self.tab1.layout.addWidget(self.l2)
        #self.tab1.layout.addWidget(self.fileButton1)
        ####시작
        
        
        #self.tab1.layout.addWidget(self.buttoncool2,21,2)
        
        
        

        self.ccc = QHBoxLayout() # 수평레이아웃

        
        self.che = QLabel('전체 거래처 ({}개)'.format(self.shop_number), self)
        self.ccc.addWidget(self.che)
     #   self.ccc.addStretch(0)
       # self.ccc.addSpacing(15)
        self.AddButton = QPushButton('거래처 추가')

        if sorted_shopes:
            self.tong_button = QPushButton('전체 ID/PW 설정')
            self.tong_button.clicked.connect(self.all_setIdPassword)
            self.ccc.addWidget(self.tong_button)

        self.ccc.addWidget(self.AddButton)
        self.tab1.layout.addLayout(self.ccc)
        

        font = QtGui.QFont()
        font.setPointSize(13)
        
        self.list = QListWidget()
                
        self.list.setFont(font)
        #self.list.setFont(QtGui.QFont("Sanserif",13))
        
        if proList is not None:
            self.list.addItems(proList)
            self.list.setCurrentRow(0)
            
        vbox= QVBoxLayout()
        for text, slot in (("추가", self.addClient),
                           ("수정", self.editClient),
                           ("삭제", self.remove),
                           ("Crawl", self.pageCrawling2),
                           ("ID/PW", self.setIdPassword2),
                           ("정렬", self.sort)):

            button= QPushButton(text)
 
            vbox.addWidget(button)
            button.clicked.connect(slot)            
        #리스트 포문
        num=0
        hbox = QHBoxLayout()
        for i in sorted_shopes: # 리스트안에 있는 튜플 
            key = i[0] # 가우디
            value = i[1][0] # url
            index = i[1][1] # index
            
            self.list.insertItem(num, key)
        

            num+=1
            index+=1
            
        self.list.clicked.connect(self.listview_clicked)
        
        #vbox.addWidget(self.list)

        
        hbox.addWidget(self.list)
        hbox.addLayout(vbox)
        self.tab1.layout.addLayout(hbox)


        
        
        #self.tab1.layout.addWidget(self.list)

       
        self.label = QLabel()
        self.label2 = QLabel()
        self.label.setFont(QtGui.QFont("Sanserif", 14))
        self.label2.setFont(QtGui.QFont("Sanserif", 14))
        self.tab1.layout.addWidget(self.label)
        self.tab1.layout.addWidget(self.label2)


        ##이미지 상황 보여주는 

        
        
        ####끝
        #tab1 layout set
        
        self.tab1.setLayout(self.tab1.layout)

        
        #Create second tab
        self.tab2.layout = QVBoxLayout(self)

        
        
        #카카오
        self.groupbox1 = QGroupBox("카카오스토리")
        self.gbox = QGridLayout()
        
        self.groupbox1.setLayout(self.gbox)

        self.l1 = QLabel()
        self.l1.setText('url')
        self.l1.setAlignment(Qt.AlignCenter)

        self.kakaoUrl = QLineEdit()
        self.gbox.addWidget(self.l1, 1, 0)
        self.gbox.addWidget(self.kakaoUrl, 1, 1)

        self.l2 = QLabel()
        self.l2.setText('다운로드')
        self.l2.setAlignment(Qt.AlignCenter)
        self.kakaoPath = QLineEdit()
        self.kakao_path = self.set_path("./download_path.txt","카카오스토리")
        self.kakaoPath.setText(self.kakao_path)

        self.fileButton1 = QPushButton('경로')
        self.saveButton1 = QPushButton('저장')

       
        self.gbox.addWidget(self.l2, 0, 0)
        self.gbox.addWidget(self.kakaoPath, 0, 1)
        self.gbox.addWidget(self.saveButton1, 0, 3)
        self.gbox.addWidget(self.fileButton1, 0, 2)
       
        self.kakaoButton = QPushButton('Crawl')
        self.pwid =QPushButton('ID/PW')
        self.gbox.addWidget(self.kakaoButton,1,3)
        self.gbox.addWidget(self.pwid, 1,2)
        #print(self.shop_number)
        #얘네를 index를 0 1 2 3 4
        self.pwid.clicked.connect(lambda state,index=0, shop="카카오스토리" : self.setIdPassword(index,shop))
        #{19: ['카카오스토리','ㅂㅂ','ㅇㅇ']}
        self.saveButton1.clicked.connect(lambda state, number =2 : self.saving(number))
        
        
        # 신상마켓
        self.groupbox2 = QGroupBox("신상마켓")
        self.gbox = QGridLayout()
        
        self.groupbox2.setLayout(self.gbox)

        self.l3 = QLabel()
        self.l3.setText('url')
        self.l3.setAlignment(Qt.AlignCenter)
        
        self.sinsangUrl = QLineEdit()
        self.gbox.addWidget(self.l3, 1, 0)
        self.gbox.addWidget(self.sinsangUrl, 1, 1)

        self.l8 = QLabel()
        self.l8.setText('다운로드')
        self.l8.setAlignment(Qt.AlignCenter)   
        self.sinsangPath = QLineEdit()
        self.sinsang_path = self.set_path("./download_path.txt","신상마켓")
        self.sinsangPath.setText(self.sinsang_path)

        self.fileButton4 = QPushButton('경로')
        self.saveButton4 = QPushButton('저장')
       
        self.gbox.addWidget(self.l8, 0, 0)
        self.gbox.addWidget(self.sinsangPath, 0, 1)
        self.gbox.addWidget(self.saveButton4, 0, 3)
        self.gbox.addWidget(self.fileButton4, 0, 2)

        self.sinsangButton = QPushButton('Crawl')
        self.pwid2 =QPushButton('ID/PW')
        self.gbox.addWidget(self.sinsangButton, 1,3)
        self.gbox.addWidget(self.pwid2, 1,2)
        self.pwid2.clicked.connect(lambda state,index=1, shop="신상마켓" : self.setIdPassword(index,shop))
        self.saveButton4.clicked.connect(lambda state, number =3 : self.saving(number))


        # 네이버 블로그
        self.groupbox4 = QGroupBox("네이버 블로그")
        self.gbox = QGridLayout()
        
        self.groupbox4.setLayout(self.gbox)

        self.l4 = QLabel()
        self.l4.setText('url')
        self.l4.setAlignment(Qt.AlignCenter)
        
        self.blogUrl = QLineEdit()
        self.gbox.addWidget(self.l4, 1, 0)
        self.gbox.addWidget(self.blogUrl, 1, 1)

        self.l5 = QLabel()
        self.l5.setText('다운로드')
        self.l2.setAlignment(Qt.AlignCenter)        
        self.blogPath = QLineEdit()
        self.blog_path = self.set_path("./download_path.txt","네이버 블로그")
        self.blogPath.setText(self.blog_path)

        self.fileButton2 = QPushButton('경로')
        self.saveButton2 = QPushButton('저장')        
       
        self.gbox.addWidget(self.l5, 0, 0)
        self.gbox.addWidget(self.blogPath, 0, 1)
        self.gbox.addWidget(self.saveButton2, 0, 3)
        self.gbox.addWidget(self.fileButton2, 0, 2)
        
        self.blogButton = QPushButton('Crawl')
        #self.pwid4 =QPushButton('ID/PW')
        self.gbox.addWidget(self.blogButton, 1,2,1,2)
        #self.gbox.addWidget(self.pwid4, 1,2)
        #self.pwid4.clicked.connect(lambda state,index=3, shop="네이버 블로그" : self.setIdPassword(index,shop))        
        self.saveButton2.clicked.connect(lambda state, number =5 : self.saving(number))

        #네이버 카페
        self.groupbox3 = QGroupBox("네이버 카페(미엘르)")
        self.gbox = QGridLayout()
        
        self.groupbox3.setLayout(self.gbox)

        self.l6 = QLabel()
        self.l6.setText('page')
        self.l6.setAlignment(Qt.AlignCenter)
        self.cafePage = QLineEdit()
        self.cafePage.setPlaceholderText("원하는 url를 입력해주세요.")

        #radio 버튼
        self.grp_1  = QGroupBox()

        
        self.grp_1_layout = QVBoxLayout()
        
        self.grp_1.setLayout(self.grp_1_layout)
        
        self.radio1 = QRadioButton("url")
        self.radio1.setChecked(True)
        self.radio2 = QRadioButton("page")
        #self.gbox.addWidget(self.radio1,1,0)
        #self.gbox.addWidget(self.radio2,1,1)
        self.grp_1_layout.addWidget(self.radio1)
        self.grp_1_layout.addWidget(self.radio2)
        self.gbox.addWidget(self.grp_1,1,0)
        self.radio1.clicked.connect(self.radioButtonClicked)
        self.radio2.clicked.connect(self.radioButtonClicked)
        self.l9 = QLabel()
        self.l9.setText('url')
        self.l9.setAlignment(Qt.AlignCenter)
                
        #self.gbox.addWidget(self.l6, 1, 0)
        self.gbox.addWidget(self.cafePage, 1, 1)
        
        #self.gbox.addWidget(self.l9, 2, 0)
        
        self.l7 = QLabel()
        self.l7.setText('다운로드')
        self.l7.setAlignment(Qt.AlignCenter)
        self.cafePath = QLineEdit()
        self.cafe_path = self.set_path("./download_path.txt","네이버 카페")
        self.cafePath.setText(self.cafe_path)

        self.fileButton3 = QPushButton('경로')
        self.saveButton3 = QPushButton('저장')
       
        self.gbox.addWidget(self.l7, 0, 0)
        self.gbox.addWidget(self.cafePath, 0, 1)
        self.gbox.addWidget(self.fileButton3, 0, 2)
        self.gbox.addWidget(self.saveButton3, 0, 3)
        
        self.cafeButton = QPushButton('Crawl')
        self.pwid3 =QPushButton('ID/PW')
        
        self.gbox.addWidget(self.cafeButton, 1,3)
        self.gbox.addWidget(self.pwid3, 1,2)
        self.pwid3.clicked.connect(lambda state,index=2, shop="네이버 카페" : self.setIdPassword(index,shop))        
        self.saveButton3.clicked.connect(lambda state, number =4 : self.saving(number))

        
        ##상황바 하단
        self.bar_layout = QHBoxLayout()
        

        self.bar_label = QLabel('Crawling: ')
        self.bar_label_result = QLabel('Done')#크롤링 되고있는 자료들 

        self.bar_label2 = QLabel('Crawling 개수: ')
        self.bar_label_result2 = QLabel()#크롤링 되고있는 자료들 개수
        #self.bar_label_result2.setText(nc.aa)
        
        
        #self.bar_layout.addWidget(self.bar_label)
        #self.bar_layout.addWidget(self.bar_label_result)
        
        



        
        #crawling된 거 보여주는 테이블 
        



        #tab2 layout set
        self.tab2.layout.addWidget(self.groupbox1)
        self.tab2.layout.addWidget(self.groupbox2)
        self.tab2.layout.addWidget(self.groupbox3)
        self.tab2.layout.addWidget(self.groupbox4)


       
        #self.tab2.layout.addWidget(self.bar_layout)
        
        self.tab2.setLayout(self.tab2.layout)
        
        
        

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.layout.addSpacing(3)
        #self.layout.addWidget(self.result)
        self.setLayout(self.layout)

        # 버튼 click function 연결
        self.load.clicked.connect(( lambda state, number=0 : self.findPath(state, number)))
        #폴더 선택하는 버튼 
        self.fileButton1.clicked.connect(( lambda state, number=1 : self.findPath(state, number)))
        self.fileButton2.clicked.connect(( lambda state, number=2 : self.findPath(state, number)))
        self.fileButton3.clicked.connect(( lambda state, number=3 : self.findPath(state, number)))
        self.fileButton4.clicked.connect(( lambda state, number=4 : self.findPath(state, number)))

        


        
        self.kakaoButton.clicked.connect(self.kakaoCrawling)
        self.sinsangButton.clicked.connect(self.sinsangCrawling)
        self.blogButton.clicked.connect(self.blogCrawling)
        self.cafeButton.clicked.connect(self.cafeCrawling)
  #     self.save.clicked.connect(self.saving) # 저장버튼 누르면 안에있는 메소드 실행
        self.save.clicked.connect(lambda state, number =1 : self.saving(number))
        self.AddButton.clicked.connect(self.addClient)

    def run_command(self):
        cmd = str(self.le.text())
        stdouterr = os.popen4(cmd)[1].read()
        self.te.setText(stdouterr)

    def add(self):
        row = self.list.currentRow()
        title = "거래처 추가" 
        question = "추가할 거래처를 입력해주세요."
        string, ok = QInputDialog.getText(self, title, question)
        if ok and string is not None:
            self.list.insertItem(row, string)
 
 
    def edit(self):
        row = self.list.currentRow()
        item = str(self.list.item(row).text())
        if item is not None:
            title = "{} 거래처 수정".format(item)
            question = "거래처를 수정해주세요."
            string, ok = QInputDialog.getText(self, title, question,
                    QLineEdit.Normal, item)
            if ok and string is not None:
                item.setText(string)
 
 
    def remove(self):
        row = self.list.currentRow()
        item = self.list.item(row)
        if item is None:
            return
        reply = QMessageBox.question(self, "거래처 삭제", "'{0}' 거래처를 삭제하시겠습니까?".format(
        str(item.text())),QMessageBox.Yes|QMessageBox.No)
        if reply == QMessageBox.Yes:

            #shops.txt파일에서도 삭제
            data = self.shops_file_open()
            

            #index 찾기   
            try:
                index = data.index(str(item.text()))# shops.txt에서 index 찾기(4,5,6,7,8,9,10...)
            
            except ValueError: # 해당 text가 shops에 없다면
                print('shops.txt에 해당 거래처가 없습니다.')
                print('다시 실행해주세요')
                index = -2 #...?
                

            #리스트에서 해당 요소 삭제 
            del data[index]#가우디
            #그 다음 요소도 삭제
            del data[index]
            

            #다시 파일에 저장
            f = open('./shops.txt', 'w', encoding='UTF8')
            f.seek(0)
            f.write('\n'.join(data))
            f.close()
            print('해당 거래처가 삭제되었습니다.')
            QMessageBox.about(self, "message", "해당 거래처가 삭제되었습니다.")#바로 실행
            
            #self.data리스트 다시 쓰기

            
            
            #pyqt리스트에서 삭제
            item = self.list.takeItem(row)
            del item

            #전체 거래처 줄이기

            self.shop_number -=1
            self.che.setText('전체 거래처 ({}개)'.format(self.shop_number))   


            
    def sort(self):
        self.list.sortItems()
 
 
         

    def listview_clicked(self):
        item = self.list.currentItem()
        row = self.list.currentRow()
        text = str(item.text())
        data = self.shops_file_open()
        try:
            index = data.index(text)# shops.txt에서 index 찾기
            text +="\n"+data[index+1]
        
        except ValueError: # 해당 text가 shops에 없다면
            print('shops.txt에 해당 거래처가 없습니다.')
            print('다시 실행해주세요')
            

            text +='\n???'
    
        self.label.setText(text)
       
        
        
    def shops_file_open(self):
        
        f = open("./shops.txt", 'r',  encoding='UTF8')
        data = f.read().strip().split('\n')
        f.close()
        return data
        
    #패스를 저장하는 기능 
    def saving(self,number):
  
        
        if number ==1:
            title = "거래처"
            tt = self.NormalPath.text().strip()# 내가 새로 입력한 값 
            
        elif number ==2:
            title = "카카오스토리"
            tt = self.kakaoPath.text().strip()
            
        elif number ==3:
            title = "신상마켓"
            tt = self.sinsangPath.text().strip()
            
        elif number ==4:
            title = "네이버 카페"
            tt = self.cafePath.text().strip()

        elif number ==5:
            title = "네이버 블로그"
            tt = self.blogPath.text().strip()
        else :
            title =""
            tt =""
            
       

        
        if tt =="":  # 칸이 빈칸이라면 
            print('빈칸입니다. 다시 해주세요')
            QMessageBox.about(self, "Warning", "빈칸입니다. 다시 입력해주세요")#바로 실행

        else:
            
            #새로운 경로 파일에 저장

            self.replaceInFile("./download_path.txt",title,tt)
                    
            QMessageBox.about(self, "message", "저장되었습니다")#바로 실행
            print('경로가 저장되었습니다')
            print('변경된 패스는 ' +tt +' 입니다.')
            #self.path = tt
            

            #밑에도 추가되게
            
            
            



        
        

            

    def findPath(self, state, number):
        fname = QFileDialog.getExistingDirectory(self) #폴더 선택하는 창 띄움
        #선택시 바로 파일에 저장되게 저장 누를 필요x 
        if number == 1:
            self.kakaoPath.setText(fname)
        elif number == 2:
            self.blogPath.setText(fname)
        elif number == 3:
            self.cafePath.setText(fname)
        elif number == 0:
            self.NormalPath.setText(fname)
        else:
            self.sinsangPath.setText(fname)
            

    def kakaoCrawling(self):
        url = self.kakaoUrl.text()
        download_path = self.kakaoPath.text()
        
        if not ( url.strip() and download_path.strip()):
            print('url또는 다운로드패스가 빈칸입니다. 다시 해주세요')
            QMessageBox.about(self, "Warning", "url또는 다운로드패스가 빈칸입니다. 다시 입력해주세요")#바로 실행

        
        else:
            downloadpath_kakao = self.kakaoPath.text() # 다운로드 위치
            kc.kakao_crawling(url, downloadpath_kakao)

    def sinsangCrawling(self):
        url = self.sinsangUrl.text()
        download_path = self.sinsangPath.text()

        if not ( url.strip() and download_path.strip()):
            print('url또는 다운로드패스가 빈칸입니다. 다시 해주세요')
            QMessageBox.about(self, "Warning", "url또는 다운로드패스가 빈칸입니다. 다시 입력해주세요")#바로 실행

        else:
            path = self.sinsangPath.text()
            sc.singsang_crawling(url, path)

    def blogCrawling(self):
        url = self.blogUrl.text()
        download_path = self.blogPath.text()

        if not ( url.strip() and download_path.strip()):
            print('url또는 다운로드패스가 빈칸입니다. 다시 해주세요')
            QMessageBox.about(self, "Warning", "url또는 다운로드패스가 빈칸입니다. 다시 입력해주세요")#바로 실행
        else:    
            download_blog = self.blogPath.text()
            nc.naver_blog(url, download_blog)
                   
                    
    def cafeCrawling(self):
        page = self.cafePage.text()
        download_path = self.cafePath.text()

        if not (page.strip() and download_path.strip()): # 칸이 빈칸이라면 
            print('url또는 다운로드패스가 빈칸입니다. 다시 해주세요')
            QMessageBox.about(self, "Warning", "url또는 다운로드패스가 빈칸입니다. 다시 입력해주세요")#바로 실행

        else:
            if self.radio1.isChecked():
                nc.naver_cafe_url(page, download_path) #url크롤링 
                
            else:
                nc.naver_cafe_page(page, download_path) #페이지 크롤링

            

   
    @pyqtSlot()
    def pageCrawling2(self):


        #index값은 -> shops.txt에 저장된 순이여야함
        row = self.list.currentRow() # 지금 클릭한 행
        item = self.list.item(row)
        if item is None:
            return
        
        shop = item.text() # 가우디 

        
        data = self.shops_file_open()

        

        #index 찾기   
        try:
            index = data.index(shop) # shops.txt에서 index 찾기(4,5,6,7,8,9,10...)
        
        except ValueError: # 해당 text가 shops에 없다면
            print('shops.txt에 해당 거래처가 없습니다.')
            print('다시 실행해주세요')
            index = -2 #...?

        url = data[index+1] #

        index =int((index/2)+4)
        
       
        #거래처 패스 경로
        
        f = open('./download_path.txt',  'r',  encoding='UTF8')
        data2 = f.read().strip().split('\n')
        f.close()
       
        location = data2.index("거래처")

        path = data2[location+1]
        print(path)
        
        #에러나면 path 가 빈칸이라면 
        #return

        

        
        download_path = self.NormalPath.text().strip()
        

        
        # CRAWL 전에 아이디/ 비번 빈칸 체크하기
        #문제

        
        def check_idpw_empty():
            #여기서 파일을 열기
            with open('IdPw.txt', 'rb') as file:    # james.p 파일을 바이너리 읽기 모드(rb)로 열기

                try:
                    scores= pickle.load(file) #딕셔너리 저장
                        
                except EOFError: # 더 이상 로드 할 데이터가 없으면
                    scores={}

                if not download_path:
                    QMessageBox.about(self, "warning", "다운로드 패스가 빈칸입니다. 다시 해주세요")#바로 실행
                    print("다운로드 패스가 빈칸입니다. 다시 해주세용")
                    return False


                if(index not in scores): #index 값이 scores 딕셔너리안에 없다면

                    QMessageBox.about(self, "warning", "아이디/패스워드가 빈칸입니다. 다시 해주세요")#바로 실행
                    print("아이디/패스워드가 빈칸입니다. 다시 해주세용")
                    return False

                                 
                else: # 딕셔너리 안에 있다면   
                    return True

            
        

        if (check_idpw_empty()): # 리턴 트루일때만

            wc.web_crawling(str(url), path, shop,index)
            


   
        
   #추가 버튼 누르면 작동할 함수 
    def addClient(self):
        #self.widget = Addclient()

        win = SubWindow()
        r = win.showModal()

        row = self.list.currentRow()

        #new_c_name = win.client_name_input.text()
        
        if r:
            new_c_name = win.name_new #error
            self.list.insertItem(row,new_c_name)
            
        self.shop_number +=1
        self.che.setText('전체 거래처 ({}개)'.format(self.shop_number))            


   #수정 버튼 누르면 작동할 함수 
    def editClient(self):
        
        row = self.list.currentRow()
        item = self.list.item(row)
        if item is None:
            return
        
        
        #이름을 매개변수로 주고, 찾기 
        win = SubWindow2(str(item.text()))
        r = win.showModal()
        
        client_name_input = win.client_name_input.text()
        client_url_input= win.client_url_input.text()

        if r:
            item.setText(client_name_input)

            #하단에도 바꿔야함
            self.label.setText(client_name_input+'\n'+client_url_input)

        
        
 
            
    def show(self):     
        super().show()

    def setIdPassword2(self):
        #index값은 -> shops.txt에 저장된 순이여야함
        row = self.list.currentRow() # 지금 클릭한 행
        shop = self.list.item(row).text()
        #print(shop.text())#가우디
        win = SetIdPass2(shop)
        r = win.showModal()
        
    def setIdPassword(self,index,shop):

        
        #self.widget = SetIdPass()
        win = SetIdPass(index,shop)
        r = win.showModal()
        
    def all_setIdPassword(self):
        
        win = All_SetIdPass()
        r = win.showModal()
        
    def replaceInFile(self,file_path, old, newstr):
        
        
        if os.stat(file_path).st_size ==0:#빈내용인 download_path.txt 라면
            read_file = ["",""]
            read_file[0] = old+ "\n"
            read_file[0]
            read_file[1] = newstr+ "\n"            
            
        else: #내용이 있다.
            f = open(file_path, 'r', encoding='utf8')
            read_file = f.readlines()
            f.close()
            n=0
            isit = False
            
            for line in read_file:
                n+=1
                if old in line: #주어진 "카카오스토리"문자열이 있는 경우
                    isit = True
                    break

            if isit == False:
                #해당 문자열이 없다면 그 다음줄에
                #아예 새로 써야함
                read_file.append(old + "\n")
                read_file.append(newstr + "\n")
                

            else:  
                read_file[n] = newstr+"\n" #고치고 내용을 다시 쓴다.
        ##ELSE


        #파일 쓰기 
        new_file = open(file_path,'w', encoding='utf8')
        new_file.writelines(read_file)
        new_file.close()

        

    def set_path(self,file_path,name):
        try:
            f = open(file_path, 'r', encoding='utf8')
        except FileNotFoundError as e :
            #파일 생성
            f = open("./download_path.txt", 'w',  encoding='UTF8')
            f.close()
            f = open('./download_path.txt',  'r',  encoding='UTF8')

        
        if os.stat("./download_path.txt").st_size ==0:#안에 내용이 없을때 즉, 방금 생성했을때
            return ""
        else:#파일 있는데
            
                
            n=0
            read_file = f.read().split("\n")
            f.close()
            
            isit = False
            for line in read_file:
                n+=1
                if name in line: # 해당 이름이 있음 
                    isit = True
                    break
                

            
            if isit:
                return read_file[n]
            else:#해당하는 파일이 없다면 
                return ""
            
        
   #         return read_file[n]


    

    def radioButtonClicked(self):
        
        if self.radio1.isChecked():
            #self.cafePage.setText("원하는 url를 입력해주세요.")
            self.cafePage.setPlaceholderText("원하는 url를 입력해주세요.")

        elif self.radio2.isChecked():
            self.cafePage.setPlaceholderText("게시판의 페이지를 입력해주세요.")
            #self.cafePage.setText("mielle_product게시판의 페이지를 입력해주세요.")
        else:
            print('')
            

if __name__ == '__main__':
    start = time.time()  # 시작 시간 저장
    app = QApplication(sys.argv)
    app.setStyle('Fusion') # ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']

    
    ex = App()
    sys.exit(app.exec_())
