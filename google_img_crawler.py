from selenium import webdriver
from bs4 import BeautifulSoup as bs

def scrap_img_google(search_name, img_num_want = None, download_path = None,
                    file_name = "", file_extension = "png"):
    search_name = "biting nails"
    url = "https://www.google.com/search?q=" + search_name + "&hl=ko&tbm=isch"
    browser = webdriver.Chrome('C:/Users/SEOHYEONPARK/chromedriver.exe')
    browser.get(url)
    
    while True:
        loading = input("\n브라우저의 스크롤을 내려서 이미지를 로드하세요. 화면에 보이는 이미지 만큼 크롤링이 가능합니다.\n" +
                        "'y'를 입력하면 크롤링을 진행합니다.")
        if loading == 'y':
            img_list = browser.find_elements_by_tag_name("img")
            img_num_searched = len(img_list)
            img_num = min([img_num_searched, img_num_want])
            print("로드된 이미지 개수 : ", img_num_searched)
            print("저장할 이미지 개수 : ", img_num)
            browser.implicitly_wait(2)
            for i in range(img_num):
                if i == 0:
                    print("이미지 저장 중")
                img = img_list[i]
                img.screenshot(f"{download_path}{file_name}{str(i)}.{file_extension}")
    browser.close()

if __name__ == "__main__":
    def check_list():
        search_name, img_num, download_path, file_name, file_extension = [None, None, None, None, "png"]

        step_dict = {"step1" : ["search_name", f'search_name = input("{(step1_msg := "검색하고 싶은 키워드")} : ")'],
                "step2" : ["img_num", f'img_num = (input("{(step2_msg := "다운로드 할 이미지 개수")} : "))'],
                "step3" : ["download_path", f'download_path = input("{(step3_msg := "다운로드 받을 디렉토리")} : ")'],
                "step4" : ["file_name", f'file_name = input("{(step4_msg := "저장할 이미지 파일 이름(공백 가능)")} : ")'],
                "step5" : ["file_extension", f'file_extension = input("{(step5_msg := "저장할 이미지 파일 확장자명")} : ")']}
        n = 1
        while True:
            #nth step
            sequence = f"step{n}"
            process = step_dict.get(sequence, "Error")[1]
            exec(process)

            var = eval(step_dict.get(sequence, "Error")[0])

            if n == 1:
                print(f"url : https://www.google.com/search?q={search_name}&hl=ko&tbm=isch")

            if var == "qt":
                break
            elif var == "rt":
                n -= 1
            elif n == len(step_dict):
                print("\n"+step1_msg+"\n"+step2_msg+"\n"+step3_msg+"\n"+step4_msg+"\n"+step5_msg)
                check_items = input("위의 정보가 맞습니까?[y/n]")
                if check_items == 'y':
                    break
                else:
                    n = 1
            else:
                n += 1

        if var == "qt":
            pass
        
        return search_name, img_num, download_path, file_name, file_extension
    search_name, img_num, download_path, file_name, file_extension = check_list()
    scrap_img_google(search_name, img_num, download_path, file_name, file_extension)
