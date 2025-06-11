
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