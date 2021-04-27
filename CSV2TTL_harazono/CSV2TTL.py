#! /usr/bin/env python3
import sys
import argparse
import pprint
import yaml
import csv
import re
pp = pprint.PrettyPrinter(indent=2)
ttlIndent = "    "


def formatPrefix(prefix_dict):
    returnStr = ""
    for each_prefix in prefix_dict:
        returnStr += f"@prefix {each_prefix}: <{prefix_dict[each_prefix]}> .\n"
    return returnStr


def formatObject(object_, formatting_rule, prefix_dict):
    returnStr = ""
    if formatting_rule is None:
        returnStr = object_
    else:
        quoter1 = ""
        quoter2 = ""
        suffix  = ""
        for each_key in formatting_rule.keys():
            each_value = formatting_rule[each_key]
            if each_key == "Type":
                if each_value == "URI":
                    quoter1 = "<"
                    quoter2 = ">"
                elif each_value == "Literal":
                    quoter1 = '"'
                    quoter2 = '"'
                    if '"' in object_:
                        quoter1 = "'"
                        quoter2 = "'"
                    if "\n" in object_:
                        quoter1 = quoter1 * 3
                        quoter2 = quoter2 * 3

            elif each_key == "Language":
                if each_value in ["ja", "en"]:
                    suffix = f"@{each_value}"

            elif each_key == "UsePrefix":
                prefixShort = each_value.strip()
                prefixLong = prefix_dict[each_value].strip()
                if object_.startswith(prefixLong):
                    returnStr = f"{prefixShort}:{object_[len(prefix_dict[each_value]):]}"
                    quoter1 = ""
                    quoter2 = ""
                    return returnStr
            returnStr = f"{quoter1}{object_}{quoter2}{suffix}"
    return returnStr


#{"<sampleID_1>", ['''dcterms:title "Human"''', burasagaru moji 2,...,]}


def dict2rdf(input_dict, config_dict):
    returnStr = ""
    for triple_subject_node in config_dict["Triple"]:
        triple_definitions = config_dict["Triple"][triple_subject_node]
        if triple_subject_node in config_dict["ExistNode"]:
            subject = input_dict[triple_subject_node]

            returnStr += f"<{subject}>\n"
            for each_definition in triple_definitions:
                predicate = each_definition[0]
                object_ = input_dict.get(each_definition[1])
                if object_ is None:#述語が空ノードの場合
                    object_ = f"<{each_definition[1]}>"
                else:#述語が空ノードでなく、加工が必要な場合の処理
                    object_ = formatObject(object_, config_dict["ObjectRule"][each_definition[2]], config_dict["Prefix"])
                returnStr += f"{ttlIndent}{predicate} {object_} ;\n"
            returnStr = returnStr[:-2] + ".\n"
    return returnStr

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="yaml config file(required)")
    parser.add_argument("csv", help="csv file WITH header(required)")
    parser.add_argument("-o", help="output file name(optional)")
    parser.add_argument("-v", help="increase output verbosity", action='store_true')
    args = parser.parse_args()
    config_fn = args.config
    config_dict = None
    with open(config_fn, "r") as f:
        config_dict = yaml.safe_load(f)
    if args.v:
        print(pp.pformat(config_dict), file = sys.stderr)
    csv_fn = args.csv
    output_stream = sys.stdout
    if args.o:
        output_stream = open(args.o, "w")
    print(formatPrefix(config_dict["Prefix"]), file = output_stream)
    with open(csv_fn, "r") as f:
        reader = csv.DictReader(f)
        for each_record in reader:
            rdf = dict2rdf(each_record, config_dict)
            print(rdf, file = output_stream)
    output_stream.close()


if __name__ == '__main__':
    main()