# bbdc24-mlbananas

Repository for [Bremen Big Data Challenge (BBDC)](https://bbdc.csl.uni-bremen.de/en/)

### Team Members
- [Sucheth Shenoy](https://github.com/sucheth17)
- [Sofia Lanetskaya](https://github.com/lanetskaya)
- [Harshith Gowda](https://github.com/harshithgowdasm)

---

### Setup Instructions

Clone the repo:
```sh
git clone https://github.com/SuchethShenoy/bbdc24-mlbananas.git
```

Download the task data and extract the folder in the base directory of the repo:
```sh
task
├── bbdc_2024_description.md
├── Data_License_Agreement.txt
├── SessionData-all.csv
├── student_data.csv
└── student_skeleton.csv
```

Create a python virtual environment and install the [required packages](https://github.com/SuchethShenoy/bbdc24-mlbananas/blob/main/requirements.txt) (Only for the first time):
```sh
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Activate the virtual environment (Subsequent times):
```sh
source venv/bin/activate
```

Switch to a branch to work on an issue:
```sh
git checkout <branch_name>
```
