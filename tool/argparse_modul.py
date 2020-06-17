import argparse
import os

parser = argparse.ArgumentParser(description='CopyRight my compare. All Rights Reserved')
parser.add_argument('filename', help='input file name')
parser.add_argument('-t', '--type', choice=['p', 'l'], required=True, help='type must be set, p or l')
args = parser.parse_args()
if os.path.exists(args.filename):
    print('file exist')
    if args.type == 'p':
        print('p method')
    elif args.type == 'l':
        print('l method')
