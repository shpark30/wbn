from bs4 import BeautifulSoup as bs
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
import time


class google_img_crawler:

    quit_msg = "qt"
    backward_msg = "bw"

    def __init__(self):
        self.result_dict = {}
        self.ctl_cmd = None

    def __call__(self):
        var = self.process_step()
        if var == quit_msg:
            print("크롤링을 종료합니다")
            return None
        search_name, img_num, download_path, file_name, file_extension = [
            self.result_dict[f"step{str(n+1)}"] for n in range(len(self.result_dict))]
        self.scrap_by_selenium(search_name, img_num,
                               download_path, file_name, file_extension)
        return None

    def _control_flow(input):
        ctl_cmd = {quit_msg: "break", backward_msg: ""}.get(input, None)
        return ctl_cmd

    def process_step(self):
        step_dict = {"step1": [(step1_msg := '검색하고 싶은 키워드'), f"input('{step1_msg} : ')"],
                     "step2": [(step2_msg := '다운로드 할 이미지 개수'), f"input('{step2_msg} : ')"],
                     "step3": [(step3_msg := '다운로드 받을 디렉토리'), f"input('{step3_msg} : ')"],
                     "step4": [(step4_msg := '저장할 이미지 파일 이름(공백 가능)'), f"input('{step4_msg} : ')"],
                     "step5": [(step5_msg := '저장할 이미지 파일 확장자명'), f"input('{step5_msg} : ')"]}

        def _single_step(step_num):
            print("\n" + (sequence := f"step{step_num}"))
            process = step_dict.get(sequence)[1]
            var = eval(process)
            self.result_dict[sequence] = var
            if n == 1:
                print(
                    f"url : https://www.google.com/search?q={var}&hl=ko&tbm=isch")
            self.ctl_cmd = _control_flow(var)
            return var

        step_num = 1
        t_step_cnt = len(step_dict)
        while True:
            if step_num < t_step_cnt + 1:
                _single_step(step_num)

            elif step_num == t_step_cnt + 1:
                # print("\n", *[eval(f"step{str(i+1)}_msg") + " : " + self.result_dict[f"step{str(i+1)}"] for i in range(len(step_dict))], sep = "\n")
                print("\n", *[step_dict[f"step{str(i+1)}"][0] + " : " +
                              self.result_dict[f"step{str(i+1)}"] for i in range(len(step_dict))], sep="\n")
                check_items = input(
                    "위의 정보가 맞습니까? 'n'을 입력하면 처음부터 다시 시작합니다\n[y/n]")
                if check_items == 'y':
                    break
                else:
                    step_num = 1
            else:
                print("step_num가 step_dict의 범위를 벗어났습니다. 디버깅해주세요.")
                var = quit_msg

            if var == quit_msg:
                break
            elif var == backward_msg:
                n -= 1
            else:
                n += 1

        return var

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

    def scrap_by_selenium(self, search_name, img_num_want, download_path=None, file_name="", file_extension="png"):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {
                                        "download.default_directory": repr(download_path)})
        driver = webdriver.Chrome(
            'C:/Users/seohy/chromedriver.exe', chrome_options=options)
        driver.get("https://www.google.co.kr/imghp?hl=ko&tab=ri&authuser=0&ogbl")
        elem = driver.find_element_by_name("q")
        elem.clear()
        elem.send_keys(search_name)
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source

        self._doScrollDown(driver, int(img_num_want))
        img_list = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
        for i, img in enumerate(img_list):

            img.click()
            target = driver.find_element_by_css_selector(".n3VNCb")
            target_src = target.get_attribute("src")
            urllib.request.urlretrieve(
                src, file_name + str(i) + "." + file_extension)

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
    img_crawler()

    # result_items, var = process_step()
    # if var == quit_msg:
    #     pass
    # search_name, img_num, download_path, file_name, file_extension = [result_items[f"step{n+1}"] for n in range(len(result_items))]
    # scrap_img_google(search_name, img_num, download_path, file_name, file_extension)
