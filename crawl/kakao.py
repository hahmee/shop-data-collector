from selenium import webdriver
import chromedriver_binary
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import pandas as pd
import time
import os
import sys
import json
import re
import pickle
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
#알림창 추가
from tkinter import messagebox as msg
from tkinter import Tk

#로그인 성공 못하면, 로그인 틀렸다고 알림 

class KakaoCrawling:
    
    def get_driver():
        driver = webdriver.Chrome(executable_path = r'./chromedriver_win32/chromedriver.exe')
        driver.implicitly_wait(3)#암묵적으로 3초 대기 
        return driver
    
    def message(types):
    #알림메시지가 뜨는 창
        root= Tk()
        root.withdraw()
        if types ==1:
            msg.showinfo('알림창.', '찜하기를 아직 누르지 않으셨습니다. 다시 눌러주세요.')
        elif types==2:
            msg.showinfo('알림창.', '아이디/비밀번호를 설정하지 않으셨습니다.')
        elif types==3:
            msg.showinfo('알림창.', '아이디/비밀번호가 틀렸습니다.')
        else:
            msg.showindfo('알림창','')
            
    def login_kakao(driver):
    

        driver.get('https://accounts.kakao.com/login/kakaostory')

        user_id = KakaoCrawling.get_user_idpw(0)[0] # index가 카카오스토리는 0 임 
        user_pw = KakaoCrawling.get_user_idpw(0)[1]   
        
        #로그인 성공 
        driver.find_element_by_xpath('//*[@id="id_email_2"]').send_keys(user_id)
        driver.find_element_by_xpath('//*[@id="id_password_3"]').send_keys(user_pw)
        driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[8]/button').click() #로그인 확인
        #다음페이지 넘어감
        #print(driver.current_url) # https://accounts.kakao.com/login/kakaostory
        
        
        time.sleep(1)
        print(driver.current_url) 
        if (driver.current_url != "https://story.kakao.com/"):
            print("카카오스토리 로그인이 실패되었습니다.")
            KakaoCrawling.message(3)
            return False
            
        else:
            print('카카오스토리 로그인이 되었습니다.')
                    
        
        return True

                
    def get_user_idpw(index):
        
        lists = []
        
        with open('IdPw.txt', 'rb') as file:    # james.p 파일을 바이너리 읽기 모드(rb)로 열기            

            try:
                scores= pickle.load(file) #딕셔너리 저장
                    
            except EOFError: # 더 이상 로드 할 데이터가 없으면 
                 scores={}
                 
        if(index in scores): #index 값이 scores 딕셔너리안에 있다면 
            id_value= scores[index][1]
            pw_value= scores[index][2]
            lists.append(id_value)
            lists.append(pw_value)

        else: # 아직 아이디 비번 설정 안했다면
            print('설정안했어요')
            root= Tk()


            root.withdraw()

            msg.showinfo('알림창.', '아이디/비밀번호를 설정하지 않으셨습니다.')
            #하고 프로그램이 오류나고 끝남
            
            #아디 비번이 틀린 경우     
                
            
        return lists
    
    def kakao_crawling(url, downloadpath):
        #print(downloadpath)
        downloadpath = downloadpath.replace('/','\\')
    
        #마지막에 '\'가 없다면 추가해주기
        if downloadpath[-1] !='\\':
            downloadpath+='\\'

        try: 
            driver = KakaoCrawling.get_driver()
            
            login = KakaoCrawling.login_kakao(driver)

            if login:
                print('로그인 됨')
                driver.get(url)
                soup = bs(driver.page_source, 'html.parser')
                
                script = str(soup.find_all('script')[1]).split('\n')

                #sripte 태그 + 불필요한 부분 제거 + 제이슨 형식으로 변경
                test = script[1].replace("boot.parseInitialData(",'')
                test = test.replace( ");" , '')
                #print(test)

                #image 원본 url 저장할 배열
                img_urls = []

                p = re.search(r"(/photos/(\d+))$",url) # 숫자로 끝나고
                if p:                
                    title = url.split("/")[-3]
                else:
                    title = url.split("/")[-1]
                    
                
                print('title: '+title)
                
                dirName = downloadpath + '카카오스토리' + '-' + title + "\\"

                
                #print('dirName ' + dirName)
                
                #content 저장할 주소
                #폴더 없으면 생성
                if not(os.path.exists(dirName)):
                    os.makedirs(dirName)

                textfile = dirName + "\\" + title + ".txt"
                
                #json 로드가 실패하면
                data = json.loads(test)
                getCreatedDate = data['activity']['created_at'].split('T')
                date = str(getCreatedDate[0]) + "\n"
            
                #제품 정보
                info = data['activity']['content']
                images = data['activity']['media']
                
                if not (os.path.exists(textfile)): # 텍스트파일이 없다면  
                    #text작성
                    f = open(textfile, "w" , -1, "utf-8")
                    f.write(date)
                    for i in info:
                        f.write(i)
                    f.close()
                else:
                    print('해당 텍스트파일이 이미 있습니다.') 


                #원본 url 저장
                for img in images:
                    img_urls.append(img['origin_url'] )

                print("<전체 이미지 : {}장입니다.>".format(len(img_urls)))

                #이미지 다운로드
                Done = False
                for index in range(len(img_urls)):
                    
                    #원본url 읽어오기
                    t = urlopen(img_urls[index]).read() 

                    filename = dirName + "/" + title +'_'+str(index) + '.jpg'

                    #print('filename'+filename)

                    #해당 파일이 있으면 저장하지 않고 없으면
                    if not(os.path.exists(filename)):
                        Done = True
                        with open(filename,"wb") as f:
                            f.write(t)
                        #print("Image Save Success")
                        print("이미지 {}번 Save Success".format(index+1))
                    else:#해당파일이 있으면
                        print("해당 이미지가 이미 있습니다. ")
                        break
                    
                print("Done!")

                
            else :
                print('로그인 안됨')

    


        except Exception as e:
            print(str(e))
            
            r = re.compile('"content":(.*?),"require')
            m = r.search(test)
            if m:
                content = m.group(1)
                info = content.split('\\n')

            #image url
            i = re.compile('"media":(.*?),"content"')
            j = i.search(test)     
            if j:
                images = json.loads(j.group(1))

            #제품 등록 날짜
            a = re.compile('"created_at":"(.*?),"with_tag_count"')
            b = a.search(test)
            if b:
                date = str(b.group(1)).split('T')[0] + '\n'
            
            #text 파일 만들기
            f = open(textfile, "w" , -1, "utf-8")
            f.write(date)
            for i in info:
                f.write(i+'\n')
            f.close()

            #저장함수 실행되어야함
            for img in images:
                img_urls.append(img['origin_url'] )

            print("<전체 이미지 : {}장입니다.>".format(len(img_urls)))

            #이미지 다운로드
            for index in range(len(img_urls)):
                
                #원본url 읽어오기
                t = urlopen(img_urls[index]).read() 

                filename = dirName + "/" + title +'_'+str(index) + '.jpg'

                #print('filename'+filename)

                #해당 파일이 있으면 저장하지 않고 없으면
                if not(os.path.exists(filename)):
                    with open(filename,"wb") as f:
                        f.write(t)
                    print("이미지 {}번 Save Success".format(index+1))
                    
            print("Done!")            
    
        finally:
            driver.quit()
       
       
