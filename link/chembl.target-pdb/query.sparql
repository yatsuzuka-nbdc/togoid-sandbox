PREFIX cco: <http://rdf.ebi.ac.uk/terms/chembl#>
SELECT ?moleculeid ?pdb
WHERE{
  ?mechanism a cco:Mechanism ;
     cco:hasTarget ?target ;
     cco:hasMolecule ?molecule .
  ?target cco:hasTargetComponent ?component .
  ?component cco:targetCmptXref ?pdb .
  FILTER(CONTAINS(STR(?pdb), "pdb"))
  ?molecule cco:chemblId ?moleculeid .     
  }