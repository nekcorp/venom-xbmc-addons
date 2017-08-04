#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker

import xbmcgui

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Estream'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'estream'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self):
        sPattern = "v=([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def __modifyUrl(self, sUrl):
        return sUrl;

    def __getKey(self):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        
        api_call = ''
        #type1
        oParser = cParser()
        sPattern = '<source *src="([^"]+)" *type=\'video/.+?\''
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            api_call = aResult[1][0]
            
        #type2?   
        sPattern =  '<script type=\'text/javascript\'>(.+?)</script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            stri = cPacker().unpack(aResult[1][0])
            sPattern =  'file:"([^"]+)",label:"([0-9]+)"}'
            aResult = oParser.parse(stri, sPattern)
            if (aResult[0] == True):
                url=[]
                qua=[]
                
                for aEntry in aResult[1]:
                    url.append(aEntry[0])
                    qua.append(aEntry[1][:3] + '*' + aEntry[1][3:])
                    
                #Si une seule url
                if len(url) == 1:
                    api_call = url[0]
                #si plus de une
                elif len(url) > 1:
                    #Affichage du tableau
                    dialog2 = xbmcgui.Dialog()
                    ret = dialog2.select('Select Quality', qua)
                    if (ret > -1):
                        api_call = url[ret]

        if (api_call):
            return True,api_call 

        return False, False
