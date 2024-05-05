INPUT_ROOT=$1
OUTPUT_ROOT=$2
mkdir -p $OUTPUT_ROOT
for file in $INPUT_ROOT/*.qasm; do
    echo "Decomposing $file"
    python3 decompose.py --file $file --output-root ${OUTPUT_ROOT}
done