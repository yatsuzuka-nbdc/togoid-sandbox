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
