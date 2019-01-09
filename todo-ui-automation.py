#!/usr/bin/env python
# encoding: utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
import time
import datetime
import unittest
import re
import sys, getopt
import random
import os
import ftplib
import platform
#pyvirtualdisplay needed for Linux
if (platform.system() == "Linux"):
	from pyvirtualdisplay import Display
#found to be helpful in Windows environment
if (platform.system() == "Windows"):
	import win32gui


##############################################################################################
#
# Python script that uses Selenium web driver to run test
# based on previous work example. This code is untested though.
#########################################################################################################


#Global constants - TO DO: change to command line parameters later
if (platform.system() == "Windows"):
	CHROMEDRIVERLOCATION="C:\chromedriver.exe"

#initialize some needed variables
failedList=[]
passedList=[]
skippedList=[]

def getDateStamp():
	"""Creates a unique timestamp used for naming conventions to make template creation and use easier
	Args:
	Returns:
		date (str): the unique timestamp
	"""
	date=datetime.datetime.now()
	return date.strftime('%m-%d-%Y-%H:%M:%S')


		
def getFirefoxWebDriver():
	"""Creates an instance of the supplied webdriver from Selenium that works with Firefox version 46
	Returns:
		webdriver (webdriver): instance of Firefox webdriver
	"""
	firefox_profile = webdriver.FirefoxProfile()
	firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
	return webdriver.Firefox(firefox_profile=firefox_profile)	
	
def getChromeWebDriver():
	"""Creates the webdriver for Chrome
	Returns:
		webdriver (webdriver): Chrome webdriver
	"""
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--incognito")
	chrome_options.add_argument('--ignore-certificate-errors')
	chrome_options.add_argument("--start-maximized");
	return webdriver.Chrome(CHROMEDRIVERLOCATION, chrome_options=chrome_options)

def openLoginPage(driver, ott, user, httpType):
	"""Opens the vDMC OTT Login page
	Args:
		driver (webdriver): webdriver being used for the tests
		ott (str): DNS entry for the vDCM OTT to be tested
		user (str): user to log in as
		httpType (str): http or https
	"""
	#suffix=".cisco.com"
	if ((httpType <> "http") and (httpType <> "https")):
		print (httpType + " not supported. Exiting script.")
		driver.close()
		driver.quit()
		sys.exit()
	else:
		print ("Opening login page for " +user)
		try:
			#p = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
			#if ((p.match(ott)) or (ott.find(suffix))):
			#	driver.get(httpType+"://"+ott+"/admin")
			#else:	
			#	driver.get(httpType+"://"+ott+".cisco.com/admin")
			driver.get("https://vuejs.org/v2/examples/todomvc.html")
		except Exception as e:
			handleException(driver, e, "Open Login Page for " +user)
		
def checkPage(driver, text, testName):
	"""Checks the webpage for specified text and updates the globabl pass/fail numbers
	Args:
		driver (webdriver): webdriver being used for the testName
		text (str): the text to check for on the webpage
		testName (str): the name of the test that is being checked for pass/faill criteria
	"""
	time.sleep(5)
	global failedList
	global passedList
	time.sleep(2)
	#print "Looking for: "+text+" in "+textName
	if ("delete" in testName.lower()):
		if(str(text) not in driver.page_source):
			passedList.append(testName)
		else:
			failedList.append(testName)
	else:
		if (str(text) in driver.page_source):
			passedList.append(testName)
		else:
			failedList.append(testName)
		
	if ((testName.lower() == "user login") and (len(failedList) > 0)):
		print ("Login failed.")
		
def getTestResults(browser):
	"""Print the test results 
	Args:
		buildNumber (str): string containing build number of OTT being tested
		browser (str): Name of browser being tested
		ott (str): string containing name or ip address of OTT under test
	"""
	
	results = "\n\n****************************************************"
	results += ("\n*")
	results += ("\n*    	  TEST RESULTS")
	results += ("\n*")
	results += ("\n* Browser: "+browser+" v"+browserVersion)
	results += ("\n*")
	results += ("\n* PASS: " + str(len(passedList)))
	results += ("\n* FAIL: " + str(len(failedList)))
	results += ("\n* SKIPPED: " + str(len(skippedList)))
	results += ("\n*")
	if (len(failedList) > 0 ):
		results += ("\n* FAILED tests: \n*	" + '\n*	'.join(failedList))
		results += ("\n*\n*\n*")
	if (len(skippedList) > 0):
		results += ("\n* SKIPPED tests: \n*	" + '\n*	'.join(skippedList))
		results += ("\n*\n*\n*")
	if (len(passedList) > 0):	
		results += ("\n* PASSED tests: \n*	" + '\n*	'.join(passedList))
		results += ("\n*")
	results += ("\n****************************************************")
	results += ("\n\n\n\n\n")
	return results		


def main(argv):
	"""Run all the tests. Tests are grouped accordingly. Order of execution is important as templates must be created prior to creating a service flow.
	Args:
		argv (list): list of strings for command line parameters
	"""
	global httptype
	global test
	global currentDate
	global browserVersion
	#global ftpLocation
	#need default FTP path to be a raw string
	#ftpLocation = r"\\abr-reg-udp-1.cisco.com\FTPContent\nickturn\standAloneTest"
	httptype = "https"
	browser = "Firefox"
	listItem1 = "laundry"
	
	try:
		opts, args = getopt.getopt(argv,"h",)
	except getopt.GetoptError:
		print '\n\n\nERROR!'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print ("WORK IN PROGRESS")
			
	if ("Linux" in platform.system()):
		display = Display(visible=0, size=(1280, 720))
		display.start()
			
	currentDate=getDateStamp()
	driver = getWebDriver(browser)	
	browserVersion = driver.capabilities['version']
	driver.driver.find_element_by_class("new-todo").click()
	driver.find_element_by_class("new-todo").clear()

	driver.find_element_by_class("new-todo").send_keys(listItem1`)
	checkPage(driver, listItem1, "Add new item")
	
	   
	
	driver.close()
	driver.quit()
	
	
	results = getTestResults(browser)
	print (results)
	
	#For running in automation stdout will be piped to a file anyways. No need to create another file.
	#writeResultsToFile(buildNumber, results)
	
	#Linux virtual display needs to be stopped at end of test
	if ("Linux" in platform.system()):
		display.stop()
	
	#For curiosity, uncomment below line to see how long the script took to execute
	#print (str(getDateStamp()))
	
if __name__ == "__main__":
	main(sys.argv[1:])		
