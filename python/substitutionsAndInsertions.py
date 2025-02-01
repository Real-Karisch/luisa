from PyPDF2 import PdfReader
import re
import json

substitutions = [
    {
        "volume": 7,
        "page": 19,
        "line": 4,
        "newText": "A Magnitude 8.3 Earthquake occurred in SF on 4/17/1906,",
    },
    {
        "volume": 8,
        "page": 7,
        "line": 3,
        "newText": "June 30, 1908 – The true spirit of charity in the rich and in ",
    },
    {
        "volume": 8,
        "page": 44,
        "line": 18,
        "newText": "June 30, 1908 – The true spirit of charity in the rich and in ",
    },
    {
        "volume": 11,
        "page": 4,
        "line": 5,
        "newText": "February 14, 1912 – Jesus looks at everything in the will,",
    },
    {
        "volume": 11,
        "page": 23,
        "line": 4,
        "newText": "February 14, 1912 – Jesus looks at everything in the will,",
    },
    {
        "volume": 15,
        "page": 10,
        "line": 3,
        "newText": "November 28, 1922 – The Divine Will is beginning, means",
    },
    {
        "volume": 15,
        "page": 12,
        "line": 9,
        "newText": "December 1, 1922 – Jesus did and suffered everything in",
    },
    {
        "volume": 15,
        "page": 14,
        "line": 1,
        "newText": "December 2, 1922 – Jesus places three pillars in the soul",
    },
    {
        "volume": 15,
        "page": 20,
        "line": 24,
        "newText": "December 16, 1922 – On the Conception of the Eternal",
    },
    {
        "volume": 15,
        "page": 24,
        "line": 9,
        "newText": "January 2, 1923 – Prodigies of the Divine Fiat in the void",
    },
    {
        "volume": 15,
        "page": 26,
        "line": 23,
        "newText": "January 5, 1923 – Jesus prays that His Will be one with",
    },
    
    {
        "volume": 17,
        "page": 8,
        "line": 14,
        "newText": "May 17, 1925 – (Continuation of the previous",
    },
    
    {
        "volume": 17,
        "page": 117,
        "line": 12,
        "newText": "May 17, 1925 – (Continuation of the previous",
    },
    {
        "volume": 20,
        "page": 11,
        "line": 15,
        "newText": "January 30, 1927 – Why Jesus did not write.  How",
    },
    {
        "volume": 26,
        "page": 7,
        "line": 15,
        "newText": "August 25, 1929 – How Jesus created the seed of the Divine",
    },
    
]

with open('C:/Users/jackk/Projects/luisa/data/footnotes.txt', 'r') as file:
    footnotes = json.loads(file.read())
    
substitutions.extend(footnotes)

insertions = [
    {
        'volume': 4,
        'page': 15,
        'lineToInsertAfter': 28,
        'newText': 'November 30, 1902 – Fear that her state might be a work of the devil. Jesus teaches her how to recognize when it is He, and when the devil. ...150'
    },
    {
        'volume': 4,
        'page': 18,
        'lineToInsertAfter': 4,
        'newText': 'March 12, 1903 – The sacrifice of Jesus continues in His Eucharist Life in which He exercises continuous pressure on the Father for the sake of mankind. A soul who is victim with Him must also put this continuous pressure on Him. ....180'
    },
    {
        "volume": 11,
        "page": 20,
        "lineToInsertAfter": 0,
        "newText": "J.M.J",
    },
    {
        "volume": 15,
        "page": 10,
        "lineToInsertAfter": 0,
        "newText": "J.M.J",
    },
    {
        "volume": 16,
        "page": 14,
        "lineToInsertAfter": 0,
        "newText": "J.M.J",
    },
    {
        "volume": 17,
        "page": 12,
        "lineToInsertAfter": 0,
        "newText": "J.M.J",
    },
    {
        'volume': 18,
        'page': 6,
        'lineToInsertAfter': 3,
        'newText': 'December 25, 1925 – The dispositions are needed in order to possess the gift of the Divine Will.  Similes of It. The living in Supreme Volition is the greatest thing, it is to live Divine Life, and the soul operates in the unity of the Eternal Light. ....56'
    },
    {
        'volume': 20,
        'page': 7,
        'lineToInsertAfter': 21,
        'newText': 'November 21, 1926 – Tenderness of Jesus at the moment of death. How one who lives in the Divine Will has primacy over everything. ....95'
    },
    {
        'volume': 20,
        'page': 7,
        'lineToInsertAfter': 21,
        'newText': 'November 21, 1926 – Tenderness of Jesus at the moment of death. How one who lives in the Divine Will has primacy over everything. ....95'
    },
    {
        'volume': 29,
        'page': 8,
        'lineToInsertAfter': 13,
        'newText': 'September 12, 1931 – True love forms the stake on which to consume oneself in order to make Him whom one loves live again. The day of Jesus in the Eucharist. ....114'
    },
    {
        "volume": 31,
        "page": 10,
        "lineToInsertAfter": 0,
        "newText": "J.M.J",
    },
    {
        'volume': 35,
        'page': 12,
        'lineToInsertAfter': 0,
        'newText': 'J.M.J'
    },
    {
        'volume': 36,
        'page': 14,
        'lineToInsertAfter': 0,
        'newText': 'J.M.J'
    },
]

