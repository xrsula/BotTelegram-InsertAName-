import logging
from subprocess import CalledProcessError
import requests
import random
import os
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

PORT = int(os.environ.get('PORT', 5000))
TOKEN = "" ##????

# Enable logging
logging.basicConfig(format = "%(asctime)s - %(name)s - %(levelname)s  - %(message)s", 
                    level = logging.INFO)

logger = logging.getLogger(__name__)

chaoticMood = True

teffe7aPack = {
    "scary jad"             : "CAACAgQAAxkBAAEGq8dji8npHraSlcWGyI8HYO45uarHFwACVg4AAi-xQVNVw2ytAUVEFCsE",
    "yassine masterclass"   : "CAACAgQAAxkBAAEGq8lji8oD6HJFQV9zQXXSJa_slTjXuwACaQ0AAvY7QFObyhQn_yiQISsE", 
    "jad w/ knife"          : "CAACAgQAAxkBAAEGq8tji8oTkU42b-7T-ZGF2Qw2fQh5VAACvQ0AAiIFQVNpBT5dvS2hRSsE", 
    "mamoun"                : "CAACAgQAAxkBAAEGq81ji8ou-1UIYg8kR01x9JefhAABslUAAi0NAAK0VUlTwqD-X9j_maIrBA", 
    "L"                     : "CAACAgQAAxkBAAEGq89ji8o58Xa-BTMVT_wEIW6nUuGCMgACsA0AAkrKQVNfbuoOw8OncCsE", 
    "matthias wyss"         : "CAACAgQAAxkBAAEGq9Fji8pHxoVlf13YTYdevqucJAWz5gACYw0AAlLlQFOJMj8mM_ou-ysE", 
    "scary jad 2"           : "CAACAgQAAxkBAAEGq9Nji8pU_b6o0CKvvo2V_HReR0NOVQACFwwAApqxQVMcYL8vEYh0kCsE", 
    "greenscreen jad"       : "CAACAgQAAxkBAAEGq9Vji8pel4E1DqWR5VRS5XD5u0CPuwACQBAAAtNFSFOstDSZqAm61isE", 
    "pikachu mamoun"        : "CAACAgQAAxkBAAEGq9tji8px3AkDY8rX39EteoOVSf14kQACPQwAAkJgQVOMgGg6P46SfysE", 
    "unlike"                : "CAACAgQAAxkBAAEGq91ji8qLIZYWjSTwmVFKl77iEKPmWgACzA0AAvwAAUBT6qL7ZbjmkAUrBA", 
    "baguette"              : "CAACAgQAAxkBAAEGq99ji8qVsDTvqoUuWyB8YFudMjOwAAMZDAAC4rtJU8ktQZImeNcRKwQ", 
    "dalle"                 : "CAACAgQAAxkBAAEGq9lji8pp02JHGbRciVnQQg8xcOGATgAC9A0AAmvkQVOG-A9OTdcptysE", 
    "urs knife 1"           : "CAACAgQAAxkBAAEGq-Fji8qlFFasUn0qLzmzJKxRZ6QryQACdQ4AAl0RQFM5ayBNlMZnhSsE",
    "urs knife 2"           : "CAACAgQAAxkBAAEGq-Nji8qybAFE6RnYJuEL9Tj41VaduAACrgsAAlE5QVPsZRcr5-GmzSsE",
    "urs knife 3"           : "CAACAgQAAxkBAAEGq-dji8rTp3b1y2Nvcimkpr4DqHxFHQACrQ0AAifAQFP9uZmDXSrObSsE",
    "urs knife 4"           : "CAACAgQAAxkBAAEGq-Vji8rClT1g4CsITDSnyP_i6xIpDwACdw0AAlZoQVPa3t6w_kuH1SsE",
    "urs knife 5"           : "CAACAgQAAxkBAAEGq-lji8rgtczeJb4eboSq99zCTpZCcgACIQ0AAuGUQFNPYoJb2dVADSsE",
    "emergency exit"        : "CAACAgQAAxkBAAEGq-tji8rrqt_y4OG3KbCHTbdMOwLRBwAC6Q0AAjr8QVOBAj8v1tVpiCsE", 
    "agepAuLit"             : "CAACAgQAAxkBAAEGq-1ji8r3W-UDDa-5XspPsjpHZD3VxgACGA8AAihAIFDiSO3j6T5JuCsE", 
    "basé"                  : "CAACAgQAAxkBAAEGq_Jji8sDUguYvgi-lpUewGkeKyFjEQAChA0AAncEUFPS0h_m7nbUnysE",
    "cap"                   : "CAACAgQAAxkBAAEGq_Zji8sO51887Uw-KHmudoz8458kGAACKgwAAtG3SVN0Qv2iJ939hSsE",
    "réel"                  : "CAACAgQAAxkBAAEGq_hji8sZTDf2HPX_cAqZuvOvRsOuUgAC4AwAAoHySVOx8Q51K2QsRysE",
    "crowd"                 : "CAACAgQAAxkBAAEGq_pji8spBGsk4OysbOpcOyvSV3tyyQACfwwAAoClSFNdCigDThtScisE",
    "bagarre"               : "CAACAgQAAxkBAAEGq_xji8tDgHRA2RALK1tZvgAB2iBuLIUAAvkOAAJs2UFTNteSUzyooJ8rBA", 
    "wasted"                : "CAACAgQAAxkBAAEGrAJji8tmNlULam_vDGaz9GzpsO28VgACvQ0AAsEYSVMAAYUFRS6YWiQrBA",
    "à fond"                : "CAACAgQAAxkBAAEGrAABY4vLUgABIWiXnT_7yP_pcC4PY_zzAAL4DgAC4OdQU_0ccNq9jgX0KwQ", 
    "algebre"               : "CAACAgQAAxkBAAEGrARji8t3Ff3xaqx4orIN_P8bxS2y0QAC8QwAAquZSVN9I3O3nPxZOCsE",
    "sunglasses omar"       : "CAACAgQAAxkBAAEGrARji8t3Ff3xaqx4orIN_P8bxS2y0QAC8QwAAquZSVN9I3O3nPxZOCsE",
    "colonel"               : "CAACAgQAAxkBAAEGrAhji8uXgyrXShqwT9zABDPGlq037AACtQsAAqbFUVNVEDfLffQv3isE",
    "dinguerie wesh"        : "CAACAgQAAxkBAAEGrApji8uoDegAAd_nueXS3gJnL88pMpsAArkNAAIyTklTNwXLaNPZdB0rBA",
    "hassen thinking"       : "CAACAgQAAxkBAAEGrAxji8u4LjToA25jvoC-u9z4sycUGQACDwoAArVoSVNCibIFymEVFCsE",
    "sofia imposteur"       : "CAACAgQAAxkBAAEGrA5ji8vHWHiUnWkhDAUYwa0ux2zrIgACCQ0AAv-XSVP4BLATBaDSgysE",
    "imagine"               : "CAACAgQAAxkBAAEGrBBji8vXyAE6yoJAV3CkoAU6FqU3mQAC3Q4AAqscUFPtTOSO6791BCsE",
    "caddie"                : "CAACAgQAAxkBAAEGrBJji8vmG39MjCwcpbNSbDyCaqpklQACyA4AAjNBUFOCK08NznTGtysE",
    "jad filou"             : "CAACAgQAAxkBAAEGrBRji8v8yzp7qIkGv4nhPqj42TLIhgACaA0AAh5fcVM8GPwnmvIcnysE",
    "IC Wars"               : "CAACAgQAAxkBAAEGrBZji8xb-DI4MjiQKYnhIwFVrTLddwACqg8AAs8saFM4O9CITuSxiSsE",
    "yass queen"            : "CAACAgQAAxkBAAEGrBhji8xuNrGY1_3-T1lCkyDV13HDsAACLhAAAv5QaVOn7zzRubnoPCsE",
    "wiwi filou"            : "CAACAgQAAxkBAAEGrBpji8yBbSLVVh13ptefzclLEihf_wAC5xAAAgXjgFMj5eQzTpdBYisE",
    "fax"                   : "CAACAgQAAxkBAAEGrBxji8yYptZKdNAQMy9ogRldpe16uwACuA8AAuCfiFNgrFXK2HJj-SsE",
    "yas strong"            : "CAACAgQAAxkBAAEGrB5ji8yp_VGgQbIlkoR9SdNSQLUlBQACfAsAAsSukVOUL-KAz5cn6isE",
    "aveugle"               : "CAACAgQAAxkBAAEGrCJji80Z-zcQOdw4XTKWAntGOpZ8zAACrA4AApd6qVM7HkoJ1G45ZisE",
    "rien à foutre"         : "CAACAgQAAxkBAAEGrCRji80oa0bNh98HHSN-lVl7F2MHhAACLgwAAkB8sVOf0ZHTW0hYnCsE",
    "kratos messi"          : "CAACAgQAAxkBAAEGrCZji803Wn9VWkOBbVBGgj-c0CiPXwACtQ4AAk9VGVAwKG_C9epUWCsE",
    "sorcellerie"           : "CAACAgQAAxkBAAEGrChji81LnGyfbrZBRe6z_vqtMnVlswACHw0AAgiRIFCUZ2ukf8yNsysE"
}

