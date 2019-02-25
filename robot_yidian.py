#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2019年2月25日

@author: George Chiu
'''


from io import BytesIO
import random
from PIL import Image
from pytesseract import image_to_string
from splinter import Browser
from selenium.common.exceptions import NoAlertPresentException, TimeoutException, UnexpectedAlertPresentException
from time import sleep


class Voting_Robot_Yidian(object):

    def __init__(self, url=None):
        if url:
            self.url = url
        else:
            self.url = "http://yidianqinglang.mikecrm.com/FIQEZsT"
        
        self.browser = None
    

    def start(self):
        while True:
            browser = Browser(driver_name="chrome")
            browser.driver.set_page_load_timeout(180)
            self.browser = browser
            self.load_page(self.url)
            self.vote()
            self.browser.quit()


    def load_page(self, url):
        browser = self.browser
        finished, timeout = False, False
        original_url = browser.url
        retry_time = 0

        while not finished:
            try:
                if timeout:
                    timeout = False
                    browser.reload()
                
                if browser.url == original_url:
                    browser.visit(url)
                
                finished = True
            except TimeoutException as e:
                timeout = True
                print(u"超时了：%s" % (e))
                if retry_time > 10:
                    raise Exception(u"超过超时重试次数！")
                else:
                    retry_time = retry_time + 1


    def vote(self):
        self.browser.click_link_by_id("opt202747726")
        self.browser.click_link_by_id("opt202748650")
        self.browser.click_link_by_id("opt202752630")
        self.browser.find_by_xpath("//input[contains(@class, 'fbi_input') and contains(@class, 'aria-content')]").fill(self.random_mobile_number())

        self.browser.click_link_by_id("form_submit")
        while self.browser.is_element_not_present_by_xpath("//img[@class='cpt_img']"):
            sleep(random.randint(1, 2))

        while True:
            text = self.get_captcha()
            if text.isalnum():
                self.browser.find_by_xpath("//input[contains(@class, 'fbi_input') and contains(@class, 'cpt_input')]").fill(text)
                if self.browser.find_by_xpath("//i[contains(@class, 'iconfont') and contains(@class, 'cpt_icon') and contains(@class, 'succeed')]"):
                    break
            self.browser.driver.find_element_by_class_name("cpt_img").click()
            sleep(random.random())
        
        self.browser.find_by_xpath("//a[contains(@class, 'fbc_button') and contains(@class, 'cpt_confirm')]").click()

        sleep(random.randint(1, 5))
    
    
    def random_mobile_number(self):
        prelist=["130","131","132","133","134","135","136","137","138","139","147","150","151","152","153","155","156","157","158","159","186","187","188"]
        return random.choice(prelist)+"".join(random.choice("0123456789") for i in range(8))

    
    def get_captcha(self):
        screenshot = Image.open(BytesIO(self.browser.driver.get_screenshot_as_png()))

        element = self.browser.driver.find_element_by_class_name("cpt_img")
        location = element.location
        size = element.size
        left = location["x"]
        top = location["y"]
        right = left + size["width"]
        bottom = top + size["height"]
        area = (left, top, right, bottom)

        captcha_img = screenshot.crop(area)
        text = image_to_string(captcha_img)

        return text


    def binary_image(self, image, threshold):
        gray_image = image.convert("L")
        table = []

        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
    
        bin_image = gray_image.point(table, "1")
        return bin_image


    def clear_noise(self, image):
        data = image.getdata()
        w, h = image.size
        black_point = 0

        for x in range(1, w - 1):
            for y in range(1, h - 1):
                mid_pixel = data[w * y + x]
                if mid_pixel < 50:
                    top_pixel = data[w * (y - 1) + x]
                    left_pixel = data[w * y + (x - 1)]
                    down_pixel = data[w * (y + 1) + x]
                    right_pixel = data[w * y + (x + 1)]
                
                    if top_pixel < 10:
                        black_point += 1
                    if left_pixel < 10:
                        black_point += 1
                    if down_pixel < 10:
                        black_point += 1
                    if right_pixel < 10:
                        black_point += 1
                    if black_point < 1:
                        image.putpixel((x, y), 255)
                
                    black_point = 0

        for x in range(1, w - 1):
            for y in range(1, h - 1):
                if x < 2 or y < 2:
                    image.putpixel((x - 1, y - 1), 255)
                if x > w - 3 or y > h - 3:
                    image.putpixel((x + 1, y + 1), 255)