def displaySubstitutionAndInsertionPages(pdfFolder='C:/Users/jackk/Projects/luisa/pdfs/'):
    print('SUBSTITUTIONS')
    doneVolumePages = []
    for substitution in [substitutions[-1]]:
        if {'volume': substitution['volume'], 'page': substitution['page']} not in doneVolumePages:
            reader = PdfReader(f"{pdfFolder}/bookOfHeavenVolume{substitution['volume']}.pdf")

            allPages = [page.extract_text().split('\n') for page in reader.pages]

            print(f"Volume {substitution['volume']}, page {substitution['page']}")
            lineNum = 0
            for line in allPages[substitution['page']-1]:
                print(f"{lineNum}: {line}")
                lineNum += 1
            print()
            doneVolumePages.append(
                {
                    'volume': substitution['volume'],
                    'page': substitution['page']
                }
            )
    print()
    print('INSERTIONS')
    doneVolumePages = []
    for insertion in [insertions[-1]]:
        if {'volume': substitution['volume'], 'page': substitution['page']} not in doneVolumePages:
            reader = PdfReader(f"{pdfFolder}/bookOfHeavenVolume{insertion['volume']}.pdf")

            allPages = [page.extract_text().split('\n') for page in reader.pages]

            print(f"Volume {insertion['volume']}, page {insertion['page']}")
            lineNum = 0
            for line in allPages[insertion['page']-1]:
                print(f"{lineNum}: {line}")
                lineNum += 1
            print()
            doneVolumePages.append(
                {
                    'volume': substitution['volume'],
                    'page': substitution['page']
                }
            )

def footnoteFinderAndDeleter(pdfFolder='C:/Users/jackk/Projects/luisa/pdfs/'):
    deletions = []
    for i in range(33, 37):
        print(f"Volume {i}")
        reader = PdfReader(f"{pdfFolder}/bookOfHeavenVolume{i}.pdf")
        allPages = [page.extract_text().split('\n') for page in reader.pages]

        pageNum = 1
        for page in allPages:
            linesStartingWithNumber = [x[0] for x in zip(range(1, len(page)), page[1:]) if re.search('^ *\d', x[1])]
            if linesStartingWithNumber != []:
                print(f"Volume {i}, page {pageNum}")
                lineNum = 0
                for line in page:
                    print(f"{lineNum}: {line}")
                    lineNum += 1

                linesToRemove = input(f"\nNumber detected in lines: {','.join([str(x) for x in linesStartingWithNumber])}\n\nWhich line would you like to remove? Press enter to continue without removing any.")
                if linesToRemove == '':
                    print()
                    continue
                else:
                    for lineToRemove in [int(x) for x in linesToRemove.split(',')]:
                        deletions.append(
                            {
                                'volume': i,
                                'page': pageNum,
                                'line': lineToRemove,
                                'newText': ''
                            }
                        )
                    deletionsJson = json.dumps(deletions)
                    with open('footnotes.txt', 'w') as file:
                        file.write(deletionsJson)
            pageNum += 1
            
def showPage(volumeNum, pageNum, pdfFolder='C:/Users/jackk/Projects/luisa/pdfs/'):
    reader = PdfReader(f"{pdfFolder}/bookOfHeavenVolume{volumeNum}.pdf")
    allPages = [page.extract_text().split('\n') for page in reader.pages]
    
    page = allPages[pageNum - 1]
 
    print(f"Volume {volumeNum}, page {pageNum}")
    lineNum = 0
    for line in page:
        print(f"{lineNum}: {line}")
        lineNum += 1
        
    print()

if __name__ == '__main__':
    #displaySubstitutionAndInsertionPages()
    #footnoteFinderAndDeleter()
    showPage(29, 80)