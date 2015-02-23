#This takes some time to complete but... Works!

from urllib.request import urlopen
from bs4 import BeautifulSoup

#This gets data from the page below: A list of the current players in the ATP
url = ('http://www.atpworldtour.com/Rankings/Singles.aspx?d=23.02.2015&r=0&c=#')
page = urlopen(url)

ATP_soup = BeautifulSoup(page) #initiates bs4
table = ATP_soup.find('table') #finds the table in the page

x = (len(table.findAll('tr')) - 1) # variable to check length of rows - not sure why this is necessary, but doesn't work well without it.

for row in table.findAll('tr')[1:x]: #starts loop to fetch the Rankings data table
#for row in table.findAll('tr')[1:3]: # this is for only 2 players, example. #this is for testing

    #These are the data points I parse from the data. I use slices from the input, that was somehow originated from a tuple that I split
    col = row.findAll('td')
    href = str(row.find('a', href=True))
    name = ' '.join(str(col[0].getText()).split())
    player = (name, href)
    arg = ' '.join(player)
    Ranking = int(arg[:arg.find(' ')].replace(',',''))
    Full_Name = arg[arg.find(' ')+1:arg.find('(')-1]
    First_Name = Full_Name[Full_Name.find(', ')+2:]
    Last_Name = Full_Name[:Full_Name.find(',')]
    Country = arg[arg.find('(')+1:arg.find(')')]
    Web_Page = 'http://www.atpworldtour.com/' + str(arg[arg.find('=')+2:arg.find('">')]) #this creates the player's webpage

    #adds items to list
    Player_Data = []
    Player_Data.append(Ranking)
    Player_Data.append(First_Name)
    Player_Data.append(Last_Name)
    Player_Data.append(Country)
    Player_Data.append(Web_Page)

    #This gets data in the player's personal page, for each of the players
    url = (Web_Page)
    page = urlopen(url)
    Player_soup = BeautifulSoup(page) # initiates bs4

    #There are 2 locations with the data I wanted:
    player_table1 = Player_soup.find('ul', id = 'playerBioInfoList') #finds the data in the page
    player_table2 = Player_soup.find('table', id = 'bioGridSingles') #finds the table in the page

    #Some players have more data than the others and I've found some discrepancies where the data doesn't match
    #Example: Djokovic and Federer: Even though the code is the same, Federer's age is not shown in the data. Same with Nishokori

    for row in player_table1.findAll('li')[1:]: # adds items from location1 to list
        row = str(row).replace('<li><span>','').replace('</span>','').replace('</li>','')
        Player_Data.append(row)

    for row in player_table2.findAll('td')[2:]: # adds items from location2 to list
        Player_Data.append(row.getText())

    #My main goal in this project was to be able to gather how much Prize_Money a player has earned over his career
    #Despite the variable data points for each player, the career money is always the last in the query. Therefore, I used the negative slice [-1]
    #to get the last item in the list and cast it as an integer for later calculations
    Prize_Money = int(str(Player_Data[-1]).replace('Singles & Doubles combined', '').replace('$','').replace(',',''))
    Player_Data.append(Prize_Money) # append this to the list

    print(Player_Data) #This is just to show results -> could save to file, etc.