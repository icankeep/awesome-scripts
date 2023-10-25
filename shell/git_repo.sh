#!/bin/bash

regex_pattern="git@([^:]+):([^/]+)/([^\.]+).git"
remote_name=$1
remote_name=${remote_name:-"origin"}
shift 1

git_url=$(git remote get-url --push $remote_name)

if [[ $git_url =~ $regex_pattern ]]; then
    git_repo_url=https://${BASH_REMATCH[1]}/${BASH_REMATCH[2]}/${BASH_REMATCH[3]}
    echo $git_repo_url
    open $git_repo_url
fi
