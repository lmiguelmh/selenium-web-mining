# @author lmiguelmh
# @since 
from os import listdir
from os.path import isfile, join

basedir = "txt"
encoding = "utf8"
files = [basedir+"/"+f for f in listdir(basedir) if isfile(join(basedir, f))]
words = ["chambear", "bamba", "jama", "chancar", "chela", "papayita", "jatear", "jato", "tombo", "tranca",
         "huasca", "choborra", "cacharro", "chongo", "chupodromo", "fercho", "huachimán", "latear", "lompa",
         "mitra", "jeta", "moquear", "ni michi", "ñanga", "ñoba", "telo", "panudo"]

for file in files:
    with open(file, encoding=encoding) as f:
        content = f.read()

    foundwords = []
    for word in words:
        if word in content:
            foundwords.append(word)

    try:
        with open(file + ".clase.txt", 'wb') as f:
            for word in foundwords:
                f.write(bytes(word + "\n", encoding=encoding))
    except Exception as e:
        print(e)
        pass
