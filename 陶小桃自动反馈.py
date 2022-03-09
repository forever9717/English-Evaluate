from selenium import webdriver
from PIL import Image
import pytesseract
from pytesseract import *
from bs4 import BeautifulSoup
from datetime import timedelta
from datetime import date
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time 
import schedule
import os 
import shutil
def submit():
    global driver,study_info,student_situation_url,chrome_options
    chrome_options=Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1366x768')
    driver=webdriver.Chrome(options=chrome_options)
    driver.get('https://xx.dchixj.com/studyAdmin/sso/login;jsessionid=95610F7DD10C4BAF1EED68415BFC0504')
    account=driver.find_elements_by_tag_name("input")
    account[0].send_keys('LWC15059905685')
    account[1].send_keys('LWC15059905685')
    driver.save_screenshot('验证码.png')
    im=Image.open('验证码.png')
    im=im.crop((732,392,784,418))
    im.save('验证码.png')
    text=pytesseract.image_to_string('验证码.png')
    account[2].send_keys(text)
    driver.implicitly_wait(5)
    driver.maximize_window()
    study_info=driver.find_element_by_xpath('/html/body/div[1]/nav/div[2]/div[1]/ul/li[8]/a')
    student_situation_url=study_info.get_attribute('href')
    study_info.click()
    driver.implicitly_wait(5)
    driver.switch_to.frame('iframe4')
