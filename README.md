# README #
Just a small script for my daily use.  
It can rename the subtitle file using the video file name.  
It uses regular expression.  
`rename.py` with python 2.x.  
`ui.py` with python 3.x.  

## Usage ##
### rename.py ###
1. If no config.ini exists, use `python rename.py` to create it.  
2. Fill the config.ini.  
3. Execute `python rename.py` to rename.  
More details may be found in config.ini.  

### ui.py ###
Just execute `python3 ui.py`.  

1. Fill the blank entry  
2. Click button __Src match__, to list the matched video files.  
3. Click button __Dst match__, to list the matched subtitle files.  
4. Click button __List Todo__, to list the rename actions to do.  
5. Click button __Run__, to do the rename actions.  

### options ###
* `src pattern`: match the video files. Use the group name `(?P<name>)` to specify the subtitle's name  
* `dst pattern`: match the subtitle files. Use the group name`(?P<ext>)` to specify the subtitle's ext  
* `src key pattern`: the regex pattern for key in video's filename. Use the group name`(?P<key>)` to specify the key  
* `dst key pattern`: the regex pattern for key in subtitle's filename. Use the group name`(?P<key>)` to specify the key  
* `key collect`: the match key collect. You can use multiple keys as one key for match  

For example,  
```
src pattern: (?P<name>.+)\.(mp4|mkv|avi)
dst pattern: .+chs(?P<ext>\.(ass|ssa|srt))
key collect: key1,key2,suffix
src key pattern: (?P<key1>\d{2})xxx(?P<key2>\w+)-(?P<suffix>\w+)
dst key pattern: (?P<key1>\d{2})---(?P<suffix>\w+)xxx(?P<key2>\w+)
```




