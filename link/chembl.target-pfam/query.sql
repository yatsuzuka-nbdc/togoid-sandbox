PREFIX cco: <http://rdf.ebi.ac.uk/terms/chembl#>
SELECT   ?moleculeid ?pfam
WHERE{
  ?mechanism a cco:Mechanism ;
     cco:hasTarget ?target ;
     cco:hasMolecule ?molecule .
  ?target cco:hasTargetComponent ?component .
  ?component cco:targetCmptXref ?pfam .
  FILTER(CONTAINS(STR(?pfam), "pfam"))
  ?molecule cco:chemblId ?moleculeid .
  }