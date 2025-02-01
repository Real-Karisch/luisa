import re
from datetime import datetime
from PyPDF2 import PdfReader
from copy import deepcopy
import json

from substitutionsAndInsertions import substitutions, insertions

patterns = {
    'date': r'([A-Z][a-z]+ \d+, \d\d\d\d)',
    'tableOfContentsEntryEnd': r'[.�… ]+(\d+)$',
    #'tableOfContentsEntryEnd': r'([.�… ]|\x08)+(\d+)$',
    'spaceDashSpace': r' *[–—] *', #need to catch * for the earthquake entry
    'footer': r'by the Little Daughter of the Divine Will Luisa',
    'prayerPageTitles': r'(Prayer of Consecration to the Holy Divine Will|Prayer For the Glorification)',
    'diaryFirstPage': r'(J\.M\.J|I\.M\.I)',
}

def flatten(listOfLists):
    return [x for l in listOfLists for x in l]

def findOverlappingIndex(shortStr, longStr):
    longStrIndex = 0
    for shortStrIndex in range(len(shortStr)):
        if longStr[longStrIndex] == '\n':
            longStrIndex += 1
        if shortStr[shortStrIndex] != longStr[longStrIndex]:
            return longStrIndex
        longStrIndex += 1
    return longStrIndex

def stashVolumesJson(volumesDict, location='C:/Users/jackk/Projects/luisa/data/allVolumes.json'):
    volumesStrDates = deepcopy(volumesDict)

    for volume in volumesStrDates:
        for entry in volume:
            entry['date'] = entry['date'].strftime('%m/%d/%Y')

    with open(location, 'w') as file:
        file.write(json.dumps(volumesStrDates))

def loadVolumesJson(location='C:/Users/jackk/Projects/luisa/data/allVolumes.json'):
    with open(location, 'r') as file:
        volumes = json.loads(file.read())
    
    for volume in volumes:
        for entry in volume:
            entry['date'] = datetime.strptime(entry['date'], '%m/%d/%Y').date()

    return volumes

def prepareVolumeLines(volume, reader, tableOfContentsStartPageNum=4):
    substitutionsInVolume = [x for x in substitutions if x['volume'] == volume] != []
    insertionsInVolume = [x for x in insertions if x['volume'] == volume] != []

    allPages = [page.extract_text().split('\n') for page in reader.pages]

    if substitutionsInVolume:
        pageNum = 1
        for page in allPages:
            for substitution in substitutions:
                if substitution['volume'] == volume and substitution['page'] == pageNum:
                    page[substitution['line']] = substitution['newText']
            pageNum += 1
    if insertionsInVolume:
        pageNum = 1
        for page in allPages:
            for insertion in insertions:
                if insertion['volume'] == volume and insertion['page'] == pageNum:
                    page.insert(insertion['lineToInsertAfter']+1, insertion['newText'])
            pageNum += 1
            
    diaryFirstPageNum = findDiaryFirstPageNum(allPages)

    tableOfContentsLines = flatten([x for x in allPages[tableOfContentsStartPageNum-1:diaryFirstPageNum-2] if x != ''])
    firstTableOfContentsEntryLineNum = [x[0] for x in zip(range(len(tableOfContentsLines)), tableOfContentsLines) if re.search(patterns['date'], x[1])][0]
    tableOfContentsLines = tableOfContentsLines[firstTableOfContentsEntryLineNum:]

    lastDiaryPage = [x[0] for x in list(zip(range(len(allPages)), allPages))[-7:] if re.search(patterns['prayerPageTitles'], ''.join(x[1]))][0]

    diaryPages = [x for x in allPages[diaryFirstPageNum-1:lastDiaryPage] if x != '']
    
    diaryLines = [x for x in flatten(diaryPages) if re.search(patterns['footer'], x) is None]

    return {
        'tableOfContents': tableOfContentsLines,
        'diary': diaryLines
    }

def findDiaryFirstPageNum(allPages):
    pageNum = 1
    for page in allPages:
        if re.search(patterns['diaryFirstPage'], ''.join(page)):
            return pageNum
        pageNum += 1
    return -1

def parseTableOfContentsLine(line):
    if re.search(patterns['footer'], line) or re.search(patterns['prayerPageTitles'], line) or line == '':
        return {}
    line = re.sub(r'(\x08|�)', '.', line)
    line = re.sub(r'  ', ' ', line)
    dateSearch = re.match(patterns['date'], line)
    endLineSearch = re.search(patterns['tableOfContentsEntryEnd'], line)
    tableOfContentsLineItems = {
        'dateText': '',
        'date': datetime(year=1000, month=1, day=1).date(),
        'titlePortion': '',
        'entryPageNum': -1
    }
    titlePattern = '([\n\S ]+)'
    titleGroup = 1
    if dateSearch:
        tableOfContentsLineItems['dateText'] = dateSearch.group(1)
        try:
            tableOfContentsLineItems['date'] = datetime.strptime(dateSearch.group(1), "%B %d, %Y").date()
        except ValueError:
            print(f"{dateSearch.group(1)} not a real date in table of contents.")
        titlePattern = f"{patterns['date']}{patterns['spaceDashSpace']}([\n\S ]+)"
        titleGroup = 2
    if endLineSearch:
        tableOfContentsLineItems['entryPageNum'] = int(endLineSearch.group(1))
        titlePattern += patterns['tableOfContentsEntryEnd']
    titlePortion = re.search(titlePattern, line).group(titleGroup)
    
    #tableOfContentsLineItems['titlePortion'] = titlePortion.strip('.�… ') if endLineSearch else titlePortion

    tableOfContentsLineItems['titlePortion'] = titlePortion.strip('.�… ')

    return tableOfContentsLineItems

