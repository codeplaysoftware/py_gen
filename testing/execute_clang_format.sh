#
#    Copyright (C) Codeplay Software Limited. All Rights Reserved.
#
# $1 - The file to format
# 

format_binary=clang-format
file=$1

exec ${format_binary} -style=file -i ${file}