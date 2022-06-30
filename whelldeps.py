import argparse
from zipfile import ZipFile

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

archive = ZipFile(args.filename)
for f in archive.namelist():
    if f.endswith("METADATA"):
        for l in archive.open(f).read().decode("utf-8").split("\n"):
            if 'requires-dist' in l.lower():
                print(l)