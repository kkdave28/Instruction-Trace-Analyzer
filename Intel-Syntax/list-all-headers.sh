#! /usr/bin/zsh

list_all_dirs () {
    for dir in $1/*; do
        if [[ -d "$dir" ]]; then
            list_all_dirs "$dir"
        else
            echo "skip file $dir" >> all_headers
        fi
    done    
}
list_all_dirs "/usr/lib/gcc/x86_64-linux-gnu/9/include"
list_all_dirs "/usr/include"
list_all_dirs "/usr/lib/gcc/x86_64-linux-gnu/9/../../../../x86_64-linux-gnu/include"
list_all_dirs "/usr/lib/gcc/x86_64-linux-gnu/9/include-fixed"

