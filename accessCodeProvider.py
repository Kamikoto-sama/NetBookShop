import random

class AccessCodeProvider:
    accessCode = None

    @staticmethod
    def generateCode():
        length = random.randint(5, 10)
        alpha = list("0123456789QWERTYUIOPASDFGHJKLZXCVBNMqwertyuioasdfghjklzxcvbnm")
        random.shuffle(alpha)
        codeNumbers = [random.choice(alpha) for _ in range(length)]
        AccessCodeProvider.accessCode = "".join(codeNumbers)

if AccessCodeProvider.accessCode is None:
    AccessCodeProvider.generateCode()