#登陆
class select_people():
    def caculate_time(self):#获得执行开始这一个星期的日期列表
        self.d=date.today()
        self.submit_time=[]
        for i in range(7):#需要评测的时间段
            delta=timedelta(days=i)
            time_1=self.d-delta
            self.submit_time.append(time_1.strftime('%Y-%m-%d'))
        return self.submit_time
    def select(self):#筛选,获取第一面板的数据
        global select_student
        select_student=[]
        driver.get(student_situation_url)
        for i in range(10):#翻的第一面板的页数
            driver.get(driver.current_url)
            pagesource=driver.page_source
            soup=BeautifulSoup(pagesource,'html.parser')
            student_situation_list=soup.find_all('tr')  
            for m in student_situation_list[1:11]:#一页十行的数据
                student_list=m.find_all('td')
                data=student_list[7].text.split()
                if data==[]:
                    pass
                elif data[0] in self.submit_time:
                    student_situation=[str(data[0]),student_list[3].text,student_list[9].find('a')['href'],student_list[10].find('a').text,student_list[11].find('a')['href'],[],[],[],[],[],[],[]]
                    select_student.append(student_situation)  
            page_info=driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div[2]/div[2]/div/input[2]')
            page_info.clear()
            page_info.send_keys(str(i+2))
            driver.implicitly_wait(5)
            turning_page=driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div[2]/div[2]/div/input[3]')
            turning_page.click()
            driver.implicitly_wait(5)
        return select_student
    def accquire_studytime(self):#记录学习时间，第二面板的数据
        for  i in range(len(select_student)):
            driver.get('https://xx.dchixj.com'+select_student[i][2])
            pagesource=driver.page_source
            soup=BeautifulSoup(pagesource,'html.parser')
            time_situation=soup.find_all('tr')                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
            if time_situation[1].find('td').text==str(1):
                select_student[i][2]=[[i.find_all('td')[1].text,i.find_all('td')[2].text]   for i in time_situation[1:] ]
            else:
                select_student[i][2]=[[time_situation[1].text]]
     
    def value_set_test(self):
        if self.record_type_wrong==[]:
            if self.record_time_less==[]:
                if self.record_time_more==[]:
                    for g in range(len(self.set_caulate)):
                        if self.set_caulate[g]<5:
                            value_test.append(self.set_study_info[g][0]+' 自主测试成绩没有达标哦！要连续5次96分以上哈。先去复习单词本再来挑战吧。')
                        else:
                            value_test.append(self.set_study_info[g][0]+' 自主测试成绩达标啦！你真是个平平无奇的小天才。')
                else:
                    for ee in range(len(self.set_caulate)):
                        
                        if self.set_caulate[ee]<5:
                            value_test.append(self.set_study_info[ee][0]+' 自主测试成绩没有达标哦！要连续5次96分以上哈。测试时间也过长了哈，正常是8分钟以内。说明单词还是很生疏，并且做选项的时候不要犹豫，一定要根据自己的第一直觉力去迅速判断选择答案，否则会造成刻意回忆单词，形成左脑记忆。')
                        else:
                            value_test.append(self.set_study_info[ee][0]+' 自主测试成绩达标啦！可惜用时太长了，正常用时是8分钟以内哦。说明单词还是很生疏，并且做选项的时候不要犹豫，一定要根据自己的第一直觉力去迅速判断选择答案，否则会造成刻意回忆单词，形成左脑记忆。')
            else:
                for aa in range(len(self.set_caulate)):
                    if self.set_caulate[aa]<5:
                        value_test.append(self.set_study_info[aa][0]+' 自主测试成绩没有达标哦！要连续5次96分以上哈。这么快就完成了测试，是不是没有认真按流程好好复习单词本啊，要把单词本里的生词，一般词，熟词三栏都复习完以后，再来做自主测试。复习好的判断标准是，生词和一般词点开为空，不这样的话我们自主测试的单词就是不完整的，测试成绩就不准确了哦。')
                    else:
                        value_test.append(self.set_study_info[aa][0]+' 自主测试成绩是达标了，可是我们的测试成绩有点问题哦。这么快就完成了测试，是不是没复习完单词本就来做自主测试了啊。复习单词本要把单词本里的生词，一般词，熟词三栏都复习完以后，再来做自主测试。复习好的判断标准是，生词和一般词点开为空。否则我们自主测试的单词数就不完整了。')
        else:
            if self.record_time_less==[]:
                if self.record_time_more==[]:
                    for bb in range(len(self.set_caulate)):
                        if self.set_caulate[bb]<5:
                            value_test.append(self.set_study_info[bb][0]+' 自主测试成绩没有达标哦！要连续5次96分以上哈，还有测试类型要记得选熟词测试哦，不然测的单词数就不完整了。先去复习单词本再来挑战吧。')
                        else:
                            value_test.append(self.set_study_info[bb][0]+' 自主测试成绩是达标了，可是我们的测试成绩有点问题哦，要记得测试类型要选熟词测试哦！不然测的单词数就不完整了。')
                else:
                    for dd in range(len(self.set_caulate)):
                        if self.set_caulate[dd]<5:
                            value_test.append(self.set_study_info[dd][0]+' 自主测试成绩没有达标哦！要连续5次96分以上哈，测试类型也要记得选熟词测试哦，不然测的单词数就不完整了。测试时间过长了哈，正常是8分钟以内。说明单词还是很生疏，并且做选项的时候不要犹豫，一定要根据自己的第一直觉力去迅速判断选择答案，否则会造成刻意回忆单词，形成左脑记忆。')
                        else:
                            value_test.append(self.set_study_info[dd][0]+' 自主测试成绩达标啦！可是我们的测试成绩有点问题哦，要记得测试类型要选熟词测试哦！不然测的单词数就不完整了。用时也太长啦，正常是8分钟以内。并且做选项的时候不要犹豫，一定要根据自己的第一直觉力去迅速判断选择答案，否则会造成刻意回忆单词，形成左脑记忆。')
            else:
                for ff in range(len(self.set_caulate)):
                    if self.set_caulate[ff]<5:
                        value_test.append(self.set_study_info[ff][0]+' 自主测试成绩没有达标哦！要连续5次96分以上哈，测试类型也要记得选熟词测试哦。这么快就完成了测试，是不是没有好好按流程好好复习单词本啊，要把单词本里的生词，一般词，熟词三栏都复习完以后，再来做自主测试。复习好的判断标准是，生词和一般词点开为空，不这样的话我们自主测试的单词就是不完整的，测试成绩就不准确了哦。')
                    else:
                        value_test.append(self.set_study_info[ff][0]+' 自主测试成绩是达标了，可是我们的测试成绩有点问题哦。这么快就完成了测试，是不是没复习完单词本就来做自主测试了啊，测试类型也要记得选熟词测试哦。复习单词本要把单词本里的生词，一般词，熟词三栏都复习完以后，再来做自主测试。复习好的判断标准是，生词和一般词点开为空。否则我们自主测试的单词数就不完整了。')
        return value_test
    def value_unit_test(self):
        g=0
        for f in self.unpass_equal_three:
            if f not in self.record_pass:
                g+=1
        if g==len(self.unit_study_list):
            if g>=3:
                value_test.append('有认真按照要求学习，但是今天的单元测试都没有通过而且数量有点多哦。是打字速度跟不上还是记得很吃力，学习过程中如果遇到问题要及时告诉老师的哈！')
            else:
                value_test.append('有按照要求认真学习，就可惜今天的单元测试都没通过，下次加油哦！')
        else:
            if g>=3:
                value_test.append('今天的单元测试通过率有点低哦。是打字速度跟不上还是记得很吃力，学习过程中如果遇到问题要及时告诉老师的哈！')
        a=0
        if self.unpass_more_three!=[]:
            for l in range(len(self.unpass_more_three)):
                if self.unpass_more_three[l] not in self.record_pass:
                    a+=1
                self.value_unpass_more_three+=self.unpass_more_three[l]
            value_test.append('不要贪心哦！'+self.value_unpass_more_three+'单元测试累计满三次不过就先学习下一单元，以免影响学习进度。做测试的过程中不要太过于在意测试成绩，否则会使右脑记忆变成左脑的死记硬背哦！等学完这一册书还要记得回来补测，补测的时候要先把学习，听读，复习三个流程都过了之后再做单元测试哈。')
        if self.unpass_less_three!=[]:
            for  k in range(len(self.unpass_less_three)):
                self.value_unpass_less_three+=self.unpass_less_three[k]
            value_test.append(self.value_unpass_less_three+'单元测试没通过，要记得累积测满三次哦！')
        if self.unit_study_list!=[['无']]:
            if self.record_unpass==[]:
                if self.record_pass!=[]:
                    value_test.append('单元测试全都一次通过啦！你真厉害！')
                else:
                    value_test.append('没及时做单元测试，背完单词要及时做单元测试巩固哦！')
            if self.record_unpass!=[]:
                if len(self.reach_list)==len(self.unpass_less_three) and g==0 and a==0:
                    value_test.append('学习的内容都按照要求完成了任务，真棒，加油!下次争取一次性通过。')
        return value_test
    def value_score(self):
        global value_test
        #遍历每一个选中的学生
        for  i in range(len(select_student)):
            
            driver.get('https://xx.dchixj.com'+select_student[i][4])#打开测试面板
            value_test=[]#记录评语
            #获取强制单元测试的数据
            
            pagesource=driver.page_source
            soup=BeautifulSoup(pagesource,'html.parser')
            if  soup.find_all('tr')[1].find('td').text==str(1):
               value_force_test=soup.find_all('tr')[1].find_all('td')[6].text.split()
            else:
                value_force_test=[soup.find_all('tr')[1].text]
            
            #获取单元测试的数据
            unit_info=driver.find_element_by_xpath('/html/body/div/div[1]/div/div/a[2]').get_attribute('href')
            driver.get(unit_info)
            time.sleep(10)
            driver.save_screenshot('C:\\Users\\Administrator\\Desktop\\陶小桃自动反馈脚本\\图片\\'+str(self.d)+select_student[i][1]+'.png')
            unit_test_info=[]#记录学习的单元以及通过情况
            unit_study_info=[]#记录学习的单元
            self.record_unpass=[]#记录不通过的单元
            self.record_pass=[]#记录通过的单元
            self.caculate_list=[]#计算次数
            self.reach_list=[]#记录三次内通过的单元
            self.unit_study_list=[]
            for w in range(3):#翻三页
                driver.get(driver.current_url)
                pagesource=driver.page_source
                soup=BeautifulSoup(pagesource,'html.parser')
                unit_test=soup.find_all('tr')
                if len(unit_test)!=2 or (unit_test[1].find('td').text==str(1) and len(unit_test)==2):
                    for u in unit_test[1:11]:
                        unit_score=u.find_all('td')
                        if unit_score[6].text.split()[0]==select_student[i][0]:
                            unit_test_info.append([unit_score[1].text,unit_score[2].text,unit_score[5].text]) 
                        if  unit_score[6].text.split()[0] in self.submit_time:
                            select_student[i][7].append([[unit_score[1].text,unit_score[2].text],unit_score[3].text]) 
                            
                try:#翻页
                    page_info=driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div[2]/div/div/input[2]')
                    page_info.clear()
                    page_info.send_keys(str(w+2))
                    turning_page=driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div[2]/div/div/input[3]')
                    turning_page.click()   
                except:
                    break
            
            #记录自主测试的数据
            last_test=[['无敌基础新版单词(下）','unit 8'],['音标（下）','/j/'],['无敌基础新版单词(上）','unit 9'],['无敌基础新版单词(中）','unit 9'],['音标（上）','/k/'],
            ['高中人教第一册','unit 10'],['高中人教第二册','unit 9'],['高中人教第三册','unit 10'],['高中人教第四册','unit 10'],['高中人教第五册','unit 10'],['高中人教第六册','unit 12'],['高中人教第七册','unit 10'],['高中人教第八册','unit 15'],['高中人教第九册','unit 10'],['高中人教第十册','unit 11'],['高中人教第十一册','unit 11'],['高考拓展词组2','unit 10'],['高考拓展词汇2','unit 112'],
            ['闽教版三年级下','unit 8'],['闽教版四年级下','unit 8'],['闽教版五年级下','unit 8'],['闽教版六年级下', 'unit 8'],
            ['仁爱科普版七年级上册','Review of Unit3-4'],['仁爱科普版七年级下册','Unit8 Topic3'],['仁爱科普版八年级上册','Review of Unit3-4'],['仁爱科普版八年级下册','Review of Unit7-8'],['仁爱科普版九年级上册','Review of Unit3-4'],['仁爱科普版九年级下册','Review of Unit5-6'],['中考拓展词组','Unit19'],['中考拓展词汇','Unit59'],['英语语法掌中宝——初中过去式','Unit9'],
            ['中考拓展词汇（第一册）','unit 10'],['中考拓展词汇（第二册）','unit 10'],['中考拓展词汇（第三册）','unit 10'],['中考拓展词汇（第四册）','unit 10'],['中考拓展词汇（第五册）','unit 10'],['中考拓展词汇（第六册）','unit 9'],['中考核心必背600词汇（上）','unit 7'],['中考核心必背600词汇（中）','unit 8'],['中考核心必背600词汇（下）','unit 7']
            ]#每册书最后一单元内容
            set_info=driver.find_element_by_xpath('/html/body/div/div[1]/div/div/a[3]').get_attribute('href')
            driver.get(set_info)
            driver.implicitly_wait(5)
            set_test_info=[]
            try:
                for s in range(3):#翻的自主测试页面页数
                    driver.get(driver.current_url)
                    pagesource=driver.page_source
                    soup=BeautifulSoup(pagesource,'html.parser')
                    set_test=soup.find_all('tr')
                    if len(set_test)!=2 or (set_test[1].find('td').text==str(1) and len(set_test)==2):
                        for z in set_test[1:11]:
                            set_score=z.find_all('td')
                            if set_score[6].text.split()[0]==select_student[i][0]:
                                set_test_info.append([set_score[1].text,set_score[2].text,set_score[4].text,set_score[5].text])
                            if set_score[6].text.split()[0] in self.submit_time:
                                select_student[i][10].append([[set_score[1].text],set_score[3].text])
                    try:
                        page_info=driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div[2]/div/div/input[2]')
                        page_info.clear()
                        page_info.send_keys(str(s+2))
                        turning_page=driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div[2]/div/div/input[3]')
                        turning_page.click()                                                         
                    except:
                        break
                    
            except:
                pass
                                                                                             

            #评价测试成绩

           
            
            #自主测试数据的处理
            self.set_caulate=[]
            set_content=[i[0] for i in set_test_info]                                                
            self.set_study_info=[list(m) for m in list(set([tuple([i]) for i in set_content]))]#记录做的自主测试的单元
            self.record_type_wrong=[]
            self.record_time_less=[]
            self.record_time_more=[]
            if self.set_study_info==[]:
                pass
            else:
                for t in range(len(self.set_study_info)):
                    self.set_caulate.append(0)
                for e in range(len(self.set_study_info)):
                    #计算做的自主测试通过的次数 
                    for f in range(len(set_test_info)):
                        if self.set_study_info[e]==[set_test_info[f][0]]:
                            if set_test_info[f][3]=='\n通过\n':
                                self.set_caulate[e]+=1
                        #记录测试类型不对的单元
                        if set_test_info[f][1]!='\n\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t\t熟词\n\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t':
                            self.record_type_wrong.append(set_test_info[f][0])
                        #记录时间有问题的单元
                        if float(set_test_info[f][2][3:5])+float(set_test_info[f][2][6:])/60 < float(2.5):
                            self.record_time_less.append(set_test_info[f][0])
                        if float(set_test_info[f][2][3:5])+float(set_test_info[f][2][6:])/60 > float(8):
                            self.record_time_more.append(set_test_info[f][0])
                
            #消除重复的单元内容                    
            self.record_type_wrong=[list(m) for m in list(set([tuple([i]) for i in self.record_type_wrong]))]
            self.record_time_less=[list(m) for m in list(set([tuple([i]) for i in self.record_time_less]))]
            self.record_time_more=[list(m) for m in list(set([tuple([i]) for i in self.record_time_more]))]
            
            
            
            #单元测试的数据处理
            if unit_test_info!=[]:
                for z in range(len(unit_test_info)):
                    unit_study_info.append([unit_test_info[z][0],unit_test_info[z][1]])          
                    if unit_test_info[z][2]=='\n不通过\n': 
                        self.record_unpass.append([unit_test_info[z][0],unit_test_info[z][1]])
                    if unit_test_info[z][2]=='\n通过\n':
                        self.record_pass.append([unit_test_info[z][0],unit_test_info[z][1]])
            self.unit_study_list=[list(m) for m in list(set([tuple(i) for i in unit_study_info]))]
            #去除重复后的学习内容
            self.unpass_list=[list(m) for m in list(set([tuple(i) for i in self.record_unpass]))]
            #去除重复后的未通过的内容
            self.unpass_more_three=[]
            self.unpass_less_three=[]
            self.unpass_equal_three=[]
            self.value_unpass_more_three=''
            self.value_unpass_less_three=''
            for r in range(len(self.unpass_list)):
                self.caculate_list.append(0)
            for x in self.record_unpass:
                for y in range(len(self.unpass_list)):
                    if x==self.unpass_list[y]:
                        self.caculate_list[y]+=1
            for q in range(len(self.caculate_list)):
                if self.caculate_list[q]>3:
                    self.unpass_more_three.append(self.unit_study_list[q][0]+self.unit_study_list[q][1]+'  ')
                if self.caculate_list[q]<3:
                    if self.unit_study_list[q] not in self.record_pass:
                        self.unpass_less_three.append(self.unit_study_list[q][0]+self.unit_study_list[q][1]+'  ')
                    else:
                        self.reach_list.append([self.unit_study_list[q][0],self.unit_study_list[q][1]])
                if self.caculate_list[q]==3:
                    self.unpass_equal_three.append([self.unit_study_list[q][0],self.unit_study_list[q][1]])

                        
              
            #评估数据
            select_student[i][9]=[int(m[16:]) for m in select_student[i][5] if m[0:10]==select_student[i][0]]
            if select_student[i][0]==value_force_test[0]:
                if select_student[i][9]==[0]:
                    if unit_test_info==[]:
                        if set_test_info==[]:
                            select_student[i][7].append(['无'])
                            value_test.append('该同学只登陆后做了强制单元测试而没有学习')
                        else:
                            
                            self.value_set_test()
                            
                    else:
                       
                           
                        for v in self.unit_study_list:
                            if v in last_test:
                                if [v[0]] in self.set_study_info:
                                    self.value_set_test()
                                else:
                                    value_test.append('学完一册书以后要记得去做自主测试哦！做自主测试前要先去复习单词本，自主测试成绩要求是连续5次96分以上。')
                        self.value_unit_test()
                else:
                    if unit_test_info==[]:
                        if set_test_info==[]:
                            
                            value_test.append('学完新单词后要记得及时做单元测试哦！')
                        else:
                            
                            self.value_set_test()
                            
                    else:
                        
                        for c in self.unit_study_list:
                            if c in last_test:
                                if [c[0]] in self.set_study_info:
                                    self.value_set_test()
                                else:
                                    value_test.append('学完一册书以后要记得去做自主测试哦！做自主测试前要先去复习单词本，自主测试成绩要求是连续5次96分以上。')
                        self.value_unit_test()
            else:
                if select_student[i][9]==[0]:
                    if unit_test_info==[]:
                        if set_test_info==[]:
                            
                            value_test.append('该同学只登陆了陶小桃，其他什么也没有做。')
                        else:
                            
                            value_test.append('请不要关闭强制单元测试哦！这对学习很重要。')
                            self.value_set_test()
                            
                    else:
                        
                        value_test.append('请不要关闭强制单元测试哦！这对学习很重要。')
                        for v in self.unit_study_list:
                            if v in last_test:
                                if [v[0]] in self.set_study_info:
                                    self.value_set_test()  
                                else:
                                    value_test.append('学完一册书以后要记得去做自主测试哦！做自主测试前要先去复习单词本，自主测试成绩要求是连续5次96分以上。')
                        self.value_unit_test()

                else:
                    value_test.append('请不要关闭强制单元测试哦！这对学习很重要。')
                    if unit_test_info==[]:
                        if set_test_info==[]:
                            select_student[i][7].append(['无'])
                            value_test.append('学完新单词后要记得及时做单元测试哦！')
                        else:
                            
                            self.value_set_test()
                    else:
                        

                        for v in self.unit_study_list:
                            if v in last_test:
                                if [v[0]] in self.set_study_info:
                                    self.value_set_test()
                                else:
                                    value_test.append('学完一册书以后要记得去做自主测试哦！做自主测试前要先去复习单词本，自主测试成绩要求是连续5次96分以上。')
                        self.value_unit_test()

            select_student[i][6]=value_test
            


    def count_word(self):#背单词数的记录和评价
        driver.back()
        study_info=driver.find_element_by_xpath('/html/body/div[1]/nav/div[2]/div[1]/ul/li[8]/a')
        study_info.click()
        driver.switch_to.frame('iframe4')
        driver.implicitly_wait(5)
        for n in range(10):#第一面板翻三页
            for m in range(1,11):#一页十行
                location=driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/table/tbody/tr['+str(m)+']/td[4]').text
                for l in range(len(select_student)):
                    if location==select_student[l][1]:
                        number=driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/table/tbody/tr['+str(m)+']/td[11]/a')
                        number.click()
                        driver.implicitly_wait(5)
                        record_word=[]
                        for i in range(7):#一周七次
                            x=1100-120*i
                            ActionChains(driver).move_by_offset(x,385).click().perform()
                            driver.implicitly_wait(5)
                            record_word.append(driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div/div/div[2]').text)
                            driver.implicitly_wait(5)
                            ActionChains(driver).move_by_offset(-x,-385).click().perform()
                        select_student[l][5]=record_word
                        driver.find_element_by_xpath('/html/body/div/div/div[1]/div/div[2]/a').click()
            page_info=driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div[2]/div[2]/div/input[2]')
            page_info.clear()
            page_info.send_keys(str(n+2))
            driver.implicitly_wait(5)
            turning_page=driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div[2]/div[2]/div/input[3]')
            turning_page.click()
            driver.implicitly_wait(5)
    def __init__(self):#初始化
        self.caculate_time()
        self.select()
        self.count_word()
        self.accquire_studytime()
        self.value_score()
def write_txt():#写入txt
    with open('c:\\Users\\Administrator\\Desktop\\陶小桃自动反馈脚本\\陶小桃反馈.txt','w',encoding='utf-8') as f:
        f.write('数据截止至   '+datetime.now().strftime('%Y-%m-%d %H:%S')+'\n\n')
        for i in range(len(select_student)):#遍历每一个学生
            f.write('姓名：'+select_student[i][1]+'\n')
            f.write('背单词总数：'+select_student[i][3]+'个\n')
            numword=[int(x[16:]) for x in select_student[i][5]]
            f.write('一周单词量：\n')
            if numword!=[0,0,0,0,0,0,0]:
                for h in range(7):#一周七天
                    if select_student[i][5][h]!='':
                        if int(select_student[i][5][h][16:])==0:
                            pass
                        else:
                            f.write(select_student[i][5][h][0:10]+' '+select_student[i][5][h][16:]+'个')
                            for y in select_student[i][2]:
                                if y[0]==select_student[i][5][h][0:10]:
                                    if len(y[1])>3:
                                        for u in range(len(y[1])):
                                            if y[1][u]=='分':
                                                time=int(y[1][:u])+float(y[1][u+1:-1])/60
                                    else:
                                        time=float(y[1][0:-1])/60 
                                    f.write('   '+str(float(select_student[i][5][h][16:])/time)[:4]+'个/分钟\n')
            else:
                f.write('本周无新背诵单词\n')
        
            f.write('一周学习内容：\n')
            if select_student[i][10]!=[]:
                f.write('自主测试：\n')
                set_content_1=[list(m) for m in list(set([tuple(n[0]) for n in select_student[i][10]]))]
                for pp in set_content_1:
                    set_score_1=[x[1] for x in select_student[i][10] if x[0]==pp]
                    select_student[i][11].append([pp[0],set_score_1])
                for rr in select_student[i][11]:
                    f.write(rr[0]+': ')
                    for ww in range(len(rr[1])):
                        if ww!=len(rr[1])-1:
                           f.write(rr[1][ww]+'/')
                        else:
                            f.write(rr[1][ww]+'分')
                    f.write('\n')
                 



            unit_content_1=[list(m) for m in list(set([tuple(n[0]) for n in select_student[i][7]]))]
            for ss in unit_content_1:
                if ss!='无':
                    unit_score_1=[x[1] for x in select_student[i][7] if x[0]==ss] 
                    
                    select_student[i][8].append([ss,unit_score_1])

            if select_student[i][8]!=[]:
                f.write('单元测试:\n')
                for yy in select_student[i][8]:
                    if yy[0][0]!='无':    
                        f.write(yy[0][0]+yy[0][1]+': ')
                        for ll in range(len(yy[1])):
                            if ll!=len(yy[1])-1:
                                f.write(yy[1][ll]+'/')
                            else:
                                 f.write(yy[1][ll]+'分')
                    else:
                        if len(select_student[i][8])==1:
                            f.write('无')
                        else:
                            continue
                    f.write('\n')
            if select_student[i][10]==[] and  select_student[i][8]==[]:
                f.write('本周无测试成绩')
       


                     
            f.write('\n最近一次学习评语：\n')
            if len(select_student[i][6])==0:
                f.write('你表现得太好啦，都让我无话可说了！\n')
            if len(select_student[i][6])==1:
                f.write(select_student[i][6][0]+'\n')
            else:
                for m in range(len(select_student[i][6])):
                    f.write(str(m+1)+'. '+select_student[i][6][m]+'\n')
            f.write('-------------------------------\n')
file_name='C:/Users/Administrator/Desktop/陶小桃自动反馈脚本'
if not os.path.isdir(file_name):
    os.makedirs(file_name)
if  os.path.isdir(file_name+'/图片'):
    shutil.rmtree(file_name+'/图片')
    os.makedirs(file_name+'/图片')
else:
    os.makedirs(file_name+'/图片')
condition=0
start=time.time()
while condition==0:
    end=time.time()
    if end-start<100000:
        try:
            print('先去喝杯茶吧，别等我啦，我可没那么快！') 
            submit()
            select_people()
            write_txt()
            driver.close()
            print('我好啦，快去文件夹看看我吧！')
            condition=1
        except:
            print('我好像遇到一点问题了，再等等我！')
            time.sleep(10)
            driver.save_screenshot('C:\\Users\\Administrator\\Desktop\\陶小桃自动反馈脚本\\bug.png')
            driver.close()
    else:
        print('啊呀，我奔溃了！\n 请先尝试重新运行，无效再尝试重启。还不行的话就只能去求助我的母上大人阿琼')
        time.sleep(30)
        with open('c:\\Users\\Administrator\\Desktop\\陶小桃自动反馈脚本\\陶小桃反馈.txt','w',encoding='utf-8') as f:
            f.write('发生bug时间：'+datetime.now().strftime('%Y-%m-%d %H:%S')+'\n')
            f.write('警报！！！\n 程序出现不明bug,已经超出我的能力范畴！\n 请先尝试重新运行，无效再尝试重启。再不行的话就只有我伟大的母上大人阿琼能拯救我了，请在非休息时间把bug图片发给她。')
    