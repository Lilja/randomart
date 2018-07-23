#!/bin/bash

yaml=".env.yaml"

read -r -d '' yaml_content <<'EOF'
keys:
  - api-key-here
filename: img.png
dimensions: 1920x1080
EOF


if [ ! -f "$yaml" ]; then
    echo "$yaml_content" >> "$yaml"
fi
