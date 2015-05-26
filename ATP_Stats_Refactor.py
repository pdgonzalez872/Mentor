import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import config_ATP
from datetime import date, timedelta


class FetchDataATP:
    """
    This class fetches data from the ATP, creates a csv with relevant info,
    analyses the relevant info with R, plots
    """

    def __init__(self, date_ranking):
        """
        Loads variables
        """
        self.date = date_ranking
        self.rankings_url = ('http://www.atpworldtour.com/Rankings/Singles.aspx?d=' +
                             date_ranking + '&r=0&c=#')

        #  Creates list that will be populated with relevant data
        self.relevant_data = []

        self.field_names = ['Ranking',
                            'First_Name',
                            'Last_Name',
                            'Country',
                            'Career_Prize_Money']

    def email_if_issues(self, message):
        # define some variables
        me = config_ATP.paulo_email
        you = config_ATP.paulo_email

    # Create message container - the correct MIME type is multipart/alternative
        msg = MIMEMultipart('alternative')
        fmt = datetime.datetime.now().strftime("%B/%d/%Y - %H:%M")
        msg['Subject'] = "Error with ATP fetching in {} - {}".format(message,
                                                                     fmt)
        msg['From'] = me
        msg['To'] = you
        msg['Cc'] = me

    # Record the MIME types of both parts - text/plain and text/html.
        text = 'Error - {} - while fetching data on {}'.format(message, fmt)
        part1 = MIMEText(text, 'plain')
        msg.attach(part1)
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login(config_ATP.paulo_login, config_ATP.paulo_pass)
        mail.sendmail(me, you, msg.as_string())
        mail.quit()


    def prev_weekday(self, adate):
        """
        http://stackoverflow.com/questions/12053633/previous-weekday-in-python
        """
        adate -= timedelta(days=2)
        return adate

    def fetch_data_website(self):
        """
        Fetches data from the url. It's not pretty and should be refactored,
        but gives me the data I need, without errors.
        """
        page = urlopen(self.rankings_url)
        ATP_soup = BeautifulSoup(page) #initiates bs4
        table = ATP_soup.find('table') #finds the table in the page


        """
        variable to check length of rows - not sure why this is necessary,
        but doesn't work well without it.
        """
        x = (len(table.findAll('tr')) - 1)

        try:

            # Starts loop to fetch the Rankings data table
            for row in table.findAll('tr')[1:x]:

                """
                These are the data points I parse from the data. I use slices
                from the input, that was somehow originated from a tuple
                that I split
                """

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

                #this creates the player's webpage
                player_webpage = 'http://www.atpworldtour.com/' + \
                           str(arg[arg.find('=')+2:arg.find('">')])

                #adds items to list
                Player_Data = []
                Player_Data.append(Ranking)
                Player_Data.append(First_Name)
                Player_Data.append(Last_Name)
                Player_Data.append(Country)
                Player_Data.append(player_webpage)

                #This gets data in the player's personal page, for each of the players
                url = (player_webpage)
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

                ## Diagnostic print
                print(Player_Data[0], Player_Data[1], Player_Data[2], Player_Data[3], Player_Data[-1])

                # adds to list
                single_data = (Player_Data[0],  # ranking
                               Player_Data[1],  # first_name
                               Player_Data[2],  # last_name
                               Player_Data[3],  # country
                               Player_Data[-1])  #prize_money

                self.relevant_data.append(single_data)

                ## break to test only one row
                # break

        except:  # huge exception, but, at least something.
            FetchDataATP.email_if_issues(self, 'Fetching Data')

        return self.relevant_data

    def create_csv(self):
        """
        Creates csv from object
        """

        try:
            fmt_csv = datetime.datetime.now().strftime("%m%d%Y")
            self.fn = fmt_csv + "_Rankings_ATP.csv"

            # Starts the csv process
            with open(self.fn, 'wt') as output_csv:

                # Configure writer to write standard csv file
                writer = csv.writer(output_csv, delimiter='\t',
                                    quotechar='|',
                                    quoting=csv.QUOTE_MINIMAL,
                                    lineterminator='\n')

                writer.writerow(self.field_names)  # Headers

                testing_list = [('1', 'Novak', 'Djokovic', 'SRB', '76122498'),
                                ('2', 'paulo', 'gonzalez', 'USA', '1000000000')]

                # Write to csv
                # for item in testing_list:  # to test with testing_list
                for item in self.relevant_data:
                    writer.writerow(item)
        except:  # huge exception, but, at least something.
            FetchDataATP.email_if_issues(self, 'Creating CSV file')

        return self.fn

    def replace_rubin_weird_name(self):
        """
        Takes care of Jose Rubin Statham from NZL... nickname (Rubin) messes
        my data fetching up...
        """

        try:
            # reads in csv
            with open(self.fn, 'r') as input_file:

                reader = csv.reader(input_file, delimiter="\t")
                list_data = [lines for lines in reader]

                final_list = list(list_data)

                for i in final_list:
                    if i[3] == "Rubin":
                        i[3] = "NZL"
                    else:
                        pass

            # writes csv
            with open(self.fn, 'wt') as output_csv:

                writer = csv.writer(output_csv, delimiter='\t',
                                    quotechar='|',
                                    quoting=csv.QUOTE_MINIMAL,
                                    lineterminator='\n')

                ## No need to write headers, since it is already on the list
                # writer.writerow(self.field_names)  # Headers

                for item in final_list:
                    writer.writerow(item)

        except:  # huge exception, but, at least something.
            FetchDataATP.email_if_issues(self, 'Error replacing Rubin')


if __name__ == "__main__":
    e = FetchDataATP('25.05.2015')
    e.fetch_data_website()
    e.create_csv()
    e.replace_rubin_weird_name()

