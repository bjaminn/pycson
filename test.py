﻿import sys, os, os.path, json

sys.path.insert(0, os.path.join(os.path.split(__file__)[0], 'cson'))
import cson

total = 0
errors = []

def matches(name):
    return not sys.argv[1:] or name in sys.argv[1:]

srcdir = os.path.join(os.path.split(__file__)[0], 'test', 'parser')
for name in os.listdir(srcdir):
    if not name.endswith('.cson'):
        continue
    if not matches(name):
        continue
    total += 1

    cson_fname = os.path.join(srcdir, name)
    with open(cson_fname, 'rb') as fin:
        try:
            c = cson.load(fin)
        except cson.ParseError as e:
            print('parser/{}({},{}): error: {}'.format(name, e.line, e.col, e.msg))
            errors.append(name)
            continue

    json_name = name[:-5] + '.json'

    with open(os.path.join(srcdir, json_name), 'rb') as fin:
        j = json.loads(fin.read().decode('utf-8'))
    if c != j:
        print('error: {}'.format(name))
        print(repr(c))
        print(repr(j))
        errors.append(name)
        continue
    with open(os.path.join(srcdir, json_name), 'rb') as fin:
        try:
            c = cson.load(fin)
        except cson.ParseError as e:
            print('parser/{}({},{}): error: {}'.format(json_name, e.line, e.col, e.msg))
            errors.append(name)
            continue
    if c != j:
        print('error: {}'.format(name))
        print(repr(c))
        print(repr(j))
        errors.append(name)

srcdir = os.path.join(os.path.split(__file__)[0], 'test', 'writer')
for name in os.listdir(srcdir):
    if not name.endswith('.json'):
        continue
    if not matches(name):
        continue
    total += 1
    json_fname = os.path.join(srcdir, name)
    with open(json_fname, 'rb') as fin:
        j = json.loads(fin.read().decode('utf-8'))

    c = cson.dumps(j, indent=4, sort_keys=True, ensure_ascii=False)

    cson_name = name[:-5] + '.cson'
    with open(os.path.join(srcdir, cson_name), 'rb') as fin:
        cc = fin.read().decode('utf-8').replace('\r\n', '\n')

    if c != cc:
        print('error: {}'.format(name))
        print(repr(c))
        print(repr(cc))
        errors.append(name)
        continue

    try:
        c = cson.loads(c)
    except cson.ParseError as e:
        print('writer/{}({},{}): error: {}'.format(name, e.line, e.col, e.msg))
        errors.append(name)
        continue

    if c != j:
        print('error: {}'.format(name))
        print(repr(c))
        print(repr(j))
        errors.append(name)

if errors:
    sys.exit(1)

print('succeeded: {}'.format(total))
