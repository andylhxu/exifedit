import os, re, datetime, piexif, time

DIR = './timedpngtojpg_new/'


def filenametotimestamp(filename):
    regex = r"([0-9]+)_.*\.jpeg"
    matches = re.finditer(regex, filename, re.MULTILINE)
    timestamp=get_match(matches)
    if (not isinstance(timestamp, str)):
        return False, None

    year = '20'+timestamp[0:2]
    yearint = int(year)
    month = int(timestamp[2:4])
    day = int(timestamp[4:6])
    dt = datetime.datetime(yearint, month, day, 0 , 0, 0)
    return True, dt.timestamp()

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
    if not should_process:
        return
#    timestamp = getModifiedTime(filename)
    print('attempting '+str(timestamp))
    timeobj = time.ctime(float(timestamp)/1000)
    timeobj = datetime.datetime.fromtimestamp(float(timestamp)/1000)

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