def start(update, context):
    update.message.reply_text("wesh wesh canne à pêche")

def help(update, context):
    if chaoticMood :
        update.message.reply_text(
            """che7 je vais pas t'aider""")
    else :
        update.message.reply_text(
            """ok fine >:(
                /start : starts me,
                /help : gives you tmi about me
                /cat : sends cute cat pictures :3
                /epfl : creates a poll to see who is where
                ..."""
        )

#def epfl(update, context):
    ##help

def error(update, context):
    logger.info("i hate u you broke me :|, fix it: {context.error}")

def regexFilter(main, *keywords) : 
  filters = Filters.regex(re.compile(main, re.IGNORECASE))
  for k in keywords :
    filters |= Filters.regex(re.compile(k, re.IGNORECASE))
  return filters

def reactSticker(sticker):
  return lambda update, context : update.message.reply_sticker(sticker, quote=False)

def addSticker(reaction, *keywords):
    dp.add_handler(MessageHandler(regexFilter(*keywords), reactSticker(reaction)))

##MAIN##
def main():
    updater = Updater(TOKEN, use_context = True)

    global dp
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    #dp.add_handler(CommandHandler("epfl", epfl))

    addSticker(teffe7aPack["scary jad"]             , "come")
    addSticker(teffe7aPack["yassine masterclasse"]  , "masterclasse", "pres", "vp")
    addSticker(teffe7aPack["jad w/ knife"]          , )
    addSticker(teffe7aPack["mamoun"]                , "desert", "maroc")
    addSticker(teffe7aPack["L"]                     , "L", "cheh", "che7", "F")
    addSticker(teffe7aPack["matthias wyss"]         , "LeBron James")
    addSticker(teffe7aPack["scary jad 2"]           , "no way")
    addSticker(teffe7aPack["greenscreen jad"]       , )
    addSticker(teffe7aPack["pikachu mamoun"]        , )
    addSticker(teffe7aPack["unlike"]                , )
    addSticker(teffe7aPack["baguette"]              , )
    addSticker(teffe7aPack["dalle"]                 , )
    addSticker(teffe7aPack["urs knife 1"]           , )
    addSticker(teffe7aPack["urs knife 2"]           , )
    addSticker(teffe7aPack["urs knife 3"]           , )
    addSticker(teffe7aPack["urs knife 4"]           , )
    addSticker(teffe7aPack["urs knife 5"]           , )
    addSticker(teffe7aPack["emergency exit"]        , )
    addSticker(teffe7aPack["agepAuLit"]             , )
    addSticker(teffe7aPack["basé"]                  , )
    addSticker(teffe7aPack["cap"]                   , )
    addSticker(teffe7aPack["réel"]                  , )
    addSticker(teffe7aPack["crowd"]                 , )
    addSticker(teffe7aPack["bagarre"]               , )
    addSticker(teffe7aPack["wasted"]                , )
    addSticker(teffe7aPack["à fond"]                , )
    addSticker(teffe7aPack["algebre"]               , )
    addSticker(teffe7aPack["sunglasses omar"]       , )
    addSticker(teffe7aPack["colonel"]               , )
    addSticker(teffe7aPack["dinguerie wesh"]        , )
    addSticker(teffe7aPack["hassen thinking"]       , )
    addSticker(teffe7aPack["sofia imposteur"]       , )
    addSticker(teffe7aPack["imagine"]               , )
    addSticker(teffe7aPack["caddie"]                , )
    addSticker(teffe7aPack["jad filou"]             , )
    addSticker(teffe7aPack["IC Wars"]               , )
    addSticker(teffe7aPack["yass queen"]            , )
    addSticker(teffe7aPack["wiwi filou"]            , )
    addSticker(teffe7aPack["fax"]                   , )
    addSticker(teffe7aPack["yas strong"]            , )
    addSticker(teffe7aPack["aveugle"]               , )
    addSticker(teffe7aPack["rien à foutre"]         , )
    addSticker(teffe7aPack["kratos messi"]          , )
    addSticker(teffe7aPack["sorcellerie"]           , )

