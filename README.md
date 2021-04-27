# togoid-sandbox
## getttl

## CSV2TTL
### メリット
- configをyamlファイル一つで設定でき、辞書のキーの重複がないため、togoid-configと同じ設定ファイルを使える
`togoid-config/config/chembl_compound-chebi/config.yaml`
```config.yaml
link:
  forward:
    label: closeMatch
    namespace: skos
    prefix: http://www.w3.org/2004/02/skos/core#
    predicate: closeMatch
  file: sample.tsv
update:
  frequency: threeTimesAYear
  method: sparql_csv2tsv.sh query.rq https://integbio.jp/rdf/ebi/sparql
```
CSV2TTLのconfig
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
- CSVファイル中のURIをprefixに置換できる。
- 同様にして、CSVファイル中のリテラルに対して言語タグ(現在はja/enに対応)の付与ができる。
- CSVのカラム名を用いてノードが表現できる。
- CSV2TTLのカラムを複数箇所で主語/目的語として使える。

## デメリット
- 空ノードに名前を振っているため、CSVの異なる行の間でノードの重複が起きる（修正対象）。
- 空ノードを用いたネストができない（名前付きノードなら可能）。