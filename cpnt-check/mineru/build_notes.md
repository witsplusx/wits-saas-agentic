https://blog.csdn.net/weixin_44550842/article/details/148007550

在 AutoDL上部署

conda create --prefix=/root/autodl-tmp/condars/envs/mineru python=3.11 -y
conda activate /root/autodl-tmp/condars/envs/mineru

pip install -U magic-pdf[full] --extra-index-url https://wheels.myhloli.com -i https://pypi.tuna.tsinghua.edu.cn/simple
magic-pdf --version

# 当前版本：1.3.11

pip install modelscope
curl -o download_models.py https://gcore.jsdelivr.net/gh/opendatalab/MinerU@master/scripts/download_models.py
python download_models.py

pip install paddlepaddle-gpu==2.6.1

magic-pdf -p 01.pdf -o ./output

scp -P 43486 D:/WITS-PROJS/wits-saas-agentic/wits-saas-agentic/examples/data-convs/01.pdf root@connect.bjc1.seetacloud.com:~/autodl-tmp/wits-projs/mineru

ssh -p 43486 root@connect.bjc1.seetacloud.com

文件拷贝
 scp -P 43486 D:/WITS-PROJS/wits-saas-agentic/wits-saas-agentic/examples/data-convs/01.pdf root@connect.bjc1.seetacloud.com:~/autodl-tmp/wits-projs/mineru

  scp -P 43486 D:/WITS-PROJS/wits-saas-agentic/wits-saas-agentic/examples/data-convs/002.pdf root@connect.bjc1.seetacloud.com:~/autodl-tmp/wits-projs/mineru

  scp -P 43486 D:/WITS-PROJS/wits-saas-agentic/wits-saas-agentic/examples/data-convs/003.pdf root@connect.bjc1.seetacloud.com:~/autodl-tmp/wits-projs/mineru

scp -P 43486 -r root@connect.bjc1.seetacloud.com:~/autodl-tmp/wits-projs/mineru/output D:/WITS-PROJS/wits-saas-agentic/wits-saas-agentic/examples/output01

scp -P 43486 -r root@connect.bjc1.seetacloud.com:~/autodl-tmp/wits-projs/mineru/output D:/WITS-PROJS/wits-saas-agentic/wits-saas-agentic/examples/output01

scp -P 43486 -r root@connect.bjc1.seetacloud.com:~/autodl-tmp/wits-projs/mineru/output3 D:/WITS-PROJS/wits-saas-agentic/wits-saas-agentic/examples/

scp -P 43486 -r root@connect.bjc1.seetacloud.com:~/autodl-tmp/wits-projs/mineru/output4 D:/WITS-PROJS/wits-saas-agentic/wits-saas-agentic/examples/

2025年6月

pip install MarkupSafe

pip install -U "mineru[core]"

pip install -U "mineru[all]"

重新开一个  env

conda create -n wits-saas-mineru python=3.11 -y
conda activate wits-saas-mineru

docker run --gpus all  --shm-size 32g  -p 30000:30000  --ipc=host  mineru-sglang:latest  mineru-sglang-server --host 0.0.0.0 --port 30000

mineru-models-download

mineru -p ./cpnt-check/mineru/files/002.pdf -o ./cpnt-check/mineru/files/output002 --source local -d cuda -l ch

mineru -p ./cpnt-check/mineru/files/002.pdf -o ./cpnt-check/mineru/files/output002 --source modelscope -b vlm-transformers -l ch -d cuda:0

mineru -p shencha.pdf -o result --source modelscope -b vlm-transformers

pip install sglang[all]==0.4.7

mineru -p ./cpnt-check/mineru/files/002.pdf -o ./cpnt-check/mineru/files/output002 --source local -b vlm-sglang-engine

mineru -p ./cpnt-check/mineru/files/平凡的世界.pdf -o ./cpnt-check/mineru/files/output003 --source local -b vlm-transformers -l ch -d cuda:0
