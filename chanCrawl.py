import time
import datetime
import re
from selenium import webdriver
from bs4 import BeautifulSoup

def GetURLFromPageNumb(pageNumb, soup):
        # Case 1 : Success for finding page URL
        # Case 2 : Fail. But There is next button
        # Case 3 : Fail. In Addition, There is no next button
        # Return ( int:Case, str:pageURL or next button URL)
        mydivs = soup.findAll("div", {"class" : "prev-next"})
        b_findCurrentPage = False
        b_findNextBtn = False
        pageURL = ''
        buttonURL = ''
        for divs in mydivs:
                for hrefs in divs.findAll('a'):
                        pageStr = hrefs.get_text()
                        if(pageStr.isdigit() == True):
                                if(int(pageStr) == pageNumb):
                                        pageURL = hrefs['href']
                                        b_findCurrentPage = True
                        elif(pageStr[0] == '다'):
                                b_findNextBtn = True
                                buttonURL = hrefs['href']
        
        if(b_findCurrentPage == True):
                return 1, pageURL;
        elif(b_findCurrentPage == False and b_findNextBtn == True):
                return 2, buttonURL;
        elif(b_findCurrentPage == False and b_findNextBtn == False):
                return 3, None;
        else:
                return -1, None;

def GotoDestPage(chrome, pageNumb):
        # Case 1 : Start Crawling!
        # Case 2 : Stop Crawling!
        # Return ( int : Case , str : pageURL)
        b_startCrawl = False
        b_findCurrentPage = False
        pageURL = ""
        while(b_findCurrentPage == False):
                soup = BeautifulSoup(chrome.page_source, 'html.parser')
                b_result, pageURL = GetURLFromPageNumb(pageNumb, soup)
                if(b_result == 1):
                        # found Page!
                        b_findCurrentPage = True
                        b_startCrawl = True
                        chrome.get(cafeBaseURL + pageURL)
                        chrome.switch_to.frame('cafe_main')
                        chrome.implicitly_wait(3)
                elif(b_result == 2):
                        # page not found, but I got next btn URL
                        # Let's go to next page
                        chrome.get(cafeBaseURL + pageURL)
                        chrome.switch_to.frame('cafe_main')
                        chrome.implicitly_wait(3)
                else:
                        # No Hope. Let's Escape from this loop
                        b_findCurrentPage = True
        return b_startCrawl, pageURL;

def changeStrForProperFileName(fName):
        fName = " ".join(str(fName).split())
        fName = fName.strip().replace(' ', '-')
        return re.sub(r'(?u)[^-\w.]', '', fName)


# TODO
# 1. 내용 못 긁어오는 부분 html 파악해서 긁어오기
# 2. 댓글 긁어와서 write
# 3. 내용과 댓글은 일정 글자 이상되면 \n으로 보기좋게 만들기


log_id = input('아이디 : ')
log_pw = input('비밀번호 : ')

#S ####### Execute Chrome ############
driverFile = open("chrome_driver_location.txt","r")
driverAddr = driverFile.readline()
print("Chrome Driver 위치 : " + driverAddr)
driverFile.close()

chrome = webdriver.Chrome(driverAddr)

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
CafeName = mydivs[int(CafeIndex) - 1].find('a').get_text()
CafeName = " ".join(CafeName.split())
print("접속 카페 : " + CafeName)
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

menuHREF = list()
menuNAME = list()

MenuIndex = 0
for divs in mydivs:
    for lis in divs.findAll('li'):
        MenuIndex += 1
        a = lis.find('a')
        MenuStr = " ".join(a.get_text().split())
        mElement = str(MenuIndex) + ' ' + MenuStr
        print(mElement)
        menuHREF.append(a['href'])
        menuNAME.append(MenuStr)
        
#E ####### Get Cafe Menu List ############


# S ####### Function Definitions ############



# E ####### Function Definitions ############

# def hasPage(chrome, page):
        
        
        

# Crawling Main Loop
cafeBaseURL = chrome.current_url
firstFlag = True
while(1):
    if(firstFlag == False):
        exitFlag = input("종료(1 - YES / 2 - NO) : ")
        if(exitFlag == '1'): break;

    MenuIndex = int(input('\n카페 메뉴의 번호 입력: '))
    startPage = int(input('크롤링 시작 페이지 번호 입력 : '))
    endPage = int(input('크롤링 끝 페이지 번호 입력 : '))
    
    #S ###### Go to the board user chose############
    chrome.get(cafeBaseURL + menuHREF[MenuIndex - 1])
    chrome.switch_to.frame('cafe_main')
    time.sleep(3)
    #E ###### Go to the board user chose############

    now = datetime.datetime.now()
    CurrentDateTime = now.strftime("%Y-%m-%d %H시 %M분")
    fileTitle = CurrentDateTime + " "
    fileTitle += (CafeName + " " + menuNAME[MenuIndex - 1] + " " + str(startPage) + " "+ str(endPage))
    fileTitle += ".txt"
    fileTitle = changeStrForProperFileName(fileTitle)
    
    _chFile = 0
    

    #S ###### Crawl on the pages from start to end  ############
    fileWriteFirstFlag = True
    currentPage = startPage
    while(currentPage <= endPage):
            bCrawl, pageURL = GotoDestPage(chrome, currentPage)
            if (bCrawl == True):
                    if(fileWriteFirstFlag == True):
                            _chFile = open(fileTitle, "wt", encoding='UTF8')
                            _FileTag = "Time : " + CurrentDateTime + "\n"
                            _FileTag += "Cafe : " + CafeName + r" / " + cafeBaseURL + "\n"
                            _FileTag += "Menu : " + menuNAME[MenuIndex - 1] + r" \ " + cafeBaseURL + menuHREF[MenuIndex - 1] + "\n"
                            _chFile.write(_FileTag)
                            fileWriteFirstFlag = False
                     
                    
                    article_list = chrome.find_elements_by_css_selector('span.aaa > a.m-tcol-c')
                    article_urls = [i.get_attribute('href') for i in article_list]

                    print("Page " + str(currentPage) + " Crawling...")
                    for article in article_urls:
                        chrome.get(article)
                        chrome.switch_to.frame('cafe_main')
                        chrome.implicitly_wait(3)
                        soup = BeautifulSoup(chrome.page_source, 'html.parser')


                        content = "[\n"
                        content += "\t Page : " + str(currentPage) + "\n"
                        
                        content += "\t 제목 : " + soup.select('div.tit-box span.b')[0].get_text() + "\n"

                        content_tags = soup.select('#tbody p')
                        content += "\t 내용 : "
                        content += ' '.join([tags.get_text() for tags in content_tags])
                        content += "\n"

                        content += "\t 댓글 : "
                        content += "\n"

                        content += "\t 링크 : " + article + "\n"
                        content += "]\n"
                        
                        _chFile.write(content)
            
            else:
                    print('크롤링 할 페이지가 없습니다')
                    break;
            chrome.get(cafeBaseURL + pageURL)
            chrome.switch_to.frame('cafe_main')
            time.sleep(3)
            currentPage += 1
    #E ###### Crawl on the pages from start to end  ############
    if(fileWriteFirstFlag == False):
            _chFile.close()
    firstFlag = False

# Crawling Main Loop
