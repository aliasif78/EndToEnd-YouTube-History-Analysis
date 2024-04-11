import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta


def scrapeWatchHistory():
    # Import HTML Content
    with open('C:/Users/92334/Desktop/Takeout/YouTube/history/watch-history.html', 'r', encoding='utf-8') as file:
        htmlContent = file.read()

    # Create Soup object
    soup = BeautifulSoup(htmlContent, 'html.parser')


    # Define DataFrame Columns
    columns = {'Channel Name' : [], 'Video Title' : [], 'Date & Time' : []}


    # Get Channel Names
    tempList = soup.select('div.content-cell a[href^="https://www.youtube.com/channel/"]')

    # Extract text content from each element and store in tempList
    channels = [i.text for i in tempList]

    for i in channels:
        columns['Channel Name'].append(i)


    # Find all div elements with more than one <a> element
    filtered_divs = [div for div in soup.select('div.content-cell') if len(div.select('a')) != 1]

    # Get Video Titles from remaining divs
    tempList = [a.text for div in filtered_divs for a in div.select('a[href^="https://www.youtube.com/watch?"]')]
    
    # Extract text content from each element and store in tempList
    videos = [i for i in tempList]

    for i in videos:
    
        if (i.startswith('https://')):
            continue
    
        if (i.startswith('New Age General Ad | ')):
            continue

        columns['Video Title'].append(i)


    # Get Dates & Times
    tempList = soup.select('div.content-cell')

    for count, i in enumerate(tempList, start=1):

        if (count % 3 != 1):
            continue
       
        if (i.text.strip().split('<br>')[-1].startswith('Answered survey question')):
            print('survey')
            continue
        
        if (i.text.strip().split('<br>')[-1].startswith('Watched a video that has been removed')):
            print('removed')
            continue
        
        if (('https' or 'New Age') in i.text.strip().split('<br>')[-1]):
            #print(i.text.strip().split('<br>')[-1])
            continue
        
        if (i.text.strip().split('<br>')[-1] == ' '):
            print('PKT')
            continue

        columns['Date & Time'].append(i.text.strip().split('<br>')[-1])


    # Filling in missing values
    for i in range(11):
        columns['Channel Name'].append('-1')
    
    for i in range(11):
        columns['Video Title'].append('-1')


    # Creating and Returning a DataFrame
    return columns


def getDatesAndTimes(entry):

    # Get rightmost 29 characters
    myString = entry[-29:]

    # Remove unwanted characters from the beginning
    while True:
        if not (myString.startswith('Jan') or myString.startswith('Aug') or myString.startswith('Sep') or myString.startswith('Oct') or myString.startswith('Nov') or myString.startswith('Dec')):
            myString = myString[1:]
        else:
            break

    # Convert to DataType : Date & Time
    # Jan 22, 2024, 1:10:34 PM PKT
    tempList = myString.split(' ')
    result = ''

    # Year
    result += (tempList[2].rstrip(','))
    result += ('-')

    # Month
    if (tempList[0] == 'Jan'):
        month = '01'
        
    if (tempList[0] == 'Aug'):
        month = '08'
        
    if (tempList[0] == 'Sep'):
        month = '09'
        
    if (tempList[0] == 'Oct'):
        month = '10'
        
    if (tempList[0] == 'Nov'):
        month = '11'
        
    if (tempList[0] == 'Dec'):
        month = '12'

    result += (month)
    result += ('-')

    # Day
    tempList[1] = tempList[1].rstrip(',')

    if (len(tempList[1]) == 1):
        tempList[1] = '0' + tempList[1]

    result += (tempList[1])
    result += (' ')

    # Time
    if (len(tempList[3]) == 7):
        tempList[3] = '0' + tempList[3]

    result += (tempList[3])
    
    return result