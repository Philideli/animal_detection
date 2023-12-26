set -e
set -o pipefail

if [ $# -eq 0 ]
then
  echo "No arguments supplied"
  exit 1
fi
if [ -z "$1" ]
then
  echo "No install path supplied"
  exit 1
fi

python "$1/object_detection/builders/model_builder_tf2_test.py"