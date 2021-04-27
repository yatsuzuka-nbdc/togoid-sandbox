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
sampleID_1,Human,Human is mammalian,ヒトは哺乳類です,https://landingpage.com/human_ja,https://landingpage.com/human_en
```
```config.yaml
EmptyNode:
  [KaraNode1, KaraNode2]

ExistNode:
  [ID, Name, Desc1, Desc2, LandingPageJa, LandingPageEn]

Prefix:
  land: https://landingpage.com/
  dcterms: http://purl.org/dc/terms/
  rdfs: http://www.w3.org/2000/01/rdf-schema#

Triple:
  ID:
  - [dcterms:title, Name, ObjectRule1_Literal]
  - [dcterms:description, Desc1, ObjectRule2_Literal_en]
  - [dcterms:description, Desc2, ObjectRule3_Literal_ja]
  - [rdfs:seeAlso, KaraNode1, ObjectRule4_URI]
  - [rdfs:seeAlso, KaraNode2, ObjectRule4_URI]
  KaraNode1:
  - [rdfs:seeAlso, LandingPageJa, ObjectRule4_URI]
  - [rdfs:seeAlso, LandingPageEn, ObjectRule4_URI]
  KaraNode2:
  - [rdfs:seeAlso, LandingPageJa, ObjectRule5_URI_UsePrefix]
  - [rdfs:seeAlso, LandingPageEn, ObjectRule5_URI_UsePrefix]

ObjectRule:
  ObjectRule1_Literal:
    Type: Literal
  ObjectRule2_Literal_en:
    Type: Literal
    Language: en
  ObjectRule3_Literal_ja:
    Type: Literal
    Language: ja
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
@prefix land: <https://landingpage.com/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<sampleID_1>
    dcterms:title "Human" ;
    dcterms:description "Human is mammalian"@en ;
    dcterms:description "ヒトは哺乳類です"@ja ;
    rdfs:seeAlso <KaraNode1> ;
    rdfs:seeAlso <KaraNode2> .
<KaraNode1>
    rdfs:seeAlso <https://landingpage.com/human_ja> ;
    rdfs:seeAlso <https://landingpage.com/human_en> .
<KaraNode2>
    rdfs:seeAlso land:human_ja ;
    rdfs:seeAlso land:human_en .

```