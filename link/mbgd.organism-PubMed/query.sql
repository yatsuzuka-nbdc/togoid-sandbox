######
# Get PMID from MBGD organisms
#

PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX orth: <http://purl.jp/bio/11/orth#>
PREFIX mbgdr: <http://mbgd.genome.ad.jp/rdf/resource/>
PREFIX dct: <http://purl.org/dc/terms/>

SELECT DISTINCT ?mbgd_organism_id ?pubmed_id
FROM <http://mbgd.genome.ad.jp/rdf/resource/default>
FROM <http://mbgd.genome.ad.jp/rdf/resource/organism>
WHERE {
    mbgdr:default orth:organism ?mbgd_organism_id .
    ?mbgd_organism_id dct:references ?pubmed_id .
}
ORDER BY ?mbgd_organism_id