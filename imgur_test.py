
# coding: utf-8


from selenium import webdriver
from pyvirtualdisplay import Display
import time
from bs4 import BeautifulSoup
import json


def url_to_soup(target_url, scroll_downs, browser, display):
    browser.get(target_url)
    for i in range(scroll_downs):
        print("scrolling down...")
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
    access_time = str(time.time())
    print(browser.title, " accessed at: ", access_time)
    html_source = browser.page_source
    soup = BeautifulSoup(html_source, "html.parser")
    return soup, access_time


def int_clean(number_string):
    if type(number_string) == 'string':
        return int(number_string.replace(",", ""))
    return number_string


def posttype(infostring):
    posttype = infostring.split('·')[0][2:].strip(" ")
    viewstring = infostring.split('·')[1]
    endloc = viewstring.index('views')
    numstring = viewstring[0:endloc].strip(' ')
    if numstring != 'ø':
        numviews = int_clean(numstring)
    else:
        numviews = 0
    return posttype, numviews


def postdata(post, access_time):
    returndict = {}
    returndict['permalink'] = post.attrs['id']
    upv = int_clean(post.find(title = 'like').attrs['data-up'])
    dnv = int_clean(post.find(title = 'dislike').attrs['data-downs'])

    #parse post info
    pi = posttype(post.find(class_='post-info').text)
    returndict['title'] = post.find(class_='hover').p.text
    returndict['type'] = pi[0]
    views = int_clean(pi[1])
    returndict['snapshots'] = [{'time': access_time, 'upv':upv, 'dnv':dnv, 'views':views}]
    return returndict



def process_soup(soup, access_time):
    fpgal = soup.find_all(class_='home-gallery')[0]
    posts = fpgal.find_all(class_= "post")
    processed_posts = []
    for i in posts:
        processed_posts.append(postdata(i, access_time))
    with open('datanew/'+ access_time, 'w') as outfile:
        json.dump(processed_posts, outfile)
    print(len(processed_posts), " posts processed and saved.")
    return



def main(repeats = 1):
    display = Display(visible=0, size=(800, 600))
    display.start()
    browser = webdriver.Firefox()
    target_url = 'http://imgur.com/new/time'
    for i in range(repeats):
        soup, access_time = url_to_soup(target_url, 12, browser, display)
        process_soup(soup, access_time)
        if repeats > 1:
            print("sleeping... ")
            time.sleep(50)
    browser.quit()
    display.stop()




main(100)



