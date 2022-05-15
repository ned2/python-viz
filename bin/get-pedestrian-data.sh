#!/usr/bin/env bash

# Download latest Pedestrian traffic datasets and then prep for use in Dashboard

set -e

# directory of this script
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# directory to download data into
DATA_DIR=${SCRIPT_DIR}/../data

# https://data.melbourne.vic.gov.au/Transport/Pedestrian-Counting-System-2009-to-Present-counts-/b2ak-trbp
COUNT_DATASET_ID=b2ak-trbp

# https://data.melbourne.vic.gov.au/Transport/Pedestrian-Counting-System-Sensor-Locations/h57g-5234
SENSOR_DATASET_ID=h57g-5234


download_dataset () {
    wget --content-disposition --backups=1 --directory-prefix=${DATA_DIR} \
         https://data.melbourne.vic.gov.au/api/views/${1}/rows.csv?accessType=DOWNLOAD

}

download_dataset ${COUNT_DATASET_ID}
download_dataset ${SENSOR_DATASET_ID}
