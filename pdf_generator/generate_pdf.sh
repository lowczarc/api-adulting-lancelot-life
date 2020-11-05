python3 get_bills.py $1 | pandoc --metadata-file=/dev/stdin --template=template/facture_simple.md /dev/null | pandoc -t html --metadata-file template/metadata.yaml --css template/facture.css -o $2

