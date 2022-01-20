import requests
from bs4 import BeautifulSoup
from requests.sessions import dispatch_hook

def get_distance(a,b):
    # URL 
    url = f"https://www.google.com/search?&q=distace+between+{a}+bus+stop+and+{b}+bus+stop+bengaluru" 
    url = url.replace(" ", "+")
    #print(url)
    #Sending HTTP request
    req = requests.get(url)
    
    # Pulling HTTP data from internet
    sor = BeautifulSoup(req.text, "html.parser") 
    
    # Finding temperature in Celsius
    temp = sor.find("div", class_='BNeawe').text
    temp = temp.replace(")", "")  
    temp = temp.replace("(", "")  
    temp = temp.split()

    # print(temp)
    lol = temp.index("km")
    y = lol-1
    distance = temp[y]
    return distance


