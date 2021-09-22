from bs4 import BeautifulSoup
import requests

def fetch(url):
    # returns soup object of url
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }
    page = requests.get(url, headers=headers).text
    soup = BeautifulSoup(page, "html.parser")
    return soup

def list_td(td):
    # prints the gear a character has equipped
    for item in td:
        title = item.get('title')
        print(title)

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

    print("\nCharacters:")

    # display characters and their gear
    for char in char_table_body[1:]:
        td = char.find_all('td')
        print(f"Lvl: {td[3].text} {td[2].text}, Fame: {td[5].text}, Exp: {td[6].text}, Pl: {td[7].text}")
        items = td[8].find_all("span", class_="item")
        list_td(items)
        print(" ")

def player_graveyard():
    user = input("Enter a user: ")
    site = "https://www.realmeye.com/graveyard-of-player/" + user
    data = fetch(site)

    characters = data.find("table", class_="table table-striped tablesorter")
    try:
        graveyard_table_body = characters.find_all("tr")
    except:
        print(f"No graveyard found for {user}")
        print("If their name is correct they may have chosen to hide their graveyard.")
        return

    print(f"Graveyard of player {user}:\n")
    for tr in graveyard_table_body[1:]:
        td = tr.find_all('td')
        print(f"Lvl: {td[3].text.strip()} {td[8].text.strip()} {td[2].text.strip()} died on {td[0].text.strip().replace('T',' ').replace('Z',' ')}[Base fame: {td[4].text.strip()}] [Total fame: {td[5].text.strip()}] [Exp: {td[6].text.strip()}]")
        print(f"[!] Killed by {td[9].text.strip()}")
        items = td[7].find_all("span", class_="item")
        list_td(items)
        print(" ")
        
def recent_deaths():
    char_classes = {
        "0":"All",
        "1":"Archer",
        "2":"Assassin",
        "3":"Bard",
        "4":"Huntress",
        "5":"Knight",
        "6":"Mystic",
        "7":"Necromancer",
        "8":"Ninja",
        "9":"Paladin",
        "10":"Priest",
        "11":"Rogue",
        "12":"Samurai",
        "13":"Sorcerer",
        "14":"Summoner",
        "15":"Trickster",
        "16":"Warrior",
        "17":"Wizard",
    }
    print("--<>--<>--<>--<>--<>--<>--<>--<>--")
    for key, value in char_classes.items():
        print(key,':',value)
    print("--<>--<>--<>--<>--<>--<>--<>--<>--")

    # user may only select 0 to 17
    class_number = -1
    while not int(class_number) in range (0,18):
        class_number = input("Enter a class using their number (0 - 17): ")
    print(f"You have chosen {char_classes[class_number]}")

    # user may only enter 0 to 8
    maxed_stats = -1
    while not int(maxed_stats) in range (0,9):
        maxed_stats = input("Enter minimum number of maxed stats (0-8): ")

    if char_classes[class_number] == "All":
        # user wants to search all classes
        data = fetch("https://www.realmeye.com/recent-deaths?ms=" + str(maxed_stats))
        table = data.find("table", id="d")
    else:
        # user has searched for specific class
        data = fetch("https://www.realmeye.com/recent-" + char_classes[class_number] + "-deaths?ms=" + str(maxed_stats))
        table = data.find("table", id="d")

    recent_characters = table.find_all('tr')
    
    # finds 10 most recent deaths, private characters are not listed.
    print(" ")
    for index, row in enumerate(recent_characters[1:]):
        td = row.find_all('td')
        if td[1].text != "Private": # do not show private characters
            print(f"{td[1].text}, Base fame: {td[3].text}, {td[6].text} killed by: {td[7].text}")
            items = td[5].find_all("span", class_="item")
            list_td(items)
            print(" ")
        if index == 10:
            break
        
if __name__ == "__main__":
    option = -1
    while option != 0:
        try:
            print("""+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n0 = Quit\n1 = Search for a player\n2 = Check recent character deaths\n3 = Search for a players graveyard\n+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+""")
            option = int(input())
            if option == 0:
                print("Quitting...")
            elif option == 1:
                player_search()
            elif option == 2:
                recent_deaths()
            elif option == 3:
                player_graveyard()
        except:
            print("[!] Enter a number to select an option.")