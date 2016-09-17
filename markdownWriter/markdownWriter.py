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
        client = clientDict.get('client')
        contact = clientDict.get('contact')
        title = clientDict.get('title')
        info = clientDict.get('info')
        tags = clientDict.get('tags')
        website = clientDict.get('website')

        titleHyphenated = '-'.join(title.split(' '))
        #print titleHyphenated

        destFile = os.path.join(destMdDir, '{}-{}.md'.format(date, titleHyphenated))
        s = '---\n'
        with open(destFile, 'w') as f:
            #s = '---\nwebsite: {website}\n---\n{info}'.format(website=website, info=info)
            s += 'client: {}\n'.format(client)
            s += 'contact: {}\n'.format(contact)
            s += 'website: {}\n'.format(website)
            
            if len(tags) > 0:
                s += 'tags: {}\n'.format('[{}]'.format(', '.join(tags)))
            s += '---\n\n'

            s += info

            f.write(s)

createMarkdown()