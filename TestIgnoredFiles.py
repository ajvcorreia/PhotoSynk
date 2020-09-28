import accessories

filename = "thumbs.db"
if filename not in accessories.IgnoredFiles():
    print("yes")