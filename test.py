import json
import os
from xml.dom import minidom
from shutil import rmtree

  
# # Opening JSON file
# f = open('database.json')
  
# # returns JSON object as 
# # a dictionary
# data = json.load(f)

# for user in data:
#     print('--------------')
#     print(user)
#     print('*****')
#     for gesture in data[user]:
#         print(gesture,len(data[user][gesture]))

def createXMLUserLogs():
    file = open('database.json')
    user_data = json.load(file)
    file.close()
    
    root = os.getcwd()
    log_directory_name = 'xml_collected_logs'
    log_directory_path = os.path.join(root, log_directory_name)
    rmtree(log_directory_path)
    os.makedirs(log_directory_path)

    for user in user_data:
        # print(user)
        user_path = os.path.join(log_directory_path, user)
        os.makedirs(user_path)
        for gesture in user_data[user]:
            # print(gesture)
            # print(len(user_data[user][gesture]))
            for i in range(0,len(user_data[user][gesture])):
                pointList = user_data[user][gesture][i]
                print(user, gesture, len(pointList))
                root = minidom.Document()
                gestureChild = root.createElement('Gesture')
                gestureChild.setAttribute('User', str(user))
                gestureChild.setAttribute('Gesture', '{}{}'.format(gesture,i+1))
                gestureChild.setAttribute('Number', str(i+1))
                gestureChild.setAttribute('NumPts', str(len(pointList)))
                root.appendChild(gestureChild)
                for point in pointList:
                    pointChild = root.createElement('Point')
                    pointChild.setAttribute('X', str(point[0]))
                    pointChild.setAttribute('Y', str(point[1]))
                    gestureChild.appendChild(pointChild)
                    gestureRootString = root.toprettyxml(indent= "\t")
                    file_name = '{}{}.xml'.format(gesture,i+1)
                    file_path = os.path.join(user_path, file_name)
                    with open(file_path, "w") as file:
                        file.write(gestureRootString) 







createXMLUserLogs()