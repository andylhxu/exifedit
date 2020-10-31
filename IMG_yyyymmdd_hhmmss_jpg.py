import os, re, datetime, piexif, time

DIR = '../dates_img/'


def filenametotimestamp(filename):
    regex = r"IMG_([0-9]+)*_([0-9]+)*.jpg"
    matches = re.finditer(regex, filename, re.MULTILINE)
    (date, time)=get_match(matches)
    if (date is None):
        return False, None
    year = date[0:4]
    yearint = int(year)
    month = int(date[4:6])
    day = int(date[6:8])
    hour = int(time[0:2])
    minu = int(time[2:4])
    sec = int(time[4:6])
    dt = datetime.datetime(yearint, month, day, hour, minu, sec)
    return True, dt.timestamp()

def get_match(matches):
    for matchNum, match in enumerate(matches, start=1):
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            return (match.group(groupNum), match.group(groupNum+1))
    return (None,None)

def getModifiedTime(filename):
    modified_time = os.path.getmtime(DIR+filename)
    return modified_time

def process_mmexport(filename):
    print('file '+filename)
    should_process, timestamp = filenametotimestamp(filename)
    if not should_process:
        return
    print('attempting '+str(timestamp))
    return
    timeobj = datetime.datetime.fromtimestamp(timestamp)

    exif_data = piexif.load(DIR+filename)
 #   print(exif_data)
    datetimestring = timeobj.strftime('%Y:%m:%d %H:%M:%S')
    exif_data['Exif'][36867] = datetimestring
    exif_data['Exif'][36868] = datetimestring
    exif_bytes = piexif.dump(exif_data)
    piexif.insert(exif_bytes, DIR+filename)
    print('done inserting')

def main():
    # get all files in this dir
    result = os.listdir(DIR)
    for filename in result:
        process_mmexport(filename)

main()
