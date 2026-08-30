from nids_datasets import Dataset

# Download CIC-IDS2017 network flows (smallest subset to start)
data = Dataset(dataset='CIC-IDS2017', subset=['Network-Flows'], files='all')
data.download()