import discum
import json
import asyncio
#import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import threading
import multiprocessing
from bs4 import BeautifulSoup
import time
#open settings.json and load it into settings
# define a driver

def returnsetting(setting):
    with open("settings.json", "r") as f:
        settings = json.load(f)
    return settings[setting]
# driver path is returnsetting("seleniumpath")
def get_xpath(element):
    """
    Returns the XPath of a given element as a string
    """
    xpath_components = []
    node = element
    while node:
        xpath_components.append(node.name)
        siblings = node.find_previous_siblings(node.name)
        if siblings:
            pos = len(siblings) + 1
            xpath_components[-1] += f"[{pos}]"
        node = node.parent
    xpath_components.reverse()
    return '/' + '/'.join(xpath_components)
class replikadriver():
    def start(self):
        global checkresponder
        checkresponder = False
        self.status = False
        options = webdriver.ChromeOptions()
        # add path to chrome drive
        s = Service(returnsetting("seleniumpath"))
        #make headless
        if returnsetting("headless") == True:
            options.add_argument("--headless")

        self.driver = webdriver.Chrome(service=s, options=options)
        self.driver.get("https://my.replika.com/login")
        wait = webdriver.support.ui.WebDriverWait(self.driver, 5)
        #/html/body/div/div/div[1]/main/form/div[1]/input
        try:
            
            emailelement = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/main/form/div[1]/input")))
        except:
            emailelement = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/form/div/div[1]/input")))
            #enter email
            #fill in returnsetting("replikaemail")
            emailelement.send_keys(returnsetting("replikaemail"))

            #locate and waitfor /html/body/div/div/div[2]/form/div/div[2]/div/input
            password = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/form/div/div[2]/div/input")))
            #fill in returnsetting("replikapassword")
            password.send_keys(returnsetting("replikapassword"))
            #waitfor and click /html/body/div/div/div[2]/form/div/button[2]
            wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/form/div/button[2]"))).click()
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "GdprNotification__LinkButton-sc-nj3w6j-2"))).click()
            time.sleep(10)
            
            self.status = True
            return
        #fill in returnsetting("replikaemail")
        emailelement.send_keys(returnsetting("replikaemail"))
        #find and click /html/body/div/div/div[1]/main/form/button
        wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/main/form/button"))).click()
        #find element /html/body/div/div/div[1]/main/div/h2 and get content
        #not clickable
        try:
            check = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[1]/main/div/h2")))
        except:
            raise("Something is wrong with the email or and replika ")
        check = check.text
        if not check == returnsetting("replikaemail"):
            raise("Something is wrong with the email")
        # fill in returnsetting("replikapassword") to /html/body/div/div/div[1]/main/form/div[1]/div/input
        wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/main/form/div[1]/div/input"))).send_keys(returnsetting("replikapassword"))
        # click /html/body/div/div/div[1]/main/form/button
        wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/main/form/button"))).click()
        # wait until GdprNotification__LinkButton-sc-nj3w6j-2 fmFKYG
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "GdprNotification__LinkButton-sc-nj3w6j-2"))).click()
        wait = webdriver.support.ui.WebDriverWait(self.driver, 10)

        # find //*[@data-testid='daily-reward-dialog']
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@data-testid='daily-reward-dialog']")))
            print("Claim daily rewards")
        except:
            print("Found no daily rewards")
            pass
        
    

        
        #click the element
       
        time.sleep(5)
        
        self.status = True
    def getstatus(self):
        if self.status == True:
            return True
        else:
            return False
    def sendtoreplika(self, message):
        #check if there is a element with class TextArea-sc-10kop8p-0 WidgetLayout__WidgetTextArea-sc-s1msl5-4 ChatTitledTextFieldWidget__StyledTextArea-sc-1vx115z-0 gmPCa-D eiEbsT ikzwMG
        
        wait = webdriver.support.ui.WebDriverWait(self.driver, 10)
        #wait until a textarea is clickable
        #by tag name
        wait.until(EC.element_to_be_clickable((By.TAG_NAME, "textarea"))).send_keys(message)
        #try to find a div with a class name that starts with string "WidgetLayout__SubmitContainer"
        try:
            #class name starts with WidgetLayout__SubmitContainer but also may have other text after it
            element = self.driver.find_element(By.XPATH, "//*[starts-with(@class, 'WidgetLayout__SubmitContainer')]")
            #find element that has data-testid ="titled-text-field-widget-send-button"
            element = self.driver.find_element(By.XPATH, "//*[starts-with(@data-testid, 'titled-text-field-widget-send-button')]")
            self.driver.execute_script("arguments[0].click();", element)

            
            
            
            return
        except:
            print("no submit container found")
        
                
        
        self.driver.find_element(By.TAG_NAME, "textarea").send_keys(Keys.ENTER)
        
def fetchmessages():
    message = ""
    oldid = ""
    # get newest div with attribute data-author = "replika"
    #with bs4
    try:
        innerhtml = replika.driver.execute_script("return document.body.innerHTML")
    except:
        
        return
    soup = BeautifulSoup(innerhtml, "html.parser")
    #message = soup.find("div", {"data-author": "replika"})
    #similar like above but with :last-of-type
    # find all div tags
    divs = soup.find_all("div")
    # loop through the divs in reverse order
    for div in divs:
        # check if this div has a data-author attribute equal to "replika"
        if div.get("data-author") == "replika":
            # return this div element
            message = div

    
    #soup the message
    message = BeautifulSoup(str(message), "html.parser")
    # in the div get the span with id that starts with "message-<anything>"
    #with bs4
    #message = message.find("span", {"id": lambda L: L and L.startswith('message-')})
    #like above but search for the last one
    try:
        message = message.find_all("span", {"id": lambda L: L and L.startswith('message-')})[-1]
    except:
        return
    messageid = message["id"]
    soup = BeautifulSoup(str(message), "html.parser")
    span = soup.find('span')
    message = span.text
    
    #now get the message id from the span id
    
        
        

    return message
def messagechecker():
    global client
    
    oldmessage = ""
    message = ""
    
    while True:
        try:
            newhtml = replika.driver.execute_script("return document.body.innerHTML")
        except:

            time.sleep(1)

        
        message = fetchmessages()

        if message != oldmessage:
            sendmsg(message)
        else:
            time.sleep(1)
        oldmessage = message
        


client = discum.Client(token=returnsetting("discordtoken"), log=False)
@client.gateway.command
def intitial(resp):
    if resp.event.ready_supplemental:
        user = client.gateway.session.user
        print("Logged in as {}#{}".format(user['username'], user['discriminator']))
    if resp.event.message:

        #check if the message is a dm
        m= resp.parsed.auto()
        channelid = m['channel_id']
        author = m['author']
        tosend = m['content']
        tosend = "*message from {}#{}*: {}".format(author['username'], author['discriminator'], tosend)
        if returnsetting("dmchannel") == channelid and author['id'] != client.gateway.session.user['id']:
            replika.sendtoreplika(tosend)
def sendmsg(msg):
    client.sendMessage(returnsetting("dmchannel"), msg)



        


replika = replikadriver()
# start the replika driver in a thread  
#run threadsafe


t2 = threading.Thread(target=replika.start)
t4 = threading.Thread(target=messagechecker)
t3 = threading.Thread(target=client.gateway.run, kwargs={'auto_reconnect': True})
t4.start()
t2.start()
t3.start()
#start the discord client with args auto_reconnect=True
t3.join()
t4.join()
t2.join()


