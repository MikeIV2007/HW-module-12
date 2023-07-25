def format_phone_number(func):
    def inner (phone):
        result = func(phone)
        if len(result) == 12:
            new_phone = '+' + result[:2] + '(' + result[2:5] + ')' + result[5:8] + '-' + result[8:10] + '-' + result[10: 12]
        elif len(result) == 10:
            new_phone = '+38(' + result[:3] + ')' + result[3:6] + '-' + result[6:8] + '-' + result[8:10]
        else:
            return None
        
        return new_phone
    return inner

@format_phone_number
def sanitize_phone_number(phone):
    new_phone = (
        phone.strip()
            .removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
    )
    return new_phone

if __name__ == '__main__':
    phone = "38050-111-22-2"
    #phone = "    +38(050)1233234"
    #phone = "     0503451234"
    #phone = ' 1234567891111234'

    print (sanitize_phone_number(phone))

# "    +38(050)123-32-34"
# "     0503451234"
# #(050)8889900"
# "38050-111-22-22"
# "38050 111 22 11   "

