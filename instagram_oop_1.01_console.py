import sys
import os
import re
import random
import time
import winsound
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
import datetime
import imaplib
import urllib3
import requests


class instaClicker:
    html = 'https://vk.com/honor5?w=wall6864019_13264%2Fall'
    html2 = 'https://www.instagram.com/accounts/login/?source=auth_switcher'
    count = 0
    count_fail=0
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3729.169 Safari/537.36')
    driver = None
    user = ''
    login = ''
    password = ''
    login1 = 'HMobileShots'
    password1 = 'GJPjL2wX'
    login2 = 'Hon0r5'
    password2 = 't%v8X^bR'
    email = ''
    email_password = ''
    email1 = '2335045T@gmail.com'
    email1_password = 'RyOQiD20SHnf'
    email2 = '2335045@gmail.com'
    email2_password = 'O0%gi8$!Ci'
    set_count = 0
    timeLastStart = ''
    delay = 0

    def __init__(self, headless=1, user='HMobileShots', password='GJPjL2wX', set_count=9):
        self.set_count = set_count
        # check which user chouse
        if user == 'Hon0r5':
            self.user = 'Hon0r5'
            self.login = self.login2
            self.password = self.password2
            self.email = self.email2
            self.email_password = self.email2_password
        elif user == 'HMobileShots':
            self.user = 'HMobileShots'
            self.login = self.login1
            self.password = self.password1
            self.email = self.email1
            self.email_password = self.email1_password
        else:
            self.user = user
            self.login = user
            self.password = password

        if self.check():
            if headless == 1:
                self.driver = webdriver.Chrome('lib\chromedriver.exe', options=self.options)
                self.delay = 2.5
            else:
                self.driver = webdriver.Chrome('lib\chromedriver.exe')
            self.driver.set_page_load_timeout(45)
            self.delay = 1.2

    def __del__(self):
        self.driver.quit()
        try:
            self.driver.quit()
        except:
            print('fail self.driver.quit()')
        # del self.driver
        print('__del__')

    def check(self):
        self.loads()  # read list of tags
        # check passed hour from the moment last work of script or not, if yes logging in account, if not wait
        time1 = float(self.timeLastStart)
        time2 = float(time.mktime(datetime.datetime.now().timetuple()))
        timeZap = time2 - time1
        if timeZap < 0:
            timeZap *= -1
        if timeZap < 3600:
            print('sorry from the last run, not yet hour, wait', 3600 - timeZap, ' seconds')
            time.sleep(3600 - timeZap)
        else:
            print('all okay, program run and now logging user')
            pass
        return 1

    def main(self):
        url = 'https://www.instagram.com/'
        listoftags = []
        url2 = url + 'accounts/login/?source=auth_switcher'
        count = 0

        self.flogin(url2, login=self.login, password=self.password)  # logging in instagram

        start_time = time.time()
        for i in self.listoftags[:self.set_count]:
            try:
                inst.fsearch(url, i)  # find page with tags
                cont = self.likedAndCommentPosts(commentYN=0)  # лайкаем 3 лучших и 6 новых фото
                print('tags', i, 'liked - ', cont)
                time.sleep(3)
            except(BaseException):
                self.__del__()
                if self.count_fail == 0:
                    self.__init__()
                    print('program error we try again, please wait')
                    self.main()
                else:
                    print('sorry, second try fail, program is closed')
                    exit()


            count = count + cont
            cont = 0

        end_time = time.time() - start_time  # find and write time of work script
        print('by all tag\'s liked photo - ', count)
        print('Program run -', round(end_time) // 60, 'min :', round(end_time) % 60, 'sec in - ',
              datetime.datetime.now().time())
        print('for user - ', self.user)
        if self.count > 2:
            with open('info\\' + self.login + '_end.txt', 'w+', encoding='utf-8') as file_d:
                file_d.write(str(float(time.mktime(datetime.datetime.now().timetuple()))))
            # write time last work script in file
            winsound.Beep(440, 450)
        # inst.__del__()  # close driver
        exit(0)

    def tosec(self, time):
        sum = ((int(time[:2])) * 3600) + ((int(time[3:5])) * 60) + (int(time[6:8]))
        return sum

    def loads(self):  # loads all data from file
        file1 = list()
        with open('info\\ListOfTags.txt', 'r', encoding='utf-8') as file:
            self.listoftags = file.read().split('\n')
            random.shuffle(self.listoftags)
            if self.listoftags:
                print('list of tags load successful, count - ', len(self.listoftags))
        if os.path.exists('info\\' + str(self.login) + '_end.txt'):
            with open('info\\' + str(self.login) + '_end.txt', 'r', encoding='utf-8') as file2:
                self.timeLastStart = file2.read()
        else:
            with open('info\\' + str(self.login) + '_end.txt', 'w+', encoding='utf-8') as file2:
                file2.write(str((time.mktime(datetime.datetime.now().timetuple())) - 3650))
                self.timeLastStart = file2.read()


    if not os.path.exists:
        with open('logs\ListOfLikedUrltest.txt', 'w+', encoding='utf-8') as file1:
            pass

    def flogin(self, url, login, password):
        self.driver.implicitly_wait(10)
        self.driver.get(url)
        elemname = self.driver.find_elements_by_name('username')
        elemname[0].send_keys(str(login))  # log
        elemname = self.driver.find_elements_by_name('password')
        elemname[0].send_keys(str(password))  # pass)
        elemname = self.driver.find_elements_by_xpath(
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button')
        if not elemname:
            print('not find button')
            self.driver.quit()
            time.sleep(1000)
            self.main(user=self.user, set_count=self.set_count)
        try:
            elemname[0].click()
        except IndexError:
            self.driver.quit()
            winsound.Beep(440, 300)
            winsound.Beep(440, 300)
            winsound.Beep(440, 300)
            print('error log, try again')
        except TimeoutException as e:
            # Handle your exception here
            print(e)
        except BaseException:
            print('other')

        try:
            elemname = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/div/div/p')
            if elemname.text == 'Чтобы защитить ваш аккаунт, мы отправим вам код безопасности для подтверждения личности. Как вы хотите его получить?':
                # click and send mail
                if str(self.driver.find_element_by_xpath('//*[@id="react-root"]/section/div/div/div[3]/form/div/div[2]/label').text).find('Эл. адрес: ')!=-1:
                    elemname = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/div/div/div[3]/form/div/div[2]/label')
                    elemname.click()
                else:
                    time.sleep(200)
                    print('Sorry, we dont find button choice path of confirmation, we try again, if that not be success, please refer to developer')
                    self.driver.quit()
                    self.driver = None
                    if self.count_fail == 0:
                        print('Program will be try again')
                    self.count_fail = self.count_fail + 1
                    self.main()
                    if self.count_fail > 0:
                        print('Second try fail, program will be closed')
                        inst.__del__()

                        exit()
        except(NoSuchElementException):
            print('NoSuchElementException\n'
                  'choice path of confirmation')

        try:
            #click on button send code on email
            elemname = self.driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/div/div/div[3]/form/span/button')
            elemname.click()
            # insert code from email
            elemname = self.driver.find_element_by_xpath('//*[@id="security_code"]')
            time.sleep(15)
            elemname.send_keys(str(self.check_mail()))
            elemname = self.driver.find_element_by_xpath(
                '// *[ @ id = "react-root"] / section / div / div / div[2] / form / span / button')
            elemname.click()
            # time.sleep(200)
            # print('time.sleep(200)')
            if elemname.text == 'К сожалению, вы ввели неверный пароль. Проверьте свой пароль еще раз.' or elemname.text == 'Чтобы защитить ваш аккаунт, мы сбросили ваш пароль. ' \
                                                                                                                            'Нажмите «Забыли пароль?» на экране входа и следуйте инструкциям по восстановлению доступа к аккаунту.':
                print('Password incorrect or other problem in logging')
            elemname = self.driver.find_element_by_xpath('//*[@id="slfErrorAlert"]')
            if elemname.text == 'К сожалению, вы ввели неверный пароль. Проверьте свой пароль еще раз.' or elemname.text == 'Чтобы защитить ваш аккаунт, мы сбросили ваш пароль. ' \
                                                                                                                            'Нажмите «Забыли пароль?» на экране входа и следуйте инструкциям по восстановлению доступа к аккаунту.':
                print('Password incorrect or other problem in logging')
                if self.count_fail == 0:
                    print('we try logging again, please wait')
                    self.driver.quit()
                    self.main()
                else:
                    print('sorry, second try to logging fail, program is closed')
                    self.driver.quit()
                    exit()

                print('window unusual loging and check with mail is close!')
            else:
                print('error find window unusual loging and check with mail!')

        except(NoSuchElementException):
            print('NoSuchElementException\n'
                  'find field insert code')

        try:
            #check frame
            elemname = self.driver.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/div')
            if elemname.text == 'Моментально узнавайте о новых подписчиках, отметках "Нравится" и комментариях к вашим фото.':
                try:
                    elemname = self.driver.find_element_by_xpath(
                        '/html/body/div[3]/div/div/div[3]/button[2]')  # close  window notification
                    elemname.click()
                    print('notification window is closed!')
                except:
                    print('error on find window on main page')
        except(NoSuchElementException):
            print('NoSuchElementException')

        try:
            elemname = self.driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/div/div/p[1]')  # close  window with checked unusual logging try
            elemname = self.driver.find_element_by_xpath(
                '// *[ @ id = "react-root"] / section / div / div / div[3] / form / div[2] / span / button')
            elemname.click()
            print('window checked unusual logging try is close!')
        except:
            print('error on window checked unusual logging!')

        # проверка зашли ли мы
        # переходим в профиль и смотрим имя
        try:
            elemname = self.driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[3]/a')
            elemname.click()
            elemname = self.driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/header/section/div[1]/h1')
            if elemname.text.upper() == str(self.user).upper():
                print('Logged user - ', login, 'in instagram')
            else:
                if self.count_fail == 0:
                    print('error, user not logged, we try again, please wait')
                    self.driver.quit()
                    self.main()
                else:
                    print('sorry, second try to logging fail, program is closed')
                    self.driver.quit()
                    exit()
        except:
            print('error')

        self.driver.implicitly_wait(5)

    def fsearch(self, url, tag):
        # elemname = driver.find_elements_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div/div')
        urls = url + 'explore/tags/' + str(tag)
        self.driver.get(urls)
        html = self.driver.page_source
        elemname = self.driver.find_elements_by_xpath(
            '// *[ @ id = "react-root"] / section / nav / div[2] / div / div / div[2]')
        print('go by tag', tag)
        time.sleep(2)

    def checkheart(self, url):
        # print('link', url)
        self.driver.refresh()
        soup = self.driver.page_source  # get raw full html code
        checkboth = re.findall('aria-label="Не нравится"|aria-label="Unlike"', soup)  # check liked or not photo
        if not checkboth:
            print('unliked in ', url)
            return 1
        else:
            print('liked in', url)
            return 0

    def likedAndCommentPosts(self, commentYN=0):
        countf = 0
        for i in range(1, 4):
            try:
                elemname = self.driver.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[' + str(i) + ']')  # best foto
                elemname.click()
            except WebDriverException:
                print('err find and click on photo')
                break

            time.sleep(self.delay)

            if self.checkheart(self.driver.current_url):
                try:
                    elemname = self.driver.find_element_by_css_selector(
                        '#react-root > section > main > div > div > article > div.eo2As > section.ltpMr.Slqrh > span.fr66n > button > span')  # search button heart
                    time.sleep(2)
                    elemname.click()  # push
                    countf = countf + 1
                except:
                    print('error push heart on best foto')
                with open('logs\\' + str(self.user) + '_ListOfLikedUrl.txt', 'a', encoding='utf-8') as file1:
                    file1.write('\n' + self.driver.current_url)
                self.driver.back()  # close photo
                time.sleep(self.delay)
            else:
                time.sleep(self.delay)
                self.driver.back()
        for i in range(1, 4):
            for j in range(1, 3):
                try:
                    elemname = self.driver.find_element_by_xpath(
                        '//*[ @ id = "react-root"]/section/main/article/div[2] / div / div[' + str(
                            i) + '] / div[' + str(j) + ']')  # new foto
                    elemname.click()
                except:
                    print('err')
                    break
                time.sleep(self.delay)
                if self.checkheart(self.driver.current_url):
                    try:
                        elemname = self.driver.find_element_by_css_selector(
                            '#react-root > section > main > div > div > article > div.eo2As > section.ltpMr.Slqrh > span.fr66n > button > span')  # serch button heart

                        time.sleep(self.delay)
                        elemname.click()  # push
                        countf = countf + 1
                    except:
                        print('error push heart on new foto')

                    with open('logs\\' + str(self.user) + '_ListOfLikedUrl.txt', 'a', encoding='utf-8') as file1:
                        file1.write('\n' + self.driver.current_url)

                    self.driver.back()  # close photo
                else:
                    self.driver.back()
                    time.sleep(self.delay)

        return countf

    def check_mail(self):
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(self.email, self.email_password)
        mail.list()
        mail.select("inbox")  # Подключаемся к папке "входящие".
        result, data = mail.search(None, "ALL")

        ids = data[0]  # Получаем сроку номеров писем
        id_list = ids.split()  # Разделяем ID писем
        latest_email_id = id_list[-1]  # Берем последний ID

        result, data = mail.fetch(latest_email_id, "(RFC822)")  # Получаем тело письма (RFC822) для данного ID

        raw_email = data[0][1]  # Тело письма в необработанном виде

        # включает в себя заголовки и альтернативные полезные нагрузки
        answ = re.findall(r'<font size=3D\"6\">.*<\/font>', str(raw_email))
        print('Secure code from email  - ', answ[0][17:23])
        answ = answ[0][17:23]
        return answ

    def updatedriver(self):
        urllib3.util.connection
        requests.get()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        user1 = 'Hon0r5'
        user2 = 'HMobileShots'
        set_countlocal = 2
        inst = instaClicker(headless=0, user=user1, set_count=set_countlocal)
        inst.__del__()
        # inst.main()
        # a = input()
    else:
        inst = instaClicker(headless=0, user=str(sys.argv[1]), password=str(sys.argv[2]), set_count=10)
        inst.main()
