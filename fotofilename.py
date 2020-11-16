import os
#Scan source directory and remove special chars from paths and filenames
source = "/mnt/source"
#
replace = [["Ã","A"], ["õ","o"], ["@","_"], ["%",""], ["^",""], ["~",""], ["ª",""], ["ó","o"], ["É","E"], ["│",""], ["├",""], ["³",""], ["'",""], ["ç","c"],["à","a"], ["é","e"], ["ã","a"], ["á","a"], ["í","i"], ["Ç","C"], ["ô","o"], ["&","-"], ["云",""], ["卷",""], ["舒",""], ["舒",""], ["卷",""], ["焰",""], ["火",""], ["色",""], ["蓝",""], ["染",""], ["晕",""], ["+",""]]
count = 0 
renamed = 0
errors = 0
for path,dirs,files in os.walk(source):
    for filename in files:
        filepath = os.path.join(path, filename)
        size = os.stat(filepath).st_size
        for special in replace:
            special_char = filename.find(special[0])
            if special_char > -1:
                print (filepath)
                newfilepath = filepath.replace(special[0], special[1])
                print (newfilepath)
                count +=1
                try:
                    os.rename(filepath, newfilepath)
                    print ("File renamed : %s" % (newfilepath))
                    renamed += 1
                except Exception as error:
                    print ("File not renamed : %s, %s" % (filepath, error))
                    errors += 1
print ("Renamed : %s" % renamed)
print ("Errors  : %s" % errors)
print ("Total   : %s" % count)