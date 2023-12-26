set -e
set -o pipefail

if [ $# -eq 0 ]
then
  echo "No arguments supplied"
  exit 1
fi
if [ -z "$1" ]
then
  echo "No pretrained model directory provided"
  exit 1
fi
pt_models_dir=$1

if [ -z "$2" ]
then
  echo "No pretrained model name provided"
  exit 1
fi
pt_model_name=$2

if [ -z "$3" ]
then
  pt_download_link="http://download.tensorflow.org/models/object_detection/tf2/20200711/$pt_model_name.tar.gz"
else
  pt_download_link=$3
fi
if [ ! -d "$pt_models_dir" ]
then
  mkdir -p "$pt_models_dir"
fi
cd "$pt_models_dir" || exit 1
wget "$pt_download_link" -O "$pt_model_name.tar.gz" || exit 1
tar -zxvf "$pt_model_name.tar.gz" || exit 1
rm "$pt_model_name.tar.gz"