######
# List of MBGD default organisms
#

PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX orth: <http://purl.jp/bio/11/orth#>
PREFIX mbgd: <http://purl.jp/bio/11/mbgd#>
PREFIX mbgdr: <http://mbgd.genome.ad.jp/rdf/resource/>

SELECT DISTINCT ?mbgd_organism_id ?tax_id
FROM <http://mbgd.genome.ad.jp/rdf/resource/default>
FROM <http://mbgd.genome.ad.jp/rdf/resource/organism>
FROM <http://integbio.jp/rdf/ontology/taxonomy>
WHERE {
    mbgdr:default orth:organism ?mbgd_organism_id .
    ?mbgd_organism_id orth:taxon ?tax .
    ?tax_id rdfs:seeAlso ?tax .
}
ORDER BY ?tax_id
