import copy
import csv
import json
import os
import re


print('PATH TO INPUT FILE?')
FNAME = input()
fname_prefix = '.'.join(FNAME.split('.')[0:(len(FNAME.split('.')) - 1)])
FNAME_CONFIG = '{}_genttl_config'.format(fname_prefix)
# Parse the config json and write prefixes
if os.path.exists(FNAME_CONFIG + '.json'):
    with open(FNAME_CONFIG + '.json', 'r', encoding='utf-8', errors='ignore') as fin:
        WORD2OWL = json.load(fin)
else: WORD2OWL = {}
assert WORD2OWL is not None


def strip_list(list):
    for i in range(len(list)):
        if '' != list[len(list) - 1 - i]: return list[:len(list)-i]
    assert False


def obj(s, type):
    return s


def dtype(s):
    if 'double' == s:
        return '^^xsd:double'
    elif 'decimal' == s:
        return '^^xsd:decimal'
    elif 'integer' == s:
        return '^^xsd:integer'
    else: return ''


def create_vo(col_idx, pred, content, dtype, lang):
    if str(col_idx) in WORD2OWL:
        if content in WORD2OWL[str(col_idx)]:
            content = WORD2OWL[str(col_idx)][content]
            return "{0} {1} ".format(pred, content)
    if re.match(r'https{,1}://[^ ]*', content) is not None:
        return "{0} <{1}> ".format(pred, content)
    if re.match(r'.*[\'\n\r].*', content) is None:
        return "{0} '{1}'{2}{3} ".format(pred, content, dtype, lang)
    else:
        content = content.replace("'", "\\'")
        return "{0} '''{1}'''{2}{3} ".format(pred, content, dtype, lang)


def rec_hier_sub(pred, depth, rows, r, if_specified):
    ret = []
    while True:
        assert not '' == rows[r][depth]
        if not re.compile(r'^\d+$').match(rows[r][depth]):
            pair, r, if_specified = rec_hier_sub(rows[r][depth], depth + 1, rows, r, if_specified)
            ret.append(pair)
            if len(rows) <= r: break
        else:
            if_specified[int(rows[r][depth])] = True
            ret.append(int(rows[r][depth]))
            r += 1
            if len(rows) <= r: break
            if depth >= len(rows[r]): break
    return (pred, ret), r, if_specified


def rec_hier(rows, if_specified):
    ret, r, depth = [], 0, 0
    while r < len(rows):
        assert not '' == rows[r][0]
        if type(rows[r][0]) is not int:
            pair, r, if_specified = rec_hier_sub(rows[r][0], 1, rows, r, if_specified)
            ret.append(pair)
        else:
            if_specified[int(rows[r][depth])] = True
            ret.append(int(rows[r][depth]))
            r += 1
    return ret, if_specified


def output_ds_sub(row, dat_structure, depth, lst_pred, lst_dtype, lst_lang):
    ret, buf = '', ''
    for e in dat_structure:
        if '' != buf:
            ret += buf + '; \n'
            buf = ''
        if type(e) is tuple:
            buf += '{} [\n'.format('\t' * depth + e[0])
            output_ds_sub(row, e[1], depth + 1, lst_pred, lst_dtype, lst_lang)
            buf += '] '
        else:
            idx = int(e)
            ret += '\t' * depth
            buf += create_vo(idx, lst_pred[idx], obj(row[idx], idx), dtype(lst_dtype[idx]), lst_lang[idx])
    if '' != buf: ret += buf

    return ret


def output_ds(row, dat_structure, lst_pred, lst_dtype, lst_lang):
    ret, depth, buf = '', 1, ''
    for e in dat_structure:
        if '' != buf:
            ret += buf + '; \n'
            buf = ''
        if type(e) is tuple:
            buf += '{} [\n'.format('\t' * depth + e[0])
            buf += output_ds_sub(row, e[1], depth + 1, lst_pred, lst_dtype, lst_lang)
            buf += '] '
        else:
            idx = int(e)
            ret += '\t' * depth
            buf += create_vo(idx, lst_pred[idx], obj(row[idx], idx), dtype(lst_dtype[idx]), lst_lang[idx])
    if '' != buf: ret += buf

    return ret


