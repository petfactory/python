import xml.etree.ElementTree as ET
import os

def create_clip_from_xml(path):
    
    tree = ET.parse(path)
    root = tree.getroot()

    for sequence in root.findall("./sequence"):

        seq_duration = sequence.find('duration').text
        seq_name = sequence.find('name').text
        seq_timebase = sequence.find('rate/timebase').text

        media_width = sequence.find('media/video/format/samplecharacteristics/width').text
        media_height = sequence.find('media/video/format/samplecharacteristics/height').text

        print('SEQUENCE', seq_duration, seq_name, seq_timebase, media_width, media_height)
        
        track_list = sequence.findall('media/video/track')
        for track in track_list:
            # print(track)
            # create a track
            for clipitem in track.findall('clipitem'):
                # create clips
                clip_id = clipitem.get('id')
                start = clipitem.find('start').text
                end = clipitem.find('end').text
                in_point = clipitem.find('in').text
                out_point = clipitem.find('out').text
                name = clipitem.find('name').text
                enabled = clipitem.find('enabled').text
                duration = clipitem.find('duration').text

                file_name = clipitem.find('file/name').text
                file_duration = clipitem.find('file/duration').text
                file_path= clipitem.find('file/pathurl').text

                print('CLIP', file_name, file_path, start, end)



file_path = r'/Users/johan/Dev/python/read_xml/sequenser.xml'

if os.path.exists(file_path):
    create_clip_from_xml(file_path)
else:
    print('File does not exist!')



