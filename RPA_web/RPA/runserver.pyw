import os
dir_file = os.path.dirname(__file__)
manage_file = (os.path.join(dir_file, 'runserver.bat')).replace('\\', '/')
# print(manage_file)
# os.popen('python %s runserver 0.0.0.0:8080' % manage_file)
os.system('%s' % manage_file)
# f = os.popen('%s' % manage_file)

