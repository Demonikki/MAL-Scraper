import io
import re
import requests
from bs4 import BeautifulSoup

#Constants
baseurl = "https://myanimelist.net/fansub-groups.php"
lang_en = "Primary Language"

#Group class
class Group:
    def __init__(self, name, url, up, down, shows):
        self.groupname=name
        self.groupurl=url
        self.groupup=up
        self.groupdown=down
        self.groupshows=shows
    def __repr__(self):
        return "Group: "+self.groupname+"\nRating: "+(str)(self.groupup)+"/"+(str)(self.groupdown)+"\nShows:"+(str)(self.groupshows)

class Show:
    def __init__(self, name, up, down):
        self.showname=name
        self.showup=up
        self.showdown=down
    def __repr__(self):
        return ""+self.showname


def getGroups(letter):
    print("Getting Group Names and URLs for group '"+letter+"'")
    fname = 'groupsdata.txt'
    url = baseurl+"?letter="+letter
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    data = soup.find_all("td", class_="borderClass", width="300")
    links = []
    groups = []
    for td in data:
        groupname = td.text
        child=td.findChildren("a")
        groupurl = (str)(child[0])
        groupurl = groupurl[groupurl.find("?") : groupurl.find(">")-1]
        #links.append((groupname, groupurl))
        
        #Get the data of the group as a string
        group = getGroupData(groupname, groupurl)
        #Build data structure
        if(not group == "NotEnglish"):
            #print(group)
            groups.append(group)

    # print(groups)
    # with io.open(fname, "w", encoding="utf-8") as f:
    #     f.write((str)(groups))
    # f.close()

    return groups


'''
Details: (Primary Language: English)
Group Name, List of Shows, Rating per show
'''
def getGroupData(groupname, groupurl):
    page = requests.get(baseurl+groupurl)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    text = soup.get_text()

    #Check that subs are in English
    if not lang_check(text):    
        return "NotEnglish"

    (up,down,total) = getTotalRatings(text)
    shows = getShows(soup)

    #Create the group object using this data
    group = Group(groupname, groupurl, up, down, shows)
    #print (group)

    return group


'''Helper to check sub language'''
def lang_check(text):
    langpos = text.find(lang_en)+len(lang_en)
    lang = text[langpos:langpos+10]
    if("English" in lang):
        return True
    else:
        return False

'''Helper to get total rating count'''
def getTotalRatings(text):
    up_pos = text.find("approve")
    up_str = text[up_pos-10:up_pos]
    up = (int)(re.findall(r'\d+', up_str)[0])
    down_pos = text.find("disapprove")
    down_str = text[down_pos-10:down_pos]
    down = (int)(re.findall(r'\d+', down_str)[0])
    tr=up+down
    return (up,down,tr)

'''Helper to get Shows and Rating data'''
def getShows(soup):
    shows=[]
    shownames = getShowNames(soup)
    # (up,down) = getShowRatings(soup.get_text())
    for i in range(0, len(shownames)):
        shows.append(Show(shownames[i], 2, 3))
    return shows



'''Helper to get show ratings'''
def getShowRatings(text):
    vote_pos = text.find("approve")
    vote_str = text[vote_pos-20:vote_pos]
    votes = (re.findall(r'\d+', vote_str))
    up = (int)(votes[0])
    down = (int)(votes[1])-up
    return (up,down)

'''Getting show names'''
def getShowNames(soup):
    names = []
    nametags = soup.find_all('strong')
    #Hardcoded - remove first 2 names as those are ratings
    for name in nametags[2:]:
        name = (str)(name)
        name = name.replace("<strong>","")
        name = name.replace("</strong>","")
        names.append(name)
    return names


def main():
    print ("Starting..")
    
    groups = getGroups(".")
    #groupsoup = getGroupData("8thSin Fansubs","https://myanimelist.net/fansub-groups.php?id=3375")  #English 1
    #groupsoup = getGroupData("English2", "https://myanimelist.net/fansub-groups.php?id=3607") # English 2
    #groupdata = getGroupData("https://myanimelist.net/fansub-groups.php?id=5870") #German
    #https://myanimelist.net/fansub-groups.php?id=514 # Spanish


    
    # with io.open("groupdata.txt", "w", encoding="utf-8") as f:
    #     f.write(groupsoup.get_text())
    # f.close()

    # print(getShowNames(groupsoup))


#Run main
main()
