# CSV2TTL
CSVファイルの１レコードをTTL形式のRDFグラフに変換するスクリプト。
# 使い方
```
$ ./CSV2TTL.py -h
usage: CSV2TTL.py [-h] [-o O] [-v] config csv

positional arguments:
  config      yaml config file(required)
  csv         csv file WITH header(required)

optional arguments:
  -h, --help  show this help message and exit
  -o O        output file name(optional)
  -v          increase output verbosity
```
# sample.csvとconfig.yamlの例
```sample.csv
ID,Name,Desc1,Desc2,LandingPageJa,LandingPageEn
sampleID_1,Human,Human is mammalian,ヒトは哺乳類です,https://landingpage.com/ja/human,https://landingpage.com/en/human
```
```config.yaml
EmptyNode:
  [KaraNode1, KaraNode2]

ExistNode:
  [ID, Name, Desc1, Desc2, LandingPageJa, LandingPageEn]

Prefix:
  land: https://landingpage.com/
  pre1: https://prefix1.com/
  pre2: https://prefix2.com/

Triple:
  ID:
  - [pre1:name, Name, ObjectRule1_Literal]
  - [pre1:desc, Desc1, ObjectRule2_Literal_en]
  - [pre1:desc, Desc2, ObjectRule3_Literal_ja]
  - [pre1:seeAlso, KaraNode1, ObjectRule4_URI]
  - [pre1:seeAlso, KaraNode2, ObjectRule4_URI]
  KaraNode1:
  - [pre2:seeAlso, LandingPageJa, ObjectRule4_URI]
  - [pre2:seeAlso, LandingPageEn, ObjectRule4_URI]
  KaraNode2:
  - [pre2:seeAlso, LandingPageJa, ObjectRule5_URI_UsePrefix]
  - [pre2:seeAlso, LandingPageEn, ObjectRule5_URI_UsePrefix]

ObjectRule:
  ObjectRule1_Literal:
    Type: Literal
  ObjectRule2_Literal_en:
    Type: Literal
    Langage: en
  ObjectRule3_Literal_ja:
    Type: Literal
    Langage: ja
  ObjectRule4_URI:
    Type: URI
  ObjectRule5_URI_UsePrefix:
    Type: URI
    UsePrefix: land
```
## EmptyNode
空ノードの名前を指定する。TTLファイルにはこの名前のURIとして吐き出される。
## ExistNode
CSVファイルのカラム名を記載する。
## Triple
RDFトリプルのSPOを指定する。辞書構造のキー（ここではID, KaraNode1, KaraNode2）に主語を、値のリストに述語と目的語をリスト形式で記載する。
述語と目的語のリストに3つめの要素があるが、ここには目的語がリテラルかURIかなどを指定する（ObjectRuleを参照）。
## ObjectRule
目的語の種類がURIかリテラルか、URIならprefixを使うか、言語タグはつけるか、を指定する。

# 実行結果
```
$ ./CSV2TTL.py config.yaml sample.csv
<sampleID_1>
    dcterms:title "Human" :
    dcterms:description "Human is mammalian"@en :
    dcterms:description "ヒトは哺乳類です"@ja :
    rdfs:seeAlso <KaraNode1> :
    rdfs:seeAlso <KaraNode2> .
<KaraNode1>
    rdfs:seeAlso <https://landingpage.com/ja/human> :
    rdfs:seeAlso <https://landingpage.com/en/human> .
<KaraNode2>
    rdfs:seeAlso land:ja/human :
    rdfs:seeAlso land:en/human .
```