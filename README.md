# Prerequesites

Python 3

# Installation

1. Create a virtual environment
```bash
python3 -m venv env
```

2. Activate the virtual environment
```bash
source env/bin/activate
```

3. Install dependencies
```bash
pip3 install -r requirements.txt
```

# Running the CLI

Traverse graph

```bash
python3 cli.py traverse <start-node> <graph-file>
```

Run MTR

```bash
python3 cli.py mtr <dest-node>