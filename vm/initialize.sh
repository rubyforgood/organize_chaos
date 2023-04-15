#!/bin/bash -

# Initializes this project in order to be able to run several of its scripts.

# Exit when any command fails
set -e

script_start=$(date +%s)

script_directory=$(dirname "$0")

# Use python3 command if available, otherwise try python
set +e
python_cmd=$(which python3 2> /dev/null)
if [ -n "$python_cmd" ]; then
  python_cmd=python3
else
  python_cmd=$(which python 2> /dev/null)
  if [ -n "$python_cmd" ]; then
    python_cmd=python
  fi
fi

# Assert Python version is 3.7+.
python3_minor_version=$($python_cmd --version | sed -n ';s/Python 3\.\([0-9]*\)\(\.[0-9]*\)*.*/\1/p;')
if ! [[ "$python3_minor_version" -ge '7' ]]; then
  echo "Must have Python 3.7+ installed on path! Found $($python_cmd --version)."
  exit 3
fi
set -e

echo 'Creating a Python virtual environment...'
$python_cmd -m venv .venv
echo 'Done'

./vm/install-dependencies.sh

echo
script_end=$(date +%s)
dur_secs=$((script_end - script_start))
if ((dur_secs > 60)); then
  echo "Finished in $((dur_secs/60)) minutes."
else
  echo "Finished in $dur_secs seconds."
fi
