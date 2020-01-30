import ldif

ALL_STRUCTURALS = [b"TSIdevice",b"inetOrgPerson",b"device", b"person"]

DEFAULT_STRUCTURAL = b"DEFAULTOC"

STRUCTURAL_OBJECTCLASS_MAPPING = {
    (b"device",b"inetOrgPerson") : [ b"TSIdevice",b"dummyPerson" ]






}




def sharedClasses(entry, classes):
    return compareClasses(entry,classes).count(True)

def compareClasses(entry, classes):
    return [(x in entry["objectclass"]) for x in classes]

def splitClasses(entry, classesToInspect):
    """
    Nimmt einen Record und gibt ein Tupel (a, b) mit
        a alle Klassen in classesToInspect
        b alle Klassen NICHT in classesToInspect
    """
    present = []
    absent = []
    for x in entry["objectclass"]:
        if x in classesToInspect: present.append(x)
        else: absent.append(x)
    present.sort()
    absent.sort()
    return (present, absent)


def addMissingStructural(entry):
    entry["objectclass"].append(DEFAULT_STRUCTURAL)

def reduceMultipleStructural(entry):
    structurals, nonstructurals = splitClasses(entry, ALL_STRUCTURALS)
    if tuple(structurals) in STRUCTURAL_OBJECTCLASS_MAPPING:
        entry["objectclass"] = nonstructurals + STRUCTURAL_OBJECTCLASS_MAPPING[tuple(structurals)]
    else: pass


with open('datensatz','r') as f:
    recordList = ldif.LDIFRecordList(f)
    recordList.parse()
    for (dn, entry) in recordList.all_records:
        print(dn, entry)

        if (sharedClasses(entry, ALL_STRUCTURALS) == 0):
            addMissingStructural(entry)
        if (sharedClasses(entry, ALL_STRUCTURALS) == 2):
            reduceMultipleStructural(entry)

        print(dn, entry, "\n")




