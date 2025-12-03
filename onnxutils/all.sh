find /fastdata2/data/onnxfiles/models/validated/ -name "*.onnx" | while read file; do
  filename=$(basename "$file")
  filen="${filename%.*}"
  #echo $filen
  python onnxextract.py compute_graph_extraction "$file" "${filen}.json" --savePath /fastdata2/data/onnxconverted2
done
