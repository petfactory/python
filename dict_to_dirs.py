import os
import json
#from shutil import rmtree

class ProjectSetup:

    @staticmethod
    def build_relative_dirs(dir_dict, parent_list):

        for dir_name, sub_dir in dir_dict.iteritems():

            #print('{0}/{1}'.format('/'.join(parent_list), dir_name))
            os.mkdir(os.path.join('/'.join(parent_list), dir_name))

            # if dict, recurse
            if isinstance(sub_dir, dict):
                # we step one level down
                parent_list.append(dir_name)
                ProjectSetup.build_relative_dirs(sub_dir, parent_list)

            # leaf nodes
            elif isinstance(sub_dir, list):
                # we step one level down
                parent_list.append(dir_name)
                for d in sub_dir:
                    #print('{0}/{1}'.format('/'.join(parent_list), d))
                    os.mkdir(os.path.join('/'.join(parent_list), d))

            # step one level up
            parent_list.pop()

    @staticmethod
    def build_dirs_from_dict(root, dir_dict):
        # check if the dir exists
        if os.path.isdir(root):
            print('Directory exists: {0}'.format(root))
            # debug remove
            #rmtree(root)

        else:
            os.makedirs(root)
            ProjectSetup.build_relative_dirs(dir_dict, [root])


j = {
    "afx": {
        "project": [],
        "media": {
            "images": {
                "raw": [
                    "ai",
                    "psd",
                    "eps"
                ],
                "optimized": []
            },
            "audio": {
                "music": [],
                "voice_over": [],
                "sfx": [
                    "metal",
                    "organic"
                ]
            }
        }
    }
}

ROOT = r'/Users/johan/Desktop/root'
ProjectSetup.build_dirs_from_dict(ROOT, j)
