import pickle

with open('model_file', 'rb') as fp:
    content = pickle.load(fp)
    print(content, type(content))
    # for i in range(content):
    # line = pickle.loads(content)
    # print(line)

