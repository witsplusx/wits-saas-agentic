#readme

docker compose -f docker/docker-compose-dataplat.yaml -p witsmt-dk-dataplat up -d

docker compose -f docker/docker-compose-agents.yaml -p witsmt-dk-agents up -d

docker compose -f docker/docker-compose-flow.yaml -p witsmt-dk-flow up -d

deepseek api key:
sk-846fd2681908413e94cfa79bd98b3673

docker compose -f docker/maxun/docker-compose.yml -p witsmt-maxun up -d

docker compose -f docker/wiseflow/docker-compose.yml -p witsmt-wiseflow up -d

docker compose -f docker/KAG/docker-compose.yml -p witsmt-kag up -d

docker compose -f docker/milvus/milvus-standalone-docker-compose.yml -p witsmt-milvus up -d



添加本地IP访问
--add-host host.docker.internal:host-gateway

docker run -p 50080:80 -v D:/WITS-PROJS/rundatas/agent-zero:/a0 -itd frdel/agent-zero-run

docker run
-e GRADIO_SERVER_NAME=0.0.0.0
-e GRADIO_SERVER_PORT=7860
-v ./ktem_app_data:/app/ktem_app_data
-p 7860:7860 -it --rm
ghcr.io/cinnamon/kotaemon:main-full

docker run --name=kotaemon -e GRADIO_SERVER_NAME=0.0.0.0 -e GRADIO_SERVER_PORT=7860 -v D:/WITSMT-PROJS/rundatas/ktem_app_data:/app/ktem_app_data --add-host host.docker.internal:host-gateway -p 7860:7860 -itd ghcr.io/cinnamon/kotaemon:main-ollama

docker run -itd --name higress-allinone -p 8201:8001 -p 8280:8080 -p 8243:8443  higress-registry.cn-hangzhou.cr.aliyuncs.com/higress/all-in-one:latest
