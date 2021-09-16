from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def fetch(url):
    # returns soup object of url
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page,"html.parser")
    return soup

def player_search():
    user = input("Enter a user: ")
    site = "https://www.realmeye.com/player/" + user
    data = fetch(site)

    # find name and summary
    name = data.find("h1")
    summary = data.find("table", {"summary"})

    # info about user characters
    characters = data.find("table", class_="table table-striped tablesorter")
    try: 
        # display user information
        char_table_body = characters.find_all("tr")
        print(f"Player name: {name.text.strip()}")
    except:
        print(f"No characters found for {user}")
        print("If their name is correct they may have chosen to hide their characters.")
        return

    for tr in summary:
        tds = tr.find_all('td')
        print(tds[0].text + ": " + tds[1].text)

    print("\n")
    print("Characters:")

    # display characters and their gear
    for char in char_table_body[1:]:
        td = char.find_all('td')
        print(f"Lvl: {td[3].text} {td[2].text}, Fame: {td[5].text}, Exp: {td[6].text}, Pl: {td[7].text}")
        
        items = td[8].find_all("span", class_="item")
        for item in items:
            title = item.get('title')
            print(title)

        print("\n")

if __name__ == "__main__":
    player_search()