# 2013.08.22 22:17:21 Pacific Daylight Time
# Embedded file name: toontown.chat.ToonChatGarbler
import string
import random
from toontown.toonbase import TTLocalizer
from otp.otpbase import OTPLocalizer
from otp.chat import ChatGarbler

class ToonChatGarbler(ChatGarbler.ChatGarbler):
    __module__ = __name__
    animalSounds = {'dog': TTLocalizer.ChatGarblerDog,
     'cat': TTLocalizer.ChatGarblerCat,
     'mouse': TTLocalizer.ChatGarblerMouse,
     'horse': TTLocalizer.ChatGarblerHorse,
     'rabbit': TTLocalizer.ChatGarblerRabbit,
     'duck': TTLocalizer.ChatGarblerDuck,
     'monkey': TTLocalizer.ChatGarblerMonkey,
     'bear': TTLocalizer.ChatGarblerBear,
     'pig': TTLocalizer.ChatGarblerPig,
     'default': OTPLocalizer.ChatGarblerDefault}

    def garble(self, toon, message):
        newMessage = ''
        animalType = toon.getStyle().getType()
        if ToonChatGarbler.animalSounds.has_key(animalType):
            wordlist = ToonChatGarbler.animalSounds[animalType]
        else:
            wordlist = ToonChatGarbler.animalSounds['default']
        numWords = random.randint(1, 7)
        for i in range(1, numWords + 1):
            wordIndex = random.randint(0, len(wordlist) - 1)
            newMessage = newMessage + wordlist[wordIndex]
            if i < numWords:
                newMessage = newMessage + ' '

        return newMessage

    def garbleSingle(self, toon, message):
        newMessage = ''
        animalType = toon.getStyle().getType()
        if ToonChatGarbler.animalSounds.has_key(animalType):
            wordlist = ToonChatGarbler.animalSounds[animalType]
        else:
            wordlist = ToonChatGarbler.animalSounds['default']
        numWords = 1
        for i in range(1, numWords + 1):
            wordIndex = random.randint(0, len(wordlist) - 1)
            newMessage = newMessage + wordlist[wordIndex]
            if i < numWords:
                newMessage = newMessage + ' '

        return newMessage
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\chat\ToonChatGarbler.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:17:21 Pacific Daylight Time
