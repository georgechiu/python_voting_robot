#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2019年2月25日

@author: George Chiu
'''


import random
from splinter import Browser
from selenium.common.exceptions import NoAlertPresentException, TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
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
        sleep(random.randint(1, 2))

        self.browser.find_by_xpath("//input[contains(@class, 'fbi_input') and contains(@class, 'cpt_input')]").fill("ABCD")

        sleep(60)
    
    
    def random_mobile_number(self):
        prelist=["130","131","132","133","134","135","136","137","138","139","147","150","151","152","153","155","156","157","158","159","186","187","188"]
        return random.choice(prelist)+"".join(random.choice("0123456789") for i in range(8))
