#!/bin/bash

for file in $(git status -s | awk '{print $2}' | grep '\.go$'); do
  echo "$file"
  # 删除所有 import 声明中的空行
  gsed -i '/import (/, /)$/{/^$/d}' "$file"
  # 执行 goimports
  goimports -w "$file"
done
