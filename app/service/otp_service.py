import uuid

def generateOTP():
    uId = uuid.uuid4()
    
    OTP = (uId.int % 9000) + 1000
    return str(OTP)