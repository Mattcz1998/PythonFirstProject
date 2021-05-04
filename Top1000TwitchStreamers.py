import csv
import collections
import math

userSearchedTeam = input("Enter the channel name of your Twitch streamer: ")

# Function that puts number prefix
def numberPrefix(number):
    '''
    Convert an integer into its ordinal representation::
        make_ordinal(0)   => '0th'
        make_ordinal(3)   => '3rd'
        make_ordinal(122) => '122nd'
        make_ordinal(213) => '213th'
    '''
    n = int(number) # parse int
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix

# Function that ranks streamers total viewers by percentile
def getPercentile(Iviews):
  with open("twitchdata-update.csv") as data:
    r = csv.DictReader(data)
    viewsGained = []
    percentile_ranks = {}
    for item in r:
        viewsGained.append(item["Views gained"])
    frequencies = collections.Counter(viewsGained)
    frequencies = sorted(frequencies.items())
    count = len(viewsGained)
    cumulative_percentage = 0
    for i in frequencies:
      views = int(i[0])
      frequency = int(i[1])
      percentage = frequency / count
      percentile_rank = cumulative_percentage
      cumulative_percentage += percentage
      percentile_ranks[str(views)] = {"views": views,
                                 "frequency": frequency,
                                 "percentage": percentage,
                                 "cumulative_percentage": cumulative_percentage,
                                 "percentile_rank": percentile_rank}
  return numberPrefix(percentile_ranks[str(Iviews)]["percentile_rank"] * 100)

with open("twitchdata-update.csv") as data:
  readCSV = csv.reader(data, delimiter = ',')
  rankingCounter = -1   # this starts at one because of the channel header
  foundStreamer = False   # used for IF statement when channel name NOT in list
  for row in readCSV:
    rankingCounter = rankingCounter + 1
    # If channel name is in list
    if row[0].lower() == userSearchedTeam.lower():
      foundStreamer = True
      print("%s is in %s place in the Top 1000 Twitch streamers!" % (row[0], numberPrefix(rankingCounter)))
      guessedEstimatedRevenue = input("How much ad revenue do you think " + row[0] + " made in 2020? \n")
      if not guessedEstimatedRevenue.isdigit():
        print("Enter a valid number.")
        break
      # Calculate ad revenue range
      estimatedRevenueFromStreamer = int(row[7]) / 1000
      range1 = estimatedRevenueFromStreamer * 2
      range2 = estimatedRevenueFromStreamer * 10
      # If guess is in range
      if range1 <= int(guessedEstimatedRevenue) <= range2:
        print("Your guess of $" + guessedEstimatedRevenue + " DOES FALL in " + row[0] + "'s range! \n")
        print(row[0] + " made an estimated ad revenue between $" + '{0:.2f}'.format(range1) + " - $" + '{0:.2f}'.format(range2) + " in 2020")
        print(row[0] + " falls in the " + getPercentile(row[7]) + " percentile of ad revenue earned in the Top 1000 Twitch streamers list.") 
      # If guess is NOT in range
      else:
        print("Your guess of " + guessedEstimatedRevenue + " DOES NOT FALL in " + row[0] + "'s range. \n")
        print(row[0] + " made an estimated ad revenue between $" + '{0:.2f}'.format(range1) + " - $" + '{0:.2f}'.format(range2) + " in 2020") 
        print(row[0] + " falls in the " + getPercentile(row[7]) + " percentile of ad revenue earned in the Top 1000 Twitch streamers list.") 
  # If channel name NOT in list 
  if not foundStreamer:
    print(userSearchedTeam + " is not in the Top 1000 Twitch Streamer list.")