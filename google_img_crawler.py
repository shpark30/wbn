from bs4 import BeautifulSoup as bs
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
import time
import sys


class google_img_crawler:

    quit_msg = "q"
    backward_msg = "b"

    def __init__(self):
        self.result_dict = {}
        self.ctl_cmd = None

    def _input_stage(self):
        """
        1. _input_stage 함수의 self.input_dict에 필요한 정보를 업데이트한다.
        2. 필요한 정보를 crawl함수에 
        """
        self.input_dict = {"input1": '검색하고 싶은 키워드 : ',
                           "input2": '다운로드 할 이미지 개수 : ',
                           "input3": '다운로드 받을 디렉토리 : ',
                           "input4": '저장할 이미지 파일 이름(공백 가능) : ',
                           "input5": '저장할 이미지 파일 확장자명 : '}
        '''self.input_dict = {"input1": f"input('{(self.input1_msg := '검색하고 싶은 키워드')} : ')",
                           "input2": f"input('{(self.input2_msg := '다운로드 할 이미지 개수')} : ')",
                           "input3": f"input('{(self.input3_msg := '다운로드 받을 디렉토리')} : ')",
                           "input4": f"input('{(self.input4_msg := '저장할 이미지 파일 이름(공백 가능)')} : ')",
                           "input5": f"input('{(self.input5_msg := '저장할 이미지 파일 확장자명')} : ')"}'''

        #
        next_stage_num = 2
        input_num = 1
        print("\n이전 단계부터 다시 입력하고 싶다면 b, 프로그램을 중단하고 싶다면 q를 입력하세요.")
        while True:
            print("\n" + (sequence := f"input{input_num}"))
            input_msg = self.input_dict.get(sequence)
            info = input(input_msg)
            self.result_dict[sequence] = info
            if input_num == 1:
                print(
                    f"url에서 이미지를 확인하세요\n : https://www.google.com/search?q={info}&hl=ko&tbm=isch")

            if input_num > 1 and info == self.backward_msg:
                input_num -= 1
            elif info == self.quit_msg:
                self.ctl_cmd = self.quit_msg
                break
            else:
                input_num += 1

            if input_num == len(self.input_dict)+1:
                break

        return next_stage_num

    def _check_stage(self):
        print("\n", *[self.input_dict[f"input{str(i+1)}"] +
                      self.result_dict[f"input{str(i+1)}"] for i in range(len(self.input_dict))], sep="\n")
        check_items = input(
            f"위의 정보가 맞습니까?\n진행[y]/리셋[{self.backward_msg}]/중단[{self.quit_msg}]]")
        if check_items == 'y':
            next_stage_num = 3
        elif check_items == self.backward_msg:
            next_stage_num = 1
        elif check_items == self.quit_msg:
            self.ctl_cmd = self.quit_msg
            return None
        else:
            next_stage_num = 2
        return next_stage_num

    def _crawl_stage(self):
        next_stage_num = 4
        search_name, img_num, download_path, file_name, file_extension = [
            self.result_dict[f"input{str(n+1)}"] for n in range(len(self.result_dict))]
        self.scrap_by_selenium(search_name, img_num,
                               download_path, file_name, file_extension)
        return next_stage_num

    def _quit_program(self):
        if self.ctl_cmd == self.quit_msg:
            print("quit")
            quit()
            sys.exit("이미지 크롤러를 종료합니다.")
            # 파이썬 프로그램 종료하는 법
        else:
            print("다음 단계를 진행합니다.")

    def process_step(self):
        stage_dict = {"stage1": f"self._input_stage()",
                      "stage2": f"self._check_stage()",
                      "stage3": f"self._crawl_stage()"}

        stage_num = 1
        while True:
            stage_func = stage_dict.get(f"stage{stage_num}", None)
            stage_num = eval(stage_func)
            self._quit_program()
            if stage_num > len(stage_dict):
                break
        print("이미지 수집을 완료했습니다.")
        return None
        '''   if stage_num < t_step_cnt + 1:
                var = _single_step(stage_num)

            elif stage_num == t_step_cnt + 1:
                # print("\n", *[eval(f"step{str(i+1)}_msg") + " : " + self.result_dict[f"step{str(i+1)}"] for i in range(len(self.input_dict))], sep = "\n")
                print("\n", *[self.input_dict[f"step{str(i+1)}"][0] + " : " +
                              self.result_dict[f"step{str(i+1)}"] for i in range(len(self.input_dict))], sep="\n")
                check_items = input(
                    "위의 정보가 맞습니까? 'n'을 입력하면 처음부터 다시 시작합니다\n[y/n]")
                if check_items == 'y':
                    break
                elif check_items == 'n':
                    stage_num = 1
                else:
                    continue
            else:
                print("stage_num가 self.input_dict의 범위를 벗어났습니다. 디버깅해주세요.")
                var = quit_msg

            if var == quit_msg:
                break
            elif var == backward_msg:
                n -= 1
            else:
                n += 1

        return var'''

    def _doScrollDown(self, driver, limit):
        while True:
            driver.execute_script(
                'window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(0.5)
            try:
                more_result = driver.find_element_by_class_name("mye4qd")
                more_result.send_keys(Keys.RETURN)
            except:
                print("스크롤 열심히 내리고 있음")
            if len(driver.find_elements_by_tag_name("img")) > limit:
                break

    def scrap_by_selenium(self, search_name, img_num_want, download_path, file_name, file_extension):
        # 다운로드 경로 지정
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {
                                        "download.default_directory": repr(download_path),
                                        "excludeSwitches": ['enable-logging']})
        # 브라우저 오픈
        driver = webdriver.Chrome(
            'C:/Users/seohy/chromedriver.exe', chrome_options=options)
        driver.get("https://www.google.co.kr/imghp?hl=ko&tab=ri&authuser=0&ogbl")

        # 검색어 입력
        elem = driver.find_element_by_name("q")
        elem.clear()
        elem.send_keys(search_name)
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source

        # 원하는 이미지 개수를 만족할 때까지 스크롤
        self._doScrollDown(driver, int(img_num_want))
        img_list = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")

        # 이미지 다운로드
        for i, img in enumerate(img_list):
            # get image src
            # img.click() # via the webdriver element click.
            # its a click done via javascript
            driver.execute_script("arguments[0].click();", img)
            time.sleep(0.1)
            target = driver.find_element_by_css_selector(".n3VNCb")
            target_src = target.get_attribute("src")

            # download
            urllib.request.urlretrieve(
                target_src, file_name + str(i) + "." + file_extension)

            # target.context_click().send_keys("v")
            # driver.send_keys(file_name + str(i) + "." + file_extension)
            # driver.send_keys(Keys.ENTER)
        driver.close()

    def scrap_by_bs(self, search_name, img_num_want=None, download_path=None,
                    file_name="", file_extension="png"):
        url = "https://www.google.com/search?q=" + search_name + "&hl=ko&tbm=isch"
        browser = webdriver.Chrome('C:/Users/SEOHYEONPARK/chromedriver.exe')
        browser.get(url)
        img_num_want = int(img_num_want) if img_num_want else 0
        while True:
            loading = input("\n브라우저의 스크롤을 내려서 이미지를 로드하세요. 화면에 보이는 이미지 만큼 크롤링이 가능합니다.\n" +
                            "'y'를 입력하면 이미지를 로드합니다.")
            if loading == 'y':
                img_list = browser.find_elements_by_tag_name("img")[1:]
                img_num_searched = len(img_list)
                img_num = min([img_num_searched, img_num_want])
                print("로드된 이미지 개수 : ", img_num_searched)
                print("저장할 이미지 개수 : ", img_num)
                check_img_num = input(
                    f'\n{str(img_num)}개의 이미지를 크롤링하시겠습니까? \n"n" 을 입력하시면 브라우저의 스크롤을 더 조정할 수 있습니다. [y/n] : ')
                if check_img_num == 'n':
                    continue

                browser.implicitly_wait(2)
                for i in range(img_num):
                    if i == 0:
                        print("이미지 저장 중")
                    img = img_list[i]
                    img.screenshot(
                        f"{download_path}/{file_name}{str(i)}.{file_extension}")
                break
            else:
                break
        browser.close()


if __name__ == "__main__":

    img_crawler = google_img_crawler()
    img_crawler.process_step()

    # result_items, var = process_step()
    # if var == quit_msg:
    #     pass
    # search_name, img_num, download_path, file_name, file_extension = [result_items[f"step{n+1}"] for n in range(len(result_items))]
    # scrap_img_google(search_name, img_num, download_path, file_name, file_extension)
