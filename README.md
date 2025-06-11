Download graph data from neo4j database in tsv file format
```
kgx neo4j-download --uri bolt://localhost:7687
                   --username neo4j --password admin
                   --output neo_graph_download/
                   --output-format tsv
```

validate step
```
python  validate_kg.py
```
