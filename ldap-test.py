import ldif

interessant = [b"TSIdevice",b"inetOrgperson"]

def sharedClasses(entry, classes):
    return compareClasses(entry,classes).count(True)

def compareClasses(entry, classes):
    return [(x in entry["objectclass"]) for x in classes]

with open('datensatz','r') as f:
    recordList = ldif.LDIFRecordList(f)
    recordList.parse()
    for (dn, entry) in recordList.all_records:
        print(sharedClasses(entry, interessant))
