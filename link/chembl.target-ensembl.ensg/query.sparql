PREFIX cco: <http://rdf.ebi.ac.uk/terms/chembl#>
SELECT   ?moleculeid ?ensg
WHERE{
?mechanism a cco:Mechanism ;
     cco:hasTarget ?target ;
     cco:hasMolecule ?molecule .
  ?target cco:hasTargetComponent ?component .
  ?component cco:targetCmptXref ?ensg .
  FILTER(CONTAINS(STR(?ensg), "ENSG"))
  ?molecule cco:chemblId ?moleculeid .            
  }