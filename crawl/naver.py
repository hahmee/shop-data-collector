from selenium import webdriver
import chromedriver_binary
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import time
import os
import sys
import re
import pickle
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.error import HTTPError
from urllib.error import URLError
import random
from tkinter import messagebox as msg
from tkinter import Tk
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyperclip
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QProgressBar,QDialog
from PyQt5.QtCore import QBasicTimer


class Naver_progress(QDialog):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)

        self.btn = QPushButton('Start', self)
        self.btn.move(40, 80)
        self.btn.clicked.connect(self.doAction)

        self.timer = QBasicTimer()
        self.step = 0

        self.setWindowTitle('QProgressBar')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.btn.setText('Finished')
            return

        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText('Start')
        else:
            self.timer.start(100, self)
            self.btn.setText('Stop')

    def showModal(self):
        return super().exec_()
    
class NaverCrawling:

    def show_result():
        print('show_result')
        #win = Naver_progress()
    
        
      #  r = win.showModal()

    

    def folder_open(dirName):
        path = dirName
        path = os.path.realpath(path)
        os.startfile(path)
        #이미 열려있으면 

            
    
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
            
    def get_driver():
        #headless chrome으로 바꾸기
        '''
        
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        '''
        driver = webdriver.Chrome(executable_path = r'./chromedriver_win32/chromedriver.exe')
        driver.implicitly_wait(3)#암묵적으로 3초 대기 
        return driver

    def login_naver(driver):
        #캡챠 막기위해
        
        def copy_input(xpath, input):
            pyperclip.copy(input)
            driver.find_element_by_xpath(xpath).click()
            ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            time.sleep(1)
        
        driver.get('https://nid.naver.com/nidlogin.login')
        user_id = NaverCrawling.get_user_idpw(2)[0] #네이버 카페 
        user_pw = NaverCrawling.get_user_idpw(2)[1]


        copy_input('//*[@id="id"]', user_id)
        time.sleep(1)
        copy_input('//*[@id="pw"]', user_pw)
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
                

        time.sleep(1)

        

        #지워도 되는지 확인하기 
        if (driver.current_url == 'https://nid.naver.com/nidlogin.login' ):
            print("네이버 로그인이 실패되었습니다.")
            #NaverCrawling.message(3)
            
        else:
            print('네이버 로그인이 되었습니다.')
            
        return False
    

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
            NaverCrawling.message(2)
            print('아이디/ 비밀번호 설정안했어요')

                
            
        return lists

    def naver_cafe_url(url, downloadPath): # url로

        try: 
            driver = NaverCrawling.get_driver()
            NaverCrawling.login_naver(driver)
             
            time.sleep(2)#캡챠 

            #mielle_product 게시판 
            downloadPath = downloadPath.replace('/','\\')


            
            #마지막에 '\'가 없다면 추가해주기
            if downloadPath[-1] !='\\':
                downloadPath+='\\'

            driver.get(url)

            
            driver.switch_to_default_content  #(1) 상위 프레임으로 전환
            driver.switch_to.frame('cafe_main') # cafe_main 프레임으로 전환 

            
            soup = bs(driver.page_source, 'html.parser')
        
            title = soup.find('span',{'class':'b m-tcol-c'} ).text
            print(title)
            #특수문자 제거(파일 생성 안됨)
            title = re.sub('[\/:*?"<>|]','-',title).strip()
            
            print(title)

            createDate = soup.select('div.tit-box td.date')[0].get_text() + "\n\n"
            context = str(soup.select('div.tbody p')[0]).replace('<br/>','\n')
            context = createDate + str(re.sub('<.+?>', '', context, 0).strip())
            #print(content) # 에러남 --> 인코딩 문제때문에 출력 금지
            
            photoAlbum = soup.find_all('script',{'filename':'externalFile.jpg'}) 
            filepath = downloadPath + title
            textfile = filepath + "/" + title + ".txt"

            try: 
                if not(os.path.exists(filepath)):
                    os.makedirs(filepath) # 에러
                    
            except OSError:
                print('Error: Creating direcory. ' + dirName)
                

            if not (os.path.exists(textfile)): # 텍스트파일이 없다면
                f = open(textfile, "w" , -1, "utf-8")
                for i in context:
                    f.write(i)
                f.close() 
                print('['+title+']txt파일이 저장되었습니다.')
                
            else:
                print('해당 텍스트파일이 이미 있습니다.')
                
            
            print("<전체 이미지 : {}장입니다.>".format(len(photoAlbum)))

            for i in enumerate(photoAlbum):
                index = i[0]
                
                
                #원본url 읽어오기
                try:
                    t = urlopen(i[1].attrs['fileurl']).read()
                    
                except HTTPError as e:
                    print('The server couldn\'t fulfill the request.')
                    print('Error code: ', e.code)
                    break
                    
                except URLError as e:
                    print('We failed to reach a server.')
                    print('Reason: ', e.reason)
                    break

                filename = filepath + "/" +title + '_'+ str(index+1) + '.jpg'

                #해당 파일이 없으면 저장
                if not(os.path.exists(filename)):
                    with open(filename,"wb") as f:
                        f.write(t)
                    print("이미지 {}번 Save Success".format(index+1))

                else:#해당파일이 있으면 
                    print("해당 파일이 이미 있습니다. ")
                    break

           
            print("Done!!")
            

        except AttributeError as e:
            print("태그를 찾을 수 없습니다.")

        except Exception as e:
            print('Exception 에러 발생!')
            print(str(e))
            
        finally:
            #os.system("Pause")
            driver.quit()
    
    def naver_cafe_page(page, downloadPath): # 페이지로 
        try: 
            driver = NaverCrawling.get_driver()
            NaverCrawling.login_naver(driver)

        
            time.sleep(2)

            #mielle_product 게시판 
            base_url = 'https://cafe.naver.com/ArticleList.nhn?search.clubid=29179343&search.menuid=6&search.boardtype=L&search.totalCount=151'

            downloadPath = downloadPath.replace('/','\\')


         
            #마지막에 '\'가 없다면 추가해주기
            if downloadPath[-1] !='\\':
                downloadPath+='\\'

            driver.get(base_url + "&search.page=" + page)
            print(base_url + "&search.page=" + page)
            driver.switch_to.frame('cafe_main')
            #article_list = driver.find_elements_by_xpath('//*[@id="main-area"]/div[4]/table/tbody/tr[2]/td[2]/div/table/tbody/tr/td/a')
            #article_list = driver.find_elements_by_css_selector('span.aaa > a.m-tcol-c')
            #article_list = driver.find_elements_by_css_selector('div.board-list a.article')'
            #첫번째 있는 article-board m-tocol-c 의 a.article
            ##main-area > div:nth-child(6)
            
            #article_list = driver.find_elements_by_css_selector('#main-area > div:nth-child(6) > a.article')
            article_list = driver.find_elements_by_css_selector('#main-area > div:nth-child(6) a.article')

            article_urls = [ i.get_attribute('href') for i in article_list ]
            #href(주소) 로 Web Driver가 접속 함 
            

            for article in article_urls:
                driver.get(article)
                driver.switch_to.frame('cafe_main')
                soup = bs(driver.page_source, 'html.parser')

                #제품설명
                title = soup.select('div.tit-box span.b')[0].get_text()
                #특수문자 제거(파일 생성 안됨)
                title = re.sub('[\/:*?"<>|]','-',title).strip()
                print(title)
                print('title: '+title)
                createDate = soup.select('div.tit-box td.date')[0].get_text() + "\n\n"
                context = str(soup.select('div.tbody p')[0]).replace('<br/>','\n')
                context = createDate + str(re.sub('<.+?>', '', context, 0).strip())
    #            print('context : '+context) 금지 
                #원래 안되는걸수도 있음 
                
                #원본url이 써있는 script 가져옴
                photoAlbum = soup.find_all('script',{'filename':'externalFile.jpg'}) 

                filepath = downloadPath + title
                
                textfile = filepath + "/" + title + ".txt"

                #제품설명txt
                try: 
                    if not(os.path.exists(filepath)):
                        os.makedirs(filepath) # 에러
                        
                except OSError:
                    print('Error: Creating direcory. ' + dirName)
                    

                if not (os.path.exists(textfile)): # 텍스트파일이 없다면
                    f = open(textfile, "w" , -1, "utf-8")
                    for i in context:
                        f.write(i)
                    f.close() 
                    print('['+title+']txt파일이 저장되었습니다.')
                    
                else:
                    print('해당 텍스트파일이 이미 있습니다.')
                    

                print("<전체 이미지 : {}장입니다.>".format(len(photoAlbum)))

                for i in enumerate(photoAlbum):
                    
                    index = i[0]
                    downloadEnd = False
                    
                    #원본url 읽어오기
                    try: 
                        t = urlopen(i[1].attrs['fileurl']).read()
                    except HTTPError as e:
                        print('The server couldn\'t fulfill the request.')
                        print('Error code: ', e.code)
                        break
                        
                    except URLError as e:
                        print('We failed to reach a server.')
                        print('Reason: ', e.reason)
                        break

                    filename = filepath + "/" + title+ '_'+ str(index+1)+ '.jpg'

                    #해당 파일이 없으면 저장
                    if not(os.path.exists(filename)):
                        with open(filename,"wb") as f:
                            f.write(t)
                        print("이미지 {}번 Save Success".format(index+1))

                    else:
                        downloadEnd = True
                        print("해당 파일이 이미 있습니다.")
                        break

                if downloadEnd :
                    break
                
            print("Done!!")

        except AttributeError as e:
            print("태그를 찾을 수 없습니다.")

        except Exception as e:
            print('Exception 에러 발생!')
            print(str(e))
            
        finally:
            driver.quit()
            
    def mola():
        return 'mola'

    
    def naver_blog(posturl, download_path):
        #다 하면 크롤링 결과 나오기 
        
      #try -- except 하기
        #https://blog.naver.com/monica4460

        #파일에서 해당 downloat_path 가 없다면 에러 

      
        
        #######
        download_path = download_path.replace('/','\\')

     
        #마지막에 '\'가 없다면 추가해주기
        if download_path[-1] !='\\':
            download_path+='\\'

        print('download_path' + download_path)
        

        try: 
            driver = NaverCrawling.get_driver()
            driver.get(posturl)

            driver.switch_to.frame('mainFrame')
            soup = bs(driver.page_source, 'html.parser')
            
            details = soup.select('div.se-module span')
      
            title = soup.select_one('div.se-title-text span').text
            
            #특수문자 제거(파일 생성 안됨)
            title = re.sub('[\/:*?"<>|]','-',title).strip()
            #공백문자 제거하기
            #버블리도트 - 실크 
            print(title)

            
            
            
            dirName = download_path + title +"\\"
            print('dirName' + dirName)       

            #폴더 없으면 생성
            try: 
                if not(os.path.exists(dirName)):
                    os.makedirs(dirName) # 에러
                    
            except OSError:
                print('Error: Creating direcory. ' + dirName)
                
                
            
            textfile = dirName + "\\"+ title + ".txt"
            print(textfile)
            
            if not (os.path.exists(textfile)): # 텍스트파일이 없다면
                f = open(textfile, "w" , -1, "utf-8")
                for detail in details:
                    f.write(detail.text.strip() + '\n') #블로그에 파일쓰기 
                f.close() 
                print('['+title+']txt파일이 저장되었습니다.')
                
            else:
                print('해당 텍스트파일이 이미 있습니다.')
            
            imgs = soup.select('img.se-image-resource')

            print("<전체 이미지 : {}장입니다.>".format(len(imgs)))
            
            img_length =  len(imgs)
            print(img_length)
            NaverCrawling.show_result()
            for index, url in enumerate(imgs):

                filename = dirName + "/" + title + '_' + str(index+1) + ".jpg"
                original = url.attrs['src'].split('?')[0].replace('postfiles','blogfiles')
                #print(original)

                #해당 파일이 있으면 저장하지 않고 없으면
                
                if not(os.path.exists(filename)):
                    try:
                        
                        
                        with open(filename, 'wb') as f:
                            f.write(urlopen(original).read())
                            print("이미지 {}번 Save Success".format(index+1)) # 이미지 1번 
                        
                             
                        
                            
                    except HTTPError as e:
                        print('The server couldn\'t fulfill the request.')
                        print('Error code: ', e.code)
                        break
                    except URLError as e:
                        print('We failed to reach a server.')
                        print('Reason: ', e.reason)
                        break
                        
                else:
                    #print("해당{}번 이미지가 이미 있습니다.".format(index+1))
                    print('해당 이미지파일이 이미 있습니다.')
                    break
            
            #for문 끝

            print("Done!!")

            #크롤링 된 이미지 보여주기 -- 마음에 드는것만 선택 한다  

            #폴더 알아서 열어주기 
            NaverCrawling.folder_open(dirName)
            

                        
            
            
        except AttributeError as e:
            print("태그를 찾을 수 없습니다.")
                    
        except Exception as e:
            print('Exception 에러 발생!')
            print(str(e))
            print('다시 실행해주세요')
            pass
            
        finally:
            driver.quit()        
                    
            
        
             


    
