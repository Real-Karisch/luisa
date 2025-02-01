from airium import Airium
from luisaPdfToJson import loadVolumesJson
import re

def generateLuisaIndexHtml(volumesJson):
    luisaIndexHtmlBuilder = Airium()
    with luisaIndexHtmlBuilder.head():
        luisaIndexHtmlBuilder.title(_t=f"Diary of Luisa Piccarreta - Contents")
        luisaIndexHtmlBuilder.link(href="./styles.css", rel="stylesheet")
        luisaIndexHtmlBuilder('<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />')

    with luisaIndexHtmlBuilder.div(id='mainwrap'):
        with luisaIndexHtmlBuilder.div(style="text-align: center"):
            luisaIndexHtmlBuilder.h1(_t=f"Diary of Luisa Piccarreta - Contents")
            luisaIndexHtmlBuilder.br()
            luisaIndexHtmlBuilder.a(href='./../index.html', _t=f"Return to Documents Home Page", style="text-decoration: underline")
            luisaIndexHtmlBuilder.br()
            luisaIndexHtmlBuilder.br()

            volumeNum = 2
            for volumeJson in volumesJson:
                luisaIndexHtmlBuilder.a(_t=f"Volume {volumeNum} - {volumeJson[0]['date'].strftime('%b %Y')} to {volumeJson[-1]['date'].strftime('%b %Y')}", href=f'./luisaVolume{volumeNum}.html', style="text-decoration: underline")
                luisaIndexHtmlBuilder.br()
                volumeNum += 1
            luisaIndexHtmlBuilder.br()
            luisaIndexHtmlBuilder.a(_t=f"Full Index", href=f'./luisaFullIndex.html', style="text-decoration: underline")
    return luisaIndexHtmlBuilder

def generateVolumeHtml(volumeJson, volumeNum):
    volumeHtmlBuilder = Airium()
    with volumeHtmlBuilder.head():
        volumeHtmlBuilder.title(_t=f"Diary of Luisa Piccarreta, Volume {volumeNum}")
        volumeHtmlBuilder.link(href="./styles.css", rel="stylesheet")
        volumeHtmlBuilder('<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />')

    with volumeHtmlBuilder.div(id='mainwrap'):
        with volumeHtmlBuilder.div(style="text-align: center"):
            volumeHtmlBuilder.h1(_t=f"Diary of Luisa Piccarreta, Volume {volumeNum}")
            volumeHtmlBuilder.br()
           
            volumeHtmlBuilder.a(href='./../index.html', _t=f"Return to Documents Home Page", style="text-decoration: underline")
            volumeHtmlBuilder(" | ")
            volumeHtmlBuilder.a(href='./luisa.html', _t=f"Return to Diary of Luisa Piccarreta Contents", style="text-decoration: underline")
            volumeHtmlBuilder.br()

    with volumeHtmlBuilder.div(id='tightwrap'):
        for entry in volumeJson:
            with volumeHtmlBuilder.details():
                volumeHtmlBuilder.summary(_t=f"{entry['date'].strftime('%m/%d/%Y')} - {entry['title']}", style="font-weight:bold")
                with volumeHtmlBuilder.div(id='expansionwrap'):
                    with volumeHtmlBuilder.span():
                        volumeHtmlBuilder(
                            re.sub(r'\n', '<br><br>', entry['contents'])
                            )
                volumeHtmlBuilder.br()
                volumeHtmlBuilder.br()
            volumeHtmlBuilder.hr()

    return volumeHtmlBuilder

def generateKeyHtml(volumesJson):
    keyHtmlBuilder = Airium()
    with keyHtmlBuilder.head():
        keyHtmlBuilder.title(_t=f"Diary of Luisa Piccarreta - Full Index")
        keyHtmlBuilder.link(href="./styles.css", rel="stylesheet")
        keyHtmlBuilder('<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />')

    with keyHtmlBuilder.div(id='mainwrap'):
        with keyHtmlBuilder.div(style="text-align: center"):
            keyHtmlBuilder.h1(_t=f"Diary of Luisa Piccarreta - Full Index")
            keyHtmlBuilder.br()
            keyHtmlBuilder.a(href='./../index.html', _t=f"Return to Documents Home Page", style="text-decoration: underline")
            keyHtmlBuilder(" | ")
            keyHtmlBuilder.a(href='./luisa.html', _t=f"Return to Diary of Luisa Piccarreta Contents", style="text-decoration: underline")
            keyHtmlBuilder.br()
            keyHtmlBuilder.br()

            volumeNum = 2
            for volumeJson in volumesJson:
                keyHtmlBuilder.a(_t=f"Volume {volumeNum} - {volumeJson[0]['date'].strftime('%b %Y')} to {volumeJson[-1]['date'].strftime('%b %Y')}", href=f'./luisaVolume{volumeNum}.html', style="text-decoration: underline")
                keyHtmlBuilder.br()
                for entry in volumeJson:
                    keyHtmlBuilder(entry['title'])
                    keyHtmlBuilder(" • ")
                keyHtmlBuilder.br()
                keyHtmlBuilder.br()
                volumeNum += 1
    
    return keyHtmlBuilder

def saveAllVolumeHtml(volumesJsonAddress='C:/Users/jackk/Projects/luisa/data/allVolumes.json', htmlFolder='C:/Users/jackk/Projects/website/luisa/'):
    volumesJson = loadVolumesJson(volumesJsonAddress)
    
    luisaIndexHtmlBuilder = generateLuisaIndexHtml(volumesJson)
    with open(f"{htmlFolder}/luisa.html", 'wb') as file:
        file.write(bytes(luisaIndexHtmlBuilder))

    keyHtmlBuilder = generateKeyHtml(volumesJson)
    with open(f"{htmlFolder}/luisaFullIndex.html", 'wb') as file:
        file.write(bytes(keyHtmlBuilder))

    volumeNum = 2
    for volumeJson in volumesJson:
        volumeHtmlBuilder = generateVolumeHtml(volumeJson, volumeNum)

        with open(f"{htmlFolder}/luisaVolume{volumeNum}.html", 'wb') as file:
            file.write(bytes(volumeHtmlBuilder))

        volumeNum += 1

if __name__ == '__main__':
    saveAllVolumeHtml()

    
