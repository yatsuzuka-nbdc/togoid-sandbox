import copy
import csv
import json
import os
import re


print('PATH TO INPUT FILE?')
FNAME = input()
fname_prefix = '.'.join(FNAME.split('.')[0:(len(FNAME.split('.')) - 1)])
FNAME_CONFIG = '{}_csv2ttl_config'.format(fname_prefix)
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


def dtype(s):
    str2dtype = {'double': '^^xsd:double', 'decimal': '^^xsd:decimal', 'integer': '^^xsd:integer'}
    if not s in str2dtype: return ''
    return str2dtype[s]


def write_vo(col_idx, pred, content, dtype, lang):
    assert pred != ''
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


# Parse the hierarchical structure in config.csv.
def rec_hier(rows, if_specified, pred=None, depth=0, r=0):
    assert depth < len(rows[r])
    ret = []
    while r < len(rows):
        assert '' != rows[r][depth]
        if re.match(r'\d+', rows[r][depth]) is None:
            pair, r, if_specified = rec_hier(rows, if_specified, pred=rows[r][depth], depth=depth+1, r=r)
            ret.append(pair)
        else:
            if_specified[int(rows[r][depth])] = True
            ret.append(int(rows[r][depth]))
            r += 1
    if depth > 0: return (pred, ret), r, if_specified
    else: return ret, if_specified


# Output the hierarchical structure according to parse result.
def output_ds(row, dat_structure, depth, preds, dtypes, langs):
    ret, buf = '', ''
    for e in dat_structure:
        if '' != buf:
            ret += buf + '; \n'
            buf = ''
        if type(e) is tuple:
            buf += '{} [\n{}] '.format('\t' * depth + e[0], output_ds(row, e[1], depth + 1, preds, dtypes, langs))
        else:
            idx = int(e)
            ret += '\t' * depth
            buf += write_vo(idx, preds[idx], row[idx], dtype(dtypes[idx]), langs[idx])
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
                    if len(rows_hier) > 0: dat_structure, if_specified = rec_hier(rows_hier, if_specified)
                    continue
                rows_hier.append(strip_list(row))
            elif 'NAMESPACE' == target_content: f.write('@prefix {0}: <{1}> .\n'.format(row[0], row[1]))
            else: target_content = ''
    f.write('\n')
    assert ENCODING is not None
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

                # Skip empty column
                if '' == row[j]: continue
                # Process multi values in one column
                elif MULTIVALUE_SEPARATOR is not None and IF_MULTIVALUE[j]:
                    names = row[j].split(MULTIVALUE_SEPARATOR)
                    for e in names:
                        if writebuf is not None: f.write(writebuf + ';\n')
                        writebuf = '\t' + write_vo(j, PRED[j], e, dtype(DTYPE[j]), LANG[j])
                else:
                    if writebuf is not None: f.write(writebuf + ';\n')
                    writebuf = '\t' + write_vo(j, PRED[j], row[j], dtype(DTYPE[j]), LANG[j])
            if dat_structure is None: f.write(writebuf + '.\n\n')
            else:
                if writebuf is not None: f.write(writebuf + ';\n')
                f.write(output_ds(row, dat_structure, 1, PRED, DTYPE, LANG) + '.\n\n')

    f.close()


if __name__ == '__main__':
    main()
