import os, shutil
import json
import pprint

def createMarkdown():

    scriptDir = os.path.dirname(os.path.realpath(__file__))
    jsonSrcPath = os.path.join(scriptDir, 'cv.json')
    destMdDir = os.path.join(scriptDir, '_md')

    if os.path.isdir(destMdDir):
        print 'rem dir'
        shutil.rmtree(destMdDir)
    
    os.makedirs(destMdDir)
        
    json_data = None
    with open(jsonSrcPath, 'r') as f:
        data = f.read()
        json_data = json.loads(data)

    if json_data is None:
        return

    for clientDict in json_data.get('cv'):
        date = clientDict.get('date')
        title = clientDict.get('title')
        info = clientDict.get('info')
        tags = clientDict.get('tags')
        website = clientDict.get('website')

        destFile = os.path.join(destMdDir, '{}-{}'.format(date, title))
        with open(destFile, 'w') as f:
            s = '---\nwebsite: {website}\n---\n{info}'.format(website=website, info=info)
            f.write(s)

createMarkdown()