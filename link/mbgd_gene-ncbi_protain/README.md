# MBGD gene to NCBI protein

エンドポイント(http://sparql.nibb.ac.jp/sparql) に以下のクエリを投げた結果をもとに`link.tsv`を作成した。
```
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX orth: <http://purl.org/net/orth#>
PREFIX mbgd: <http://purl.jp/bio/11/mbgd#>

SELECT DISTINCT ?mbgd_gene_id ?protein_id
FROM <http://mbgd.genome.ad.jp/rdf/resource/default>
FROM <http://mbgd.genome.ad.jp/rdf/resource/gene>

 WHERE {
    ?gene a orth:Gene .
    ?gene dct:identifier ?mbgd_gene_id ;
        mbgd:protein ?protein_id .
}
```
source側に`ash`といったprefixらしき文字列が含まれているが、なんのprefixかは今のところ不明である。
以下、謎のprefixの種類と出現回数。`   1 mbgd_gene_id	protein_id`はヘッダー行。

```
🍵mbgd_gene-ncbi_protain$ cat link.tsv | cut -f 1 -d ":"|uniq -c
   1 mbgd_gene_id	protein_id
 842 ash
1412 fna
2704 pfc
3425 thi
1252 gd15668
2869 gd15669
2788 gd15670
2784 gd15671
 801 gd15672
1123 coo
🍵mbgd_gene-ncbi_protain$ 
```