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

    print("Initial links scanned. Following. ")
    # for item in link_list:
    #    print(item, '\n')

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

    openports = []
    ports_file = open("open_ports.txt", "w")

    print("Starting scan on " + targetip)
    print("-" * 60)
    print("Please wait, scanning remote host")
    print("-" * 60)

    try:
        for port in range(1, 1024):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((targetip, port))
            if result == 0:
                print("Port {}:    Open".format(port))
                openports.append(port)
            sock.close()

        for item in openports:
            ports_file.write("Found open ports: \n")
            ports_file.write(str(item))

    except KeyboardInterrupt:
        print("You pressed Ctrl +C")
    except socket.gaierror:
        print("Hostname could not be resolved. Exiting.")
    except socket.error:
        print("Could not connect to server.")

    print("PORT SCAN COMPLETE!")
    print(" Found ", len(openports), "open ports")
    print(openports, '\n')

###############
# SQLi Tester #
###############

def SQLi_Tester():

    read_file = open("crawl_results.txt", "r")
    results_file = open("SQLi_results", "w")
    results_file.write("Pages vulnerable to SQLi:")

    total_links = len(open("crawl_results.txt", "r").readlines())
    counter = 0

    while counter < total_links:
        try:
            for link in read_file:
                print("Testing target ", counter, " out of ", total_links)
                # add the testing code to the end of the link below
                target = urllib.request.urlopen(link)
                result = target.read()
                decoded_result = result.decode('utf-8')
                if "error" and "SQL" in decoded_result:
                    print("The page ", link, " might be vulnerable to SQLi!")
                    results_file.write(link)
                    continue
                counter += 1

        except urllib.error.HTTPError:
            print("Could not test link!")
            counter += 1

#############
# MAIN MENU #
#############
while True:

    print("0. Run it all!")
    print("1. Spider a website")
    print("2. Run a port scan")
    print("3. SQL injection tester")
    selection = input("Please make a selection:")

    if selection == '0':
        url_spider()
        port_scanner()
    elif selection == '1':
        url_spider()
    elif selection == '2':
        port_scanner()
    elif selection == '3':
        SQLi_Tester()