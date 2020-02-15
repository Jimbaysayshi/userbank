def som():
    a = 'aa'
    if len(a) == 1:
        return True


print(som())

with open("programs.txt", "r", encoding='utf-8') as programs:

    print([x for x in programs.readlines()])
