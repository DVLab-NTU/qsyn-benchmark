![stars](https://img.shields.io/github/stars/DVLab-NTU/qsyn-benchmark?style=plastic)
![contributors](https://img.shields.io/github/contributors/DVLab-NTU/qsyn-benchmark?style=plastic)
![release-date](https://img.shields.io/github/release-date-pre/DVLab-NTU/qsyn-benchmark?style=plastic)

# Benchmark Repository for Qsyn: A Developer-Friendly Quantum Circuit Synthesis Framework for NISQ Era and Beyond

### Installation

Clone the repository to your local machine by running

```shell!
git clone https://github.com/DVLab-NTU/qsyn-benchmark.git
cd qsyn-benchmark
git submodule init
git submodule update
```

### Non-basic Gate Decomposition

```shell!
cd utils
bash decompose.sh <Path to Input Circuit Directory> <Path to Decomposed Circuit Directory>
# e.g. bash decompose.sh ../qsyn_publication/original/hwb/ ../qsyn_publication/mapping/hwb
```