import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get("https://colorscheme.ru/")
matches = {
    1: "protanopia",
    2: "deuteronapia",
    3: "tritanopia"
}


for i in range(1, 4):
    elem = driver.find_element_by_id("csd-menu-vision")
    hover = ActionChains(driver).move_to_element(elem)
    hover.perform()

    elem = driver.find_element_by_class_name("vision-cb" + str(i))
    hover = ActionChains(driver).move_to_element(elem).click()
    hover.perform()

    elem = driver.find_element_by_id("csd-rgb-val")
    hover = ActionChains(driver).move_to_element(elem).click()
    hover.perform()

    d = {
        "r": [],
        "g": [],
        "b": [],
        "r_new": [],
        "g_new": [],
        "b_new": []
    }

    for r in range(0, 256, 16):
        for g in range(0, 256, 16):
            for b in range(0, 256, 16):
                elem = driver.find_element_by_xpath("//div[@class='colpick_rgb_r colpick_field']/input")
                elem.clear()
                elem.send_keys(str(r))

                elem = driver.find_element_by_xpath("//div[@class='colpick_rgb_g colpick_field']/input")
                elem.clear()
                elem.send_keys(str(g))

                elem = driver.find_element_by_xpath("//div[@class='colpick_rgb_b colpick_field']/input")
                elem.clear()
                elem.send_keys(str(b))
                elem.send_keys(Keys.ENTER)

                time.sleep(0.1)

                elem = driver.find_element_by_class_name("bg-pri-0")
                s = elem.get_attribute("style")
                s = s[22:]
                s = s[:-2]
                tmp = list(map(int, s.split(", ")))
                d["r"].append(r)
                d["g"].append(g)
                d["b"].append(b)
                d["r_new"].append(tmp[0])
                d["g_new"].append(tmp[1])
                d["b_new"].append(tmp[2])

    DATA = pd.DataFrame(d)
    DATA.to_csv("D:/Users/Загрузки/" + matches[i] + ".csv", index=False)
