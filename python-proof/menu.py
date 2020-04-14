# By Isabella Scollo

print("Guess the lyrics\n")

pf = open("lyrics.txt")
song = pf.read()
pf.close()
song_final = ""

for i in song:
    if i not in [",","-",".","!","?","/"]:
        song_final+=i.lower()

data_imp = song_final.split()
data = []
max_len=0
found_words = []
win = False

col = (len(data_imp)//20)+1
if len(data_imp)>319:
    col = 16

for i in data_imp:
    if len(i)>max_len:
        max_len=len(i)

for i in range((len(data_imp)//col)+1):
    data.append([])

count = 0
while count<(len(data)*col):
    for i in range(len(data)):
        if count<len(data_imp):
            data[i].append(data_imp[count])
        else:
            data[i].append(None)
        count += 1

data = [j for i in data for j in i]

count = 0
print(f"0/{len(data_imp)}")
while count<len(data):
    line = ""
    for i in range(col):
        if count<len(data):
            if data[count] is None:
                line += (" "*((max_len)+1))
            else:
                line += ("-"*(max_len))+" "
        else:
            break
        count+=1
    print(line)

while True:

    new_word= input("Enter word: ").lower()

    if (new_word in data) and (new_word not in found_words):
        found_words.append(new_word)
        count = 0
        got = 0
        win = True
        while count<len(data):
            line = ""
            for i in range(col):
                if count<len(data):
                    if data[count] is None:
                        line += (" "*((max_len)+1))
                    elif data[count] in found_words:
                        line += data[count]+(" "*(max_len-len(data[count])+1))
                        got += 1
                    else:
                        win = False
                        line += ("-"*(max_len))+" "
                else:
                    break
                count+=1
            print(line)
        print(f"\n{got}/{len(data_imp)}")
    if win:
        print("\nyou win!\n")
        break


