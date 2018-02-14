####################################
# PYDER WEB APP SCANNING UTILITY   #
#                                  #
# Author: z3r0id                   #
####################################

# Pyder attemps to simplify the first step in web app pentesting by:
#    - collecting valuable info
#    - scanning for basic vulnerabilities (SQLi, XSS, bad security settings, etc...)
#    - use collected information to present possible CVEs
#    - present an exportable report on findings

# Nothing in this scan should be trusted 100% and all uncovered vulnerabilities should be verified before finalizing.

###############
# DISCLAIMER: #
###############
# I am not responsible for any damage done with this program, nor am I responsible for any misuse. This utility is for
# ETHICAL hacking and educational purposes only and should not be used on any system without permission.

###############
# WARNING     #
###############
# This is also my first attempt at creating my own spider/scanning utility. Flaws will be present. I am open to critique
# and would welcome any suggestions.
# email me at: z3r0id@daniel-bryan.com

###############
# CONCEPTUAL  #
#   FLOW      #
###############

# take input and options
# start slow port scan
# start spidering
# collect links and follow
# iterate through links and check for SQLi
# check for xss
# check for bruteforcing options
# perform bruteforce if applicable
# scrape vulnerable data (or while spidering)
# generate possible CVEs
# Export all data to document
import socket

from bs4 import BeautifulSoup
import urllib.request
import requests

#############
# SPIDERING #
#############


def url_spider():
    inputurl = input("Enter the target URL:")
    startingurl = urllib.request.urlopen(inputurl)

    link_list = [inputurl]
    links_file = open('links.txt', 'w')

    soup = BeautifulSoup(startingurl, "html5lib")
    soup.prettify()
    init_links = [links.get('href') for links in soup.find_all('a', href=True)]
    for link in init_links:
        if link not in link_list:
            link_list.append(link)

    print("Initial links found: ")
    for item in link_list:
        print(item, '\n')

    counter = 0
    while counter < len(init_links):
        try:
            for child in init_links:
                print("Following item ", counter, "out of ", len(init_links))
                counter += 1
                if child.startswith('http'):
                    child_open = urllib.request.urlopen(child)
                    childsoup = BeautifulSoup(child_open, "html5lib")
                    soup.prettify()
                    child_links = [links.get('href') for links in childsoup.find_all('a', href=True)]
                    for found_child in child_links:
                        if child_links not in link_list:
                            link_list.append(found_child)

        except urllib.error.HTTPError:
            print("ERROR WHILE FOLLOWING CHILD LINK")
        except KeyboardInterrupt:
            counter == len(init_links)
            print("You've stopped scanning!")

    for final_result in link_list:
        links_file.write(final_result)

################
# PORT SCANNER #
################


def port_scanner():
    target = input("Please type target URL or IP:")
    targetip = socket.gethostbyname(target)

    print("Starting scan on " + targetip)
    print("-" * 60)
    print("Please wait, scanning remote host")
    print("-" * 60)


#############
# MAIN MENU #
#############
while True:

    print("1. Spider a website")
    print("2. Run a port scan")
    selection = input("Please make a selection:")

    if selection == str('1'):
        url_spider()
    elif selection == str('2'):
        port_scanner()
