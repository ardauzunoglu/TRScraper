def degerkontrol():
    girdi = input("Değer: ")
    while not girdi.isdigit():
        print("tekrar")
        girdi = input("Değer: ")

    else:
        return "bu bir sayi"

print(degerkontrol())