encrypted = 'NBY KOCWE VLIQH ZIR DOGJM IPYL NBY FUTS XIA IZ WUYMUL UHX SIOL OHCKOY MIFONCIH CM IGBULHJZBVFX'

for shift in range(1,27):
    decrypted = ''
    for char in encrypted:
        if char == ' ':
            decrypted = decrypted + ' '
        elif ord(char) + shift > 90:
            decrypted = decrypted + chr((ord(char)+shift)-26)
        else:
            decrypted = decrypted + chr((ord(char)+shift))
    print(shift, " : ", decrypted)