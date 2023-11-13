import io
import difflib
in_file = "Med_analiz\медицинские_протоколы.txt"

file = io.open(in_file, encoding='utf-8')

case = {}

def redact(read):
    while True:
        read = read.lower()
        if read.endswith('.') or read.endswith(' '):
            read = read[0:len(read) - 1]
        else:
            return read.strip()

def similarity(s1, s2):
    matcher = difflib.SequenceMatcher(None, s1, s2)
    return matcher.ratio()

def reder(line):
    step = []
    line = line.split(";")[6]
    for i in line.split(","):
        if len(i) > 4:
            i = redact(i)
            i = i.replace("  "," ")
            i = i.replace('"',"")
            i = i.replace('" ',"")
            i = i.strip()
            if "не" not in i and len(i) > 4:
                step.append(i)
    return step
    
indsl = {}

def analiz(line):
    line = reder(line)
    for blok in line:
        if blok in indsl:
            indsl[blok] += 1
        else:
            indsl[blok] = 1


def intersep():
    for key, val in indsl.items():
        for it in case.keys():
            if similarity(key, it) > 0.72 or ((it in key or key in it) and similarity(key, it) > 0.612):
                case[it] += val
                break
        else:
            if val > 10:
                case[key] = val

for line in file:
    analiz(line)

intersep()

for j in range(10):
    final_dict = dict([max(case.items(), key=lambda k_v: k_v[1])])
    for k, y in final_dict.items():
        print(f"{y} - {k}")
    case.pop(k)