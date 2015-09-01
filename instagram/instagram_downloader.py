from instagram.client import InstagramAPI
from wand.image import Image
import urllib, os, json, pprint
import os

def on_user_media_feed(dest_dir, client_secret, access_token, year=None, max_count=None):

    def save_image(media, inc):

        url = media.get_standard_resolution_url()
        filename = os.path.basename(url)
        if not os.path.splitext(filename)[1] in ('.jpg'):
            print('Not an image, skipping...')
            return False

        if inc == max_count:
            raise StopIteration('Reached max count')

        md = {}
        md['filename'] = filename
        created_time = media.created_time
        md['date'] = created_time.isoformat()
        caption = media.caption
        md['text'] = caption.text if caption else ''

        if year:
            if media.created_time.year > year:
                print('continuew search...')
                return False

            elif media.created_time.year < year:
                print('Reach max year...abort')
                raise StopIteration('Reached max year')

            else:
                print('{0} {1}'.format(inc, caption))

        # save to disk
        urllib.urlretrieve(url, os.path.join(dest_dir, filename))

        # use wand and imagemagick to resave the image so we can open in adobe apps
        with Image(filename=url) as img:
            img.format = 'jpeg'
            img.save(filename=os.path.join(dest_dir, filename))

        media_list.append(md)

        return True

    if not os.path.isdir(dest_dir):
        print('Not a valid directory')
        return

    ret_dict = {}
    media_list = []
    ret_dict['media'] = media_list
    
    inc = 0
    num_videos = 0
    try:
        api = InstagramAPI(access_token=access_token, client_secret=client_secret)
        user = api.user()
        fullname, bio, username = user.full_name, user.bio, user.username

        ret_dict['fullname'] = fullname
        ret_dict['bio'] = bio
        ret_dict['username'] = username

        media_feed, next = api.user_recent_media()

        for media in media_feed:

            if save_image(media, inc): inc += 1
            else: num_videos +=1


        while next:
            media_feed, next = api.user_recent_media(with_next_url=next)
            for media in media_feed:

                if save_image(media, inc): inc += 1
                else: num_videos +=1


    except StopIteration as e:
        print(e)

    finally:

        print('Total media: {0}\nDownloaded {1} image(s).\nSkipped {2} videos'.format((inc+num_videos), inc, num_videos))
        # reverse the media list so a year starts with the oldest media
        media_list.reverse()
        #pprint.pprint(ret_dict)
        json_data = json.dumps(ret_dict, indent=4)
        #pprint.pprint(json_data)
        file_name = os.path.join(dest_dir, 'instagram.json')
        with open(file_name, 'w') as f:
            f = open(file_name,'w')
            f.write(json_data)
            f.close()

client_secret = str(raw_input("Client secret: "))
access_token = str(raw_input("Access token: "))
year = raw_input("Year [None]:")
year = None if year == '' else int(year)
maxcount = raw_input("Max count [None]: ")
maxcount = None if maxcount == '' else int(maxcount)
dest_dir = str(raw_input("Directory to download to: "))

on_user_media_feed(dest_dir, client_secret, access_token, year, maxcount)
