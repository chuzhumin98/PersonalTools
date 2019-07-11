from selenium import webdriver
from time import sleep

import os

from params import driver_path
from params import id
from params import password

'''
代码功能：将北京共青团支部系统中的我的团员详细信息抓取下来，并存到一个Excel之中
'''

def crawlId(driver_path, id, password):
    driver = webdriver.Chrome(driver_path)

    attributes = []
    attributes_finished = False

    data = []

    main_window = driver.current_window_handle

    driver.get('https://www.bjyouth.net') # 获取共青云页面
    sleep(2)
    driver.find_element_by_id('login-username').send_keys(id)
    driver.find_element_by_id('login-password').send_keys(password)

    verifycode = input()

    driver.find_element_by_id('login-verifycode').send_keys(verifycode)
    driver.find_element_by_id('dosign').click()

    sleep(7)

    driver.find_element_by_link_text('我的团员').click()

    sleep(4)

    while True:
        info = driver.find_element_by_id('goods-grid')
        students = info.find_elements_by_tag_name('tr')

        for i in range(1, len(students)):
            student = students[i]
            link = student.find_elements_by_tag_name('td')[1].find_elements_by_tag_name('a')[0]
            print(link.text)
            link.click()

            all_windows = driver.window_handles

            for window in all_windows:
                if window != main_window:
                    driver.switch_to.window(window)
                    table = driver.find_element_by_id('w0')
                    items = table.find_elements_by_tag_name('tr')
                    data_person = []
                    for item in items:
                        contents = item.find_elements_by_tag_name('td')
                        if not attributes_finished:
                            attributes.append(contents[0].text)
                        data_person.append(contents[1].text)
                    data.append(data_person)

            driver.close()
            driver.switch_to.window(main_window)

        nextpages = driver.find_elements_by_class_name('next')

        if len(nextpages) == 0:
            break

        if nextpages[0].tag_name == 'a':
            nextpages[0].click()
            sleep(4)
        else:
            break

    if not os.path.exists('data'):
        os.makedirs('data')

    with open('./data/{}.csv'.format(id), 'w', encoding='gbk') as f:
        f.write(','.join(attributes)+'\n')
        for line in data:
            f.write(','.join(line)+'\n')

if __name__ == '__main__':
    crawlId(driver_path, id, password)
