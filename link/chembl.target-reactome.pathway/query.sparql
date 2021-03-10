PREFIX cco: <http://rdf.ebi.ac.uk/terms/chembl#>
SELECT   ?moleculeid ?reactome
WHERE{
  ?mechanism a cco:Mechanism ;
     cco:hasTarget ?target ;
     cco:hasMolecule ?molecule .
  ?target cco:hasTargetComponent ?component .
  ?component cco:targetCmptXref ?reactome .
  FILTER(CONTAINS(STR(?reactome), "reactome"))
  ?molecule cco:chemblId ?moleculeid .
  }