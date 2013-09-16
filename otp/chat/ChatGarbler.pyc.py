# 2013.08.22 22:15:11 Pacific Daylight Time
# Embedded file name: otp.chat.ChatGarbler
import string
import random
from otp.otpbase import OTPLocalizer

class ChatGarbler():
    __module__ = __name__

    def garble(self, avatar, message):
        newMessage = ''
        numWords = random.randint(1, 7)
        wordlist = OTPLocalizer.ChatGarblerDefault
        for i in range(1, numWords + 1):
            wordIndex = random.randint(0, len(wordlist) - 1)
            newMessage = newMessage + wordlist[wordIndex]
            if i < numWords:
                newMessage = newMessage + ' '

        return newMessage

    def garbleSingle(self, avatar, message):
        newMessage = ''
        numWords = 1
        wordlist = OTPLocalizer.ChatGarblerDefault
        for i in range(1, numWords + 1):
            wordIndex = random.randint(0, len(wordlist) - 1)
            newMessage = newMessage + wordlist[wordIndex]
            if i < numWords:
                newMessage = newMessage + ' '

        return newMessage
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\chat\ChatGarbler.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:11 Pacific Daylight Time
