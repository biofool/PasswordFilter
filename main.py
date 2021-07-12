    # Passwords from
# https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt

# def passworddecensy(password):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {password}')  # Press ⌘F8 to toggle the breakpoint.
from progress.bar import Bar
# import time


def test():
    cnt = 1

    with Bar('Validation (each update is 1K passwords)', max=len(compromised) / 1000) as bar:
        for badword in compromised:
            if badword not in compromised:
                print("Validation error {} not detected in {}", badword, badwordfile)
            else:
                cnt += 1
                if cnt % 1000:
                    pass
                else:
                    bar.next()


def init(custombadwordfile):
    global badwordfile, compromised
    if custombadwordfile:
        badwordfile = custombadwordfile
    else:
        badwordfile = '10-million-password-list-top-1000000.txt'
    with open(badwordfile) as compromised10K:
        compromised = set(map(str.rstrip, compromised10K))
    # Validate

init('10-million-password-list-top-1000000.txt')
test()
