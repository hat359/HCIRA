import os
import constants

rootdir = os.getcwd() + "/xml_edited_logs/"
gestureList = constants.GESTURE_LIST

for directory in os.listdir(rootdir):
    user = os.path.join(rootdir, directory)
    for fileName in os.listdir(user):
        # print(fileName)    
        data = None
        with open(os.path.join(user,fileName), 'r', encoding='utf-8') as file:
            data = file.readlines()
        for i in range(len(data)):
            data[i] = data[i].replace("\"/>", "\" T=\"{}\"/>".format(i))
            data[i] = data[i].replace("Gesture=","Name=")
            data[i] = data[i].replace("User=","Subject=")
            data[i] = data[i].replace("user","")
            for gesture in gestureList:
                data[i] = data[i].replace("{}".format(gesture),"{}0".format(gesture))
                data[i] = data[i].replace("{}010".format(gesture),"{}10".format(gesture))
        with open(os.path.join(user,fileName), 'w', encoding='utf-8') as file:
            file.writelines(data)