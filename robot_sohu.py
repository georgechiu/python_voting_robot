#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2018年12月27日

@author: George Chiu
'''


import random
from splinter import Browser
from selenium.common.exceptions import NoAlertPresentException, TimeoutException, UnexpectedAlertPresentException
from time import sleep


class Voting_Robot_Sohu(object):

    def __init__(self, url=None):
        if url:
            self.url = url
        else:
            self.url = "http://m.sohu.com/activity/vote/mp-prod/?id=274587223_32&from=timeline"
        
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
        for i in range(1, 21):
            finished = False
            while not finished:
                try:
                    while self.browser.is_element_not_present_by_text("投我一票"):
                        sleep(1)
                    finished = True
                except UnexpectedAlertPresentException as e:
                    print(u"出错了：%s" % (e))
                    sleep(random.randint(10, 30))
            
            self.browser.click_link_by_text(u"投我一票")
            print(u"第" + str(i) + u"次投票")
            sleep(random.randint(1, 5))

            alert_present = False
            while not alert_present:
                try:
                    alert = self.browser.get_alert()
                    alert.accept()
                    alert_present = True
                except NoAlertPresentException as e:
                    print(u"没有弹出确认框：%s" % (e))
                    sleep(1)