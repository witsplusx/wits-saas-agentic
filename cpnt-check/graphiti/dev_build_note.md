https://python.langchain.ac.cn/docs/integrations/graphs/falkordb/

https://www.falkordb.com/

docker run -p 6779:6379 -p 3000:3000 -it -d --name falkordb falkordb/falkordb:edge

docker run -p 6779:6379 -p 3000:3000 -it -d --name falkordb falkordb/falkordb:latest

http://localhost:3000/graph

pip install graphrag_sdk

pip install falkordb-bulk-loader

https://docs.falkordb.com/llm_integrations.html

pip install graphiti-core

pip install graphiti-core[falkord-db]

docker run -d -p 7070:7070 -p 7687:7687 -p 9090:9090 --name tugraph tugraph/tugraph-runtime-centos7

admin 73@TuGraph

教程

https://help.getzep.com/graphiti/getting-started/quick-start

docker run
--name neo4j-enterprise
-p 7474:7474 -p 7687:7687
-e NEO4J_AUTH=neo4j/your_password
-e NEO4J_PLUGINS='["apoc"]'
-e NEO4J_ACCEPT_LICENSE_AGREEMENT=yes
neo4j:5.26-enterprise

docker run -d --name neo4j-enterprise -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/witsmt2025  -e NEO4J_PLUGINS='["apoc"]'  -e NEO4J_ACCEPT_LICENSE_AGREEMENT=yes neo4j:5.26-enterprise

pip install -U FalkorDB