def main():
    PRED, DTYPE, LANG, IF_MULTIVALUE = [], [], [], []  # for each column
    ENCODING = None
    if_specified = None  # If the column is specified as included in hierarchical structure
    dat_structure = None  # Hierarchical structure

    # Output file
    f = open('{}.ttl'.format(fname_prefix), 'w', newline='', encoding='utf-8', errors='ignore')

    # Parse the config file and write prefixes
    with open(FNAME_CONFIG + '.csv', 'r', encoding='utf-8', errors='ignore') as fin:
        csvreader, target_content, rows_hier = csv.reader(fin), '', []
        for row in csvreader:
            if '' == target_content: target_content = row[0].split(' ')[1]
            elif 'ENCODING' == target_content: tmp, target_content = copy.copy(row), 'ENCODING2'
            elif 'ENCODING2' == target_content:
                tmp2 = copy.copy(row)
                for j in range(len(tmp2)):
                    if '1' == tmp2[j]:
                        ENCODING = tmp[j]
                        break
                target_content = ''
            elif 'SUBJECT' == target_content:
                sbj_col = int(row[0])
                sbj_uri = row[1]
                target_content = ''
            elif 'PREDICATE' == target_content:
                PRED, target_content = copy.copy(row), ''
                if_specified = [False] * len(PRED)
            elif 'DTYPE' == target_content:
                DTYPE, target_content = copy.copy(row), ''
                for _ in range(len(DTYPE), len(PRED)): DTYPE.append('')
            elif 'LANG' == target_content:
                LANG = copy.copy(row)
                for _ in range(len(LANG), len(PRED)): LANG.append('')
                for j in range(len(LANG)):
                    if LANG[j] != '': LANG[j] = '@{0}'.format(LANG[j])
                target_content = ''
            elif 'MULTI?' == target_content:
                for j in range(len(row)): IF_MULTIVALUE.append(row[j] != '0')
                for _ in range(len(IF_MULTIVALUE), len(PRED)): IF_MULTIVALUE.append(True)
                target_content = ''
            elif 'ITEM_SEPARATOR' == target_content:
                target_content = ''
                if 0 == len(row):
                    MULTIVALUE_SEPARATOR = None
                if 1 == len(row):
                    MULTIVALUE_SEPARATOR = row[0]
                if 2 <= len(row):
                    MULTIVALUE_SEPARATOR = row[0] + '\n'
            elif 'HIERARCHY' == target_content:
                if '<<' == row[0].split(' ')[0]:
                    target_content = row[0].split(' ')[1]
                    assert if_specified is not None
                    dat_structure, if_specified = rec_hier(rows_hier, if_specified)
                    continue
                rows_hier.append(strip_list(row))
            elif 'NAMESPACE' == target_content: f.write('@prefix {0}: <{1}> .\n'.format(row[0], row[1]))
            else: target_content = ''
    f.write('\n')
    assert ENCODING is not None
#    PRED_TYPE = 'rdfs:type'
    for i in range(len(if_specified)):
        if '' == PRED[i]: if_specified[i] = True

    # Parse the data file
    with open(FNAME, 'r', encoding=ENCODING, errors='ignore') as fin:
        csvreader = csv.reader(fin)
        for i, row in enumerate(csvreader):

            # Skip the first row as labels
            if 0 == i: continue

            writebuf = None
            f.write('<{0}>\n'.format(sbj_uri.replace('*ID*', row[sbj_col])))
            for j in range(len(row)):
                if_duplicated = False

                # Check duplication and if the column is in hierarchical structure
                for k in range(j):
                    if row[k] == row[j] and LANG[k] == LANG[j] and DTYPE[k] == DTYPE[j] and PRED[k] == PRED[j]:
                        if_duplicated = True
                        break
                if if_specified[j] or if_duplicated: continue

#                elif 1 == j:
#                    if writebuf is not None: f.write(writebuf + ';\n')
#                    writebuf = '\t{0} "{1}"{2}{3} '.format(PRED_TYPE, obj(row[1], 1), dtype(DTYPE[1]), LANG[1])

                # Skip empty column
                if '' == row[j]: continue
                # Process multi values in one column
                elif MULTIVALUE_SEPARATOR is not None and IF_MULTIVALUE[j]:
                    names = row[j].split(MULTIVALUE_SEPARATOR)
                    for e in names:
                        if writebuf is not None: f.write(writebuf + ';\n')
                        writebuf = create_vo(j, PRED[j], obj(e, j), dtype(DTYPE[j]), LANG[j])
                else:
                    if writebuf is not None: f.write(writebuf + ';\n')
                    writebuf = create_vo(j, PRED[j], obj(row[j], j), dtype(DTYPE[j]), LANG[j])
            if writebuf is not None: f.write(writebuf + ';\n')
            if dat_structure is not None: writebuf = output_ds(row, dat_structure, PRED, DTYPE, LANG)
            f.write(writebuf + '.\n\n')

    f.close()


if __name__ == '__main__':
    main()
