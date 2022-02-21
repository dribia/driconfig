#!/bin/sh

set -e  # Enable exit on non-zero.
set -x  # Enable command printing.

# Use this script to bump your project's version
# It has the same usage `poetry version` has
# What we do is to commit the change in pyproject.toml right
# after version bumping, and tag the commit when the version
# change is not a patch change.

old_version=$(poetry version -s)
commit_message=$(poetry version "$@")
new_version=$(poetry version -s)

if ! [ "$old_version" = "$new_version" ]
then
  git commit pyproject.toml -m ":bookmark: $commit_message"
  git tag -a "v$new_version" -m ":bookmark: $commit_message"
else
  echo "$1 version update did not change the version number."
fi