def parseDiaryLine(line):
    if line == '':
        return {}
    dateSearch = re.match(patterns['date'], line)
    diaryLineItems = {
        'dateText': '',
        'date': datetime(year=1000, month=1, day=1).date(),
        'contents': ''
    }
    contentsPattern = '([\n\S ]+)'
    contentsGroup = 1
    if dateSearch:
        diaryLineItems['dateText'] = dateSearch.group(1)
        try:
            diaryLineItems['date'] = datetime.strptime(dateSearch.group(1), "%B %d, %Y").date()
        except ValueError:
            print(f"{dateSearch.group(1)} not a real date in diary.")
        contentsPattern = f"{patterns['date']}{patterns['spaceDashSpace']}([\n\S ]+)"
        contentsGroup = 2
    
    diaryLineItems['contents'] = re.search(contentsPattern, line).group(contentsGroup)

    return diaryLineItems

def initializeEntriesFromTableOfContents(tableOfContentsLines):
    entries = []
    entryNum = 0
    for contentsLine in tableOfContentsLines:
        lineItems = parseTableOfContentsLine(contentsLine)
        if lineItems == {}: #if it's the footer line
            continue
        if lineItems['dateText'] != '': #if this is a line with a date in it
            entries.append(
                {
                    'num': entryNum,
                    'dateText': lineItems['dateText'],
                    'date': lineItems['date'],
                    'title': '',
                    'diaryPageNum': lineItems['entryPageNum'],
                    'contents': ''
                }
            )
            entryNum += 1
        if lineItems['entryPageNum'] != -1: #if this is a line that ends a contents item
            entries[-1]['title'] = entries[-1]['title'] + lineItems['titlePortion'] if entries[-1]['title'] == '' else f"{entries[-1]['title']} {lineItems['titlePortion']}"
            entries[-1]['diaryPageNum'] = lineItems['entryPageNum'] if entries[-1]['diaryPageNum'] == -1 else entries[-1]['diaryPageNum']
        else:
            entries[-1]['title'] = entries[-1]['title'] + lineItems['titlePortion'] if entries[-1]['title'] == '' else f"{entries[-1]['title']} {lineItems['titlePortion']}"

    for entry in entries:
        if re.search('[A-Za-z] *$', entry['title']):
            entry['title'] = entry['title'].strip() + '.'

    return entries

def findDiaryDateIndices(diaryLines):
    diaryDateIndices = []
    currentIndex = 0
    for diaryLine in diaryLines:
        if re.search(patterns['date'], diaryLine):
            diaryDateIndices.append(currentIndex)
        currentIndex += 1
    diaryDateIndices.append(len(diaryLines)+1)
    return diaryDateIndices

def parseDiaryEntryLines(diaryEntryLines):
    lineCnt = 0
    for line in diaryEntryLines:
        diaryEntryLines[lineCnt] = re.sub(r'(\x08|�)', '.', line)
        diaryEntryLines[lineCnt] = re.sub(r'  ', ' ', line)
        if re.search('\. *$', line):
            diaryEntryLines[lineCnt] += '\n'
        lineCnt += 1
    fullStr = ''.join(diaryEntryLines)
    parsePattern = f"{patterns['date']}{patterns['spaceDashSpace']}([\n\S ]+)"
    fullStrSearch = re.search(parsePattern, fullStr)
    diaryEntryItems = {
        'date': datetime.strptime(fullStrSearch.group(1), "%B %d, %Y").date(),
        'contentsIncludingTitle': fullStrSearch.group(2)
    }
    return diaryEntryItems

def addContentsToEntry(entries, diaryEntryItems):
    entriesWithDate = [x['num'] for x in entries if x['date'] == diaryEntryItems['date']]
    if entriesWithDate != []:
        entryNum = entriesWithDate[0]
    else:
        print(f"No entry in the table of contents for {diaryEntryItems['date']}")
        return
    entries[entryNum]['contents'] = diaryEntryItems['contentsIncludingTitle'][
        findOverlappingIndex(
            shortStr=entries[entryNum]['title'],
            longStr=diaryEntryItems['contentsIncludingTitle']
        ):
    ].lstrip('.,?;:- �…\n')
    
def generateSingleVolumeEntriesFromPdf(volumeNum, tableOfContentsStartPageNum=4, pdfFolder='C:/Users/jackk/Projects/luisa/pdfs/'):
    reader = PdfReader(f"{pdfFolder}/bookOfHeavenVolume{volumeNum}.pdf")
    
    preparedVolumeLines = prepareVolumeLines(volume=volumeNum, reader=reader, tableOfContentsStartPageNum=tableOfContentsStartPageNum)
    tableOfContentsLines = preparedVolumeLines['tableOfContents']
    diaryLines = preparedVolumeLines['diary']

    entries = initializeEntriesFromTableOfContents(tableOfContentsLines)
    diaryDateIndices = findDiaryDateIndices(diaryLines)

    for i in range(len(diaryDateIndices)-1):
        diaryEntryLines = diaryLines[diaryDateIndices[i]:diaryDateIndices[i+1]]
        diaryEntryItems = parseDiaryEntryLines(diaryEntryLines)
        addContentsToEntry(entries, diaryEntryItems)

    return entries

def generateAndSaveVolumes():
    volumes = []
    for i in range(2, 37):
        print(f"Volume {i}")
        volumes.append(
            generateSingleVolumeEntriesFromPdf(
                volumeNum=i
            )
        )
    stashVolumesJson(volumes)

if __name__ == '__main__':
    generateAndSaveVolumes()
    #generateSingleVolumeEntriesFromPdf(34)
    