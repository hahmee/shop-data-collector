from selenium import webdriver
import chromedriver_binary
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from urllib.error import HTTPError
from urllib.error import URLError
import time
import os
import sys
import pickle
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot
#알림창 추가
from tkinter import messagebox as msg
from tkinter import Tk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re

class WebCrawling:
    
    def get_driver():

        
        driver = webdriver.Chrome(executable_path = r'./chromedriver_win32/chromedriver.exe')
        driver.implicitly_wait(3)#암묵적으로 3초 대기 

        return driver

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
            print('아이디/비번 설정안했어요')

            WebCrawling.message(2)
            
            #하고 프로그램이 오류나고 끝남
            
            #아디 비번이 틀린 경우     
                
            
        return lists
    
    def login_web(driver,url,index):

        driver.get(url + '/Login')
        print("로그인을 처리 중입니다...")        
            
        user_id=WebCrawling.get_user_idpw(index)[0]
        user_pw=WebCrawling.get_user_idpw(index)[1]
 
        driver.find_element_by_xpath('//*[@id="user_id"]').send_keys(user_id)
        driver.find_element_by_xpath('//*[@id="user_pwd"]').send_keys(user_pw)
        driver.find_element_by_xpath('//*[@id="login_frame1"]/input[3]').click() # 확인
            
        time.sleep(1)

        try:
            WebDriverWait(driver,3).until(EC.alert_is_present())
            
        except TimeoutException:
            print("로그인 성공") # 로그인 성공한 것임
            return True

        else:
            print("아이디/비밀번호가 틀렸습니다.")
            WebCrawling.message(3)
            return False
            
        #finally:
        #    return False

            
            
    
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

            
            
                
                        
              
  
    def web_crawling(url, path, storeName,index):

        #path안에 /가 있다면 \로 바꾸기
        path = path.replace('/','\\')
    
        
        #마지막에 '\'가 없다면 추가해주기
        if path[-1] !='\\':
            path+='\\'
        
    
                        
            
        
        def getInfo():
         
            details = []

            #제품 클릭 기다리기
            
            elemente = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.jquery-modal.blocker.current"))
            )
            

   
                 #print(elemente)# 가져온 값 
            print('=============================================================')
            
            imgList = elemente.find_element_by_id('gd_listimg').get_attribute('innerHTML')
            

            
            section = elemente.find_elements_by_xpath('//*[@id="pro_pop"]/ul/li[2]/section')

            for x in section:
                context = bs(x.get_attribute('innerHTML'), 'html.parser')
                #context = bs(x.get_attribute('innerHTML'), 'lxml') # 속도 굳
 
            titleList = context.select_one('#pro_name')
            proInfoList = context.select('#pro_info')
            #제품명 가져오기
            title = titleList.text.split('[')[0].strip()
            
            #제품명 가져오기
            #for t in titleList:
            #    title = t.get_text().split('[')[0]
                
            #특수문자 제거(파일 생성 안됨)
            title = re.sub('[\/:*?"<>|]','-',title)
            print('[제품명: ' + title +']')
            details.append(title)

            #이미지 리스트
            soup = bs(imgList, 'html.parser')
            #soup = bs(imgLsit, 'lxml')

            #img tag
            imgs = soup.find_all('img')

            #제품 정보
            sizeInfo = soup.find_all('div')

            for size in sizeInfo:
                if(size.get_text()):
                    details.append(size.get_text())
                    details.append('\n')

            for pro_info in proInfoList:
                #제품 비침, 신축성, 두께감 정보
                detail_info = pro_info.select('li > div > p')
                #색상, 사이즈 옵션 
                options = pro_info.select('li > select > option')
                #가격, 혼용률 정보
                price_etc = pro_info.select('li')

            for i in range(7):
                #8번째 li까지 - 도매가, 혼용률, 중량, 원산지, 등록일자, 모델 정보
                details.append(price_etc[i].get_text())

            details.append('\n')

            for li in detail_info:
                #제품 비침, 신축성, 두께감 정보 추가
                details.append(li.get_text())

            details.append('\n')

            for option in options:
                #색상, 사이즈 옵션 추가
                details.append(option.get_text())

            details.append('\n')

            detail = "\n".join(details)

            dirName = path + storeName + '-' + title + "\\"
            


            #print('dirName ' + dirName)

            #제품정보 저장할 파일
            info_file = dirName + "\\" + title + ".txt"
            
            #해당 폴더가 없다면 
            if not(os.path.exists(dirName)):
                os.makedirs(dirName)

            if not (os.path.exists(info_file)): # 텍스트파일이 없다면    

                f = open(info_file, "w" , -1, "utf-8")
                for d in detail:
                    f.write(d)
                f.close() # 추가
                
            else:
                print('해당 텍스트파일이 이미 있습니다.')      
            
            
            #이미지 저장
            print("<전체 이미지 : {}장입니다.>".format(len(imgs)))

            Done=False
            for key, value in enumerate(imgs):
                
                try:    
                    img_url = urlopen(value.attrs['src']).read()
                        
                except HTTPError as e:
                    print('The server couldn\'t fulfill the request.')
                    print('Error code: ', e.code)
                    break
                    
                except URLError as e:
                    print('We failed to reach a server.')
                    print('Reason: ', e.reason)
                    break
            
                
                filename = dirName + "/" + title + '_' + str(key+1) + '.jpg'

                #해당 파일이 있으면 저장하지 않고 없으면 저장
                if not(os.path.exists(filename)):
                    Done=True
                    with open(filename,"wb") as f:
                        f.write(img_url)
                    print("이미지 {}번 Save Success".format(key+1))
                    
                else:#해당파일이 있으면
                    print("해당 이미지가 이미 있습니다. ")
                    break
                    
            if Done:
                print("[{}] 저장 완료".format(title))
                
            print("Done!")
            print('=============================================================')

                

 #           except TimeoutException:
 #               print('Time Out')


    

         # getInfo()끝남 
       ######################

        
 

        try:
            driver = WebCrawling.get_driver()
            login = WebCrawling.login_web(driver,url,index)


            
            time.sleep(1)
            if login :
                print('로그인')
            
                #찜목록으로 이동 http://www.gaudistyle.co.kr/Mypage?m=3 --> 여기가로그인이 안되면 오류가 나는 것임.. 
                driver.get(url+'/Mypage?m=3#') # url에 접근
                            
                
        
                #찜한 제품 로딩될 때까지 wait--> 페이지 로딩 지연이 발생해서 못읽어오는경우가 있어서 좀 기다리자
               
                ul = WebDriverWait(driver,3).until(
                    #EC.presence_of_element_located((By.CLASS_NAME, "ellipsis"))
                    EC.presence_of_element_located((By.ID, "mygoodslist"))#변경 
                    )
                
                goods = bs(driver.page_source, 'html.parser')
                
                #goodslist = goods.select('#mygoodslist > li') # select('원하는 정보') 아예 있을때만 에러 안뜨고 잘 출력 됨
                goodslist = goods.select('#mygoodslist > li')
                #print(goodslist)
                if not goodslist : #배열이 비었냐-->찜 안함 : 경고창 -> 취소
                    #WebCrawling.message(1)
                    print('찜하기를 아직 누르지 않으셨습니다. 다시 눌러주세요')
                    
                else:
                    for num in range(1, len(goodslist)+1):
                        mygoodslist = ul.find_element_by_xpath('//*[@id="mygoodslist"]/li['+ str(num) +']/figure/a')
                        driver.execute_script("arguments[0].click();", mygoodslist)
                        time.sleep(2)
                        getInfo() # 정보 가져오기 

                driver.get(url+'/Mypage?m=3#/')
                
                for num in range(1, len(goodslist)+1):
                    mygood = ul.find_element_by_xpath('//*[@id="mygoodslist"]/li['+ str(num) +']/figure/figcaption/div/ul[1]/li[2]/a')
                    driver.execute_script("arguments[0].click();", mygood)
                    #print("mygood",mygood)
                    title = goods.select("p.ellipsis a")[num-1].text.split(']')[1].strip()
                    
                    #print(title)
                    print('[{}] 찜하기 해제'.format(title))

            else:
                print('로그인이 안되었어요.')
                    
                            

        except TimeoutException:
            print("WebDriverWait의 속성값을 가진 태그가 존재하지 않거나, 해당 페이지가 3초 안에 열리지 않았습니다.")
        except AttributeError as e:
            print("태그를 찾을 수 없습니다.")            
        except Exception as e:
            print('Exception 에러 발생!')
            print(str(e))
            print('다시 실행해주세요')

            
        finally:
            driver.quit()    
   
        
    
       
            
        
