PREFIX cco: <http://rdf.ebi.ac.uk/terms/chembl#>
SELECT   ?moleculeid ?interpro
WHERE{
  ?mechanism a cco:Mechanism ;
     cco:hasTarget ?target ;
     cco:hasMolecule ?molecule .
  ?target cco:hasTargetComponent ?component .
  ?component cco:targetCmptXref ?interpro .
  FILTER(CONTAINS(STR(?interpro), "interpro"))
  ?molecule cco:chemblId ?moleculeid .
  }