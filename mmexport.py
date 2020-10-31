import os, re, datetime, piexif, time

DIR = '../mmexport/'


def filenametotimestamp(filename):
    regex = r"mmexport([0-9]+)*.jpg"
    matches = re.finditer(regex, filename, re.MULTILINE)
    timestamp=get_match(matches)
    if (timestamp is None):
        return False, None
    actual = int(timestamp) / 1000
    return True, actual

def get_match(matches):
    for matchNum, match in enumerate(matches, start=1):
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            return match.group(groupNum)
    return None

def getModifiedTime(filename):
    modified_time = os.path.getmtime(DIR+filename)
    return modified_time

def process_mmexport(filename):
    print('file '+filename)
    should_process, timestamp = filenametotimestamp(filename)
    if not should_process:
        return
    timeobj = datetime.datetime.fromtimestamp(timestamp)
    print(timeobj)
    exif_data = piexif.load(DIR+filename)
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
