
conda create -n wits-saas-agentic python=3.11 -y
conda activate wits-saas-agentic


pip install 'markitdown[all]'

markitdown --list-plugins

markitdown 01.pdf -o 01.md 

Markify：专为 LLM 优化的开源文档解析神器，轻松破解 PDF 难题！融合MinerU与Markitdown！

docker run -itd --name=markify  -p 20926:20926 -p 8501:8501 docker.io/kylinmountain/markify:0.0.1
streamlit run ./client/streamlit_client.py


