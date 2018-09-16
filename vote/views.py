from django.shortcuts import render
from django.http import HttpResponse

import getopt
import random
import sys
import time
import json
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from pynamodb.connection import Connection

def updateOrder(request):
     conn = Connection(region='us-east-1')
     table = conn.list_tables()
     personal_data = conn.scan('updateOrder')
     for item in personal_data['Items']:
          print(item['username']['S'])
          comment_numper = 4
          driver = webdriver.Chrome('chromedriver')
          driver.get("https://news.ycombinator.com/news")
          driver.maximize_window()
          time.sleep(1)
          elem = driver.find_element_by_xpath('//a[@href="login?goto=news"]')  # driver.find_element_by_link_text("login")
          ActionChains(driver).move_to_element(elem).click().perform()

          elem = driver.find_element_by_name("acct")
          ActionChains(driver).move_to_element(elem).click().perform()
          ActionChains(driver).send_keys(item['username']['S']).perform()

          elem = driver.find_element_by_name("pw")
          ActionChains(driver).move_to_element(elem).click().perform()
          ActionChains(driver).send_keys(item['password']['S']).perform()

          ActionChains(driver).send_keys(Keys.RETURN).perform()

          driver.get("https://news.ycombinator.com/news")
          time.sleep(1)

          upvote_elems = driver.find_elements_by_class_name("votearrow")
          ActionChains(driver).move_to_element(upvote_elems[random.randint(0, len(upvote_elems) - 1)]).click().perform()

          time.sleep(1)

          comment_elems = driver.find_elements_by_partial_link_text("comment")
          ActionChains(driver).move_to_element(comment_elems[int(comment_numper)]).click().perform()

          write_comment_element = driver.find_element_by_xpath('//textarea[@name="text"]')
          ActionChains(driver).move_to_element(write_comment_element).click().perform()
          ActionChains(driver).send_keys('This is one of the best test comments ever. Its bigly.').perform()

          submit_element = driver.find_element_by_xpath('//input[@type="submit"]')
          ActionChains(driver).move_to_element(submit_element).click().perform()

          time.sleep(1)

          driver.get("https://news.ycombinator.com/news")
          logout_elem = driver.find_element_by_id("logout")
          ActionChains(driver).move_to_element(logout_elem).click().perform()

          driver.close()
     return HttpResponse("Hello, world. Well Done.")
