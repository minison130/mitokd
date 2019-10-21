#!!/bin/bash

echo "== test tools/data_sampler"
(
  cd ./mitokd/tools/data_sampler/spec
  bash unittest.sh
)
