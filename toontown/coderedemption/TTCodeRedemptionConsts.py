# 2013.08.22 22:17:31 Pacific Daylight Time
# Embedded file name: toontown.coderedemption.TTCodeRedemptionConsts
DefaultDbName = 'tt_code_redemption'
RedeemErrors = Enum('Success, CodeDoesntExist, CodeIsInactive, CodeAlreadyRedeemed, AwardCouldntBeGiven, TooManyAttempts, SystemUnavailable, ')
RedeemErrorStrings = {RedeemErrors.Success: 'Success',
 RedeemErrors.CodeDoesntExist: 'Invalid code',
 RedeemErrors.CodeIsInactive: 'Code is inactive',
 RedeemErrors.CodeAlreadyRedeemed: 'Code has already been redeemed',
 RedeemErrors.AwardCouldntBeGiven: 'Award could not be given',
 RedeemErrors.TooManyAttempts: 'Too many attempts, code ignored',
 RedeemErrors.SystemUnavailable: 'Code redemption is currently unavailable'}
MaxCustomCodeLen = config.GetInt('tt-max-custom-code-len', 16)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\coderedemption\TTCodeRedemptionConsts.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:17:31 Pacific Daylight Time
