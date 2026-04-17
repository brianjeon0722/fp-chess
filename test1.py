import re

a = 'Sicilian: Prins (Moscow), 5...Nc6'

b = re.search(r"[1234567890]", a)

if b == False:
    print('false')

if b == True:
    print('true')
