rm -rf TaskMatrix && git clone https://github.com/microsoft/TaskMatrix

cd TaskMatrix/

pip install -r requirements.txt
pip install git+https://github.com/IDEA-Research/GroundingDINO.git
pip install git+https://github.com/facebookresearch/segment-anything.git