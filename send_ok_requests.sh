#!/usr/bin/env bash

set -euo pipefail

target_endpoint="http://localhost:8080/doc_length"
text="This is a random text. "

for i in `seq 1 1000000`
do
    # define a random longer length text (always under 1000 chars limit)
    N=$(( $RANDOM % 40 + 1 ))
    doctext=$(printf "%${N}s" | sed 's/ /'"$text"'/g')
    shuffled_doctext=$(echo "$doctext" | fold -w1 | shuf | tr -d '\n')

    curl -s -X POST "$target_endpoint" -H "Content-Type: application/json" -d '{"text": "'"$shuffled_doctext"'"}' > /dev/null; done
done
