from selenium import webdriver
import chromedriver_binary
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import pandas as pd
import time
import os
import sys
import re
import pickle
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.error import HTTPError
#알림창 추가
from tkinter import messagebox as msg
from tkinter import Tk

class SinsangCrwaling:

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
            
    def login_sinsang(driver):
        

        driver.get('https://sinsangmarket.kr')
        
        driver.execute_script("$('#login_container').css('display', '');")
        
        user_id = SinsangCrwaling.get_user_idpw(1)[0] # index가 신상마켓은 1임 
        user_pw = SinsangCrwaling.get_user_idpw(1)[1]

        driver.find_element_by_xpath('//*[@id="login_container"]/div[2]/div[2]/form/input[1]').send_keys(user_id)

        driver.find_element_by_xpath('//*[@id="login_container"]/div[2]/div[2]/form/input[2]').send_keys(user_pw)

        driver.find_element_by_xpath('//*[@id="login_container"]/div[2]/div[2]/form/div/button[1]').click()
        time.sleep(2)      
        
        print('커렌트',driver.current_url)




        
    def get_user_idpw(index):
        
        lists = []

        try:
            f = open('IdPw.txt',"rb")
            
        except FileNotFoundError as e:
            print("파일이 존재하지 않습니다.")

        else:#정상실행될때 
            try:
                scores= pickle.load(f) #딕셔너리 저장
            except EOFError: # 더 이상 로드 할 데이터가 없으면 
                scores={}

            f.close()
        
           
                 
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
    
    def singsang_crawling(url, path):
        #url = "https://www.sinsangmarket.kr//v3/goodsDetail?gid=38970711"


        path = path.replace('/','\\')
    
        #마지막에 '\'가 없다면 추가해주기
        if path[-1] !='\\':
            path+='\\'

        try:


            driver = SinsangCrwaling.get_driver()
            
            driver.get('https://sinsangmarket.kr')
            
            driver.execute_script("$('#login_container').css('display', '');")
            
            user_id = SinsangCrwaling.get_user_idpw(1)[0] # index가 신상마켓은 1임 
            user_pw = SinsangCrwaling.get_user_idpw(1)[1]

            driver.find_element_by_xpath('//*[@id="login_container"]/div[2]/div[2]/form/input[1]').send_keys(user_id)

            driver.find_element_by_xpath('//*[@id="login_container"]/div[2]/div[2]/form/input[2]').send_keys(user_pw)

            driver.find_element_by_xpath('//*[@id="login_container"]/div[2]/div[2]/form/div/button[1]').click()
            time.sleep(2)

            driver.get(url)
                
            soup = bs(driver.page_source, 'html.parser')

            time.sleep(5)

            title = soup.select_one('div.goods_name').text#물품 이름
            #특수문자 제거(파일 생성 안됨)
            title = re.sub('[\/:*?"<>|]','-',title)
            price = soup.select_one('div.goods_price').text

        

            details = soup.find_all('td')
            goodsDetail = title + '\n\n' + price + '\n\n'
            
            for detail in details:
                goodsDetail += (detail.text+'\n')

            #img_tags = soup.find_all('img', height=80)#여서 나네
            img_tags = soup.select('.gthumb img')#여기서 나네
            img_urls = []


            for src in img_tags:
                r = re.compile('src="(.*?)&amp')
                m = r.search(str(src))
                if m:
                    img_urls.append(str(m.group(1))+'&h=907&w=690')

            download_path = path + title
            
            
            textfile = download_path + "\\" + title + ".txt"


            if not(os.path.exists(download_path)):#폴더가 없다면 
                os.makedirs(download_path)
                
                f = open(textfile, "w" , -1, "utf-8") 
                for char in goodsDetail:
                    f.write(char)
                f.close()

            else:#해당파일이 있으면 
                print("해당 폴더가 이미 있습니다. ")
                #break             


            print("<전체 이미지 : {}장입니다.>".format(len(img_urls)))

            for key, value in enumerate(img_urls):
                
                try:
                    t = urlopen(value).read()
                    
                except HTTPError as e:
                    print('The server couldn\'t fulfill the request.')
                    print('Error code: ', e.code)
                    break
                    
                except URLError as e:
                    print('We failed to reach a server.')
                    print('Reason: ', e.reason)
                    break

                filename = download_path + "/" +title +'_'+ str(key+1) + '.jpg'

                #해당 파일이 있으면 저장하지 않고 없으면
                if not(os.path.exists(filename)):
                    with open(filename,"wb") as f:
                        f.write(t)

                    print("이미지 {}번 Save Success".format(key+1))
                else:#해당파일이 있으면 
                    print("해당 파일이 이미 있습니다. ")
                    break                            

            print('Done!!')



        except AttributeError as e:
            print(str(e))
            print("로그인이 잘못되었거나 태그를 찾을 수 없습니다.")

        except Exception as e:
            print('Exception 에러 발생!')
            print(str(e))
            
        finally:
            #os.system("Pause")
            driver.quit()
