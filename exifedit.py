import os, re, datetime, piexif, time

DIR = '../timedpngtojpg_todo/'


def filenametotimestamp(filename):
    regex = r"([0-9]+)\.jpeg"
    matches = re.finditer(regex, filename, re.MULTILINE)
    timestamp=get_match(matches)
    if (not isinstance(timestamp, str)):
        return False, None
    return True, float(timestamp)
    # year = '20'+timestamp[0:2]
    # yearint = int(year)
    # month = int(timestamp[2:4])
    # day = int(timestamp[4:6])
    # dt = datetime.datetime(yearint, month, day, 0 , 0, 0)
    # return True, dt.timestamp()

def get_match(matches):
    for matchNum, match in enumerate(matches, start=1):
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            return match.group(groupNum)

def getModifiedTime(filename):
    modified_time = os.path.getmtime(DIR+filename)
    return modified_time

def process_mmexport(filename):
    print('file '+filename)

    should_process, timestamp = filenametotimestamp(filename)
#    should_process = ('jpg' in filename)
    if not should_process:
        return
 #   timestamp = getModifiedTime(filename)
    print('attempting '+str(timestamp))
    timeobj = datetime.datetime.fromtimestamp(timestamp)

    exif_data = piexif.load(DIR+filename)
 #   print(exif_data)
    datetimestring = timeobj.strftime('%Y:%m:%d %H:%M:%S')
    exif_data['Exif'][36867] = datetimestring
    exif_bytes = piexif.dump(exif_data)
    piexif.insert(exif_bytes, DIR+filename)
    print('done inserting')

def main():
    # get all files in this dir
    result = os.listdir(DIR)
    for filename in result:
        process_mmexport(filename)

main()
