python3 ${PDF_GENERATOR}/get_bills.py $1 | pandoc --metadata-file=/dev/stdin --template=${PDF_GENERATOR}/template/facture_simple.md /dev/null | pandoc -t html --metadata-file ${PDF_GENERATOR}/template/metadata.yaml --css ${PDF_GENERATOR}/template/facture.css -o $2

