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

install_path=$1

if [ -d "$install_path" ]
then
  echo "object_detection folder exists, no need to clone again"
  # no exit 0 here, because we might not have
  # changed the folder structure yet
else
  git clone https://github.com/tensorflow/models "$install_path"
fi

if [[ ! -d "$install_path/research" ]] || [[ -d "$install_path/help" ]]
then
  msg1="Most likely Tensorflow Object detection folders are already structured."
  msg2="If not, please check the folder where TFOD API should be installed for errors"
  echo "$msg1 $msg2"
else
  for filename in $(ls -A "$install_path")
  do
    if [ "research" != "$filename" ]
    then
      rm -Rf "${install_path:?}/$filename"
    fi
  done

  mv "$install_path/research/object_detection" "$install_path/object_detection"
  mv "$install_path/research/slim" "$install_path/slim"
  rm -Rf "${install_path:?}/research"
  mkdir "${install_path:?}/help"
fi

apt-get install protobuf-compiler

cd "$install_path" || exit 1;
protoc object_detection/protos/*.proto --python_out=.
cp object_detection/packages/tf2/setup.py .
python -m pip install .
pip install datasetinsights