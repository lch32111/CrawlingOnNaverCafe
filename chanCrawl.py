import time
from selenium import webdriver
from bs4 import BeautifulSoup


# TODO
# 1. chromedriver.exe 경로적혀있는 file read하기
# 2. 사용자가 선택한 게시판 메뉴로 가기
# 3. 해당 게시판의 시작/끝 페이지 크롤링 하기
# 4. 데이터 형식에 맞춰 file write 하기


log_id = input('아이디 : ')
log_pw = input('비밀번호 : ')

#S ####### Execute Chrome ############

chrome = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')

#E ####### Execute Chrome ############


#S ####### Naver Login ############

chrome.get('https://nid.naver.com/')
chrome.implicitly_wait(5)

chrome.execute_script("document.getElementsByName('id')[0].value=\'" + log_id + "\'")
chrome.execute_script("document.getElementsByName('pw')[0].value=\'" + log_pw + "\'")
chrome.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()

#E ####### Naver Login ############


time.sleep(3) # Delay for loading user private page of naver.


#S ####### Get Cafe List and goto-Index ############

chrome.get("https://section.cafe.naver.com/")
time.sleep(2)
chrome.implicitly_wait(5)


soup = BeautifulSoup(chrome.page_source, 'html.parser')
mydivs = soup.findAll("div", {"class": "user_mycafe_info"})

CafeIndex = 0;
for div in mydivs:
        CafeIndex += 1
        a = div.find('a')
        cElement = str(CafeIndex) + ' ' + a.get_text()
        print(cElement)
        
CafeIndex = input('\n접속할 카페 목록의 번호 입력 : ')

#E ####### Get Cafe List and goto-Index ############


#S ####### Go to the Cafe ############

CafeMoveScript = "document.querySelector('#content > div.home_user > div.home_user_mycafe > div.user_mycafe_list > div:nth-child("
CafeMoveScript += str(CafeIndex)
CafeMoveScript += ") > div.user_mycafe_box > div.user_mycafe_info > a > strong').click()"
chrome.execute_script(CafeMoveScript)

#E ####### Go to the Cafe ############

time.sleep(3) # Delay for loading Cafe Info

chrome.close() # close the current tab : cafe list site
chrome.switch_to.window(chrome.window_handles[0]) # switch to the new open cafe
time.sleep(3) # Delay for controlling chrome


#S ####### Get Cafe Menu List ############

soup = BeautifulSoup(chrome.page_source, 'html.parser')
mydivs = soup.findAll("ul", {"class": "cafe-menu-list"})

MenuIndex = 0
for divs in mydivs:
    for lis in divs.findAll('li'):
        MenuIndex += 1
        a = lis.find('a')
        MenuStr = " ".join(a.get_text().split())
        mElement = str(MenuIndex) + ' ' + MenuStr
        print(mElement)
        
#E ####### Get Cafe Menu List ############


# Crawling Main Loop

cafeBaseURL = chrome.current_url
firstFlag = True
while(1):
    if(firstFlag == False):
        exitFlag = input("종료(1 - YES / 2 - NO) : ")
        if(exitFlag == '1'): break;

    
    MenuIndex = input('\n카페 메뉴의 번호 입력: ')
    startPage = input('크롤링 시작 페이지 번호 입력 : ')
    endPage = input('크롤링 끝 페이지 번호 입력 : ')
    
    #S ###### Go to the board user chose############



    #E ###### Go to the board user chose############


    #S ###### Crawl on the pages from start to end  ############



    #E ###### Crawl on the pages from start to end  ############



    firstFlag = False

# Crawling Main Loop







