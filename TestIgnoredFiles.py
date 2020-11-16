import accessories
import exifread

filename = "thumbs.db"
filename ="/mnt/source/Teambuilding/From MOGX/MOG_Repository/2003/20030421_PresidenteRepublica_visitaMOG/Fotografo_TecMaia/10203423/F1020001.JPG"
if filename not in accessories.IgnoredFiles():
    print("yes")
    
print(accessories.GetFileDate(filename))

# f = open(filename, 'rb')
# tags = exifread.process_file(f)
# for tag in tags.keys():
#     TagValue = tags[tag]
#     # print("%s = %s" % (tag, tags[tag]))