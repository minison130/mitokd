# downsampling dataset

## (0) Environments
Need python 3.7 with packeges installed as follows,
```
pip install easydict
```

## (1) Make sampled json
Run, 
```
ptyhon down_sampler.py [-h] --root_dir ROOT_DIR --output_json OUTPUT_JSON
                       [--max_rate MAX_RATE] [--target_ext TARGET_EXT]
```
* ```ROOT_DIR```: dataset direcory
* ```OUTPUT_JSON```: output path of sampled json
* ```MAX_RATE```: allow up to ($MAXRATE * $MIN_NUM_DATA) with downsampling 
* ```TARGET_EXT```: extention of the data

Format of output json is,
```
{
    "root"       (str): path to root directory
    "target_ext" (str): target extention(ex. '.png', '.txt')
    "contents": [
        {
            "dirname" (str): name of directory of data class
            "files"   (list): names of sampled data 
        },...
    ]
}
```

## (2) Make new directory
Run,
```
python make_new_dataset.py [-h] --input_json INPUT_JSON --target_root
                           TARGET_ROOT

```
* ```INPUT_JSON```: path to json generated in (1)
* ```TARGET_ROOT```: path to new directory 
