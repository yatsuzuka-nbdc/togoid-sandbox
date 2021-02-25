PREFIX dct: <http://purl.org/dc/terms/>
PREFIX orth: <http://purl.org/net/orth#>
PREFIX mbgd: <http://purl.jp/bio/11/mbgd#>
PREFIX taxid: <http://identifiers.org/taxonomy/>
SELECT ?gene ?uniprot
 WHERE {
    ?gene a orth:Gene ;
          mbgd:taxon taxid:9606 ;
          mbgd:uniprot ?uniprot .
}
LIMIT 100