from flows.validators import *

if __name__ == "__main__":
    class DocTest:
        def __init__(self, text):
            self.text = text

    try:
        PhoneValidator().validate(DocTest(""))
    except:
        print("yes 1")
    else:
        print("no 1")

    try:
        PhoneValidator().validate(DocTest("4124124"))
    except:
        print("yes 2")
    else:
        print("no 2")

    try:
        PhoneValidator().validate(DocTest("1234567890a"))
    except:
        print("yes 3")
    else:
        print("no 3")

    try:
        PhoneValidator().validate(DocTest("12A4567890"))
    except:
        print("yes 4")

    else:
        print("no 4")

    try:
        PhoneValidator().validate(DocTest("12345678901"))
    except:
        print("yes 5")
    else:
        print("no 5")

    PhoneValidator().validate(DocTest("1234567890"))

    try:
        DateValidator().validate(DocTest(""))
    except:
        print("yes 10")
    else:
        print("no 10")

    try:
        DateValidator().validate(DocTest("XX.YY.DDDD"))
    except:
        print("yes 11")
    else:
        print("no 11")

    try:
        DateValidator().validate(DocTest("33.11.2023"))
    except:
        print("yes 12")
    else:
        print("no 12")

    try:
        DateValidator().validate(DocTest("25.13.2023"))
    except:
        print("yes 22")
    else:
        print("no 22")

    DateValidator().validate(DocTest("1.1.2023"))

    try:
        EmailValidator().validate(DocTest("25.13.2023"))
    except:
        print("yes 31")
    else:
        print("no 31")

    EmailValidator().validate(DocTest("svayt2@gmail.com"))

    SimpleListValidator(["1", "2", "3", "4"], False).validate(DocTest("2"))
    print("yes 40")

    # import pdb
    # pdb.set_trace()
    try:
        SimpleListValidator(["1", "2", "3", "4"], False).validate(DocTest("5"))
    except:
        print("yes 41")
    else:
        print("no 42")

    SimpleListValidator([], True).validate(DocTest(""))
    print("yes 43")

    print("end")
