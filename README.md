# tidbyt-birdweather
displaying birdweather data on a tidbyt box

run pull-birdweather-api.py with no arguments and it will prompt for input
to build the config.json file to be used for all future runs.


```python ./pull-birdweather-api.py```


config.json is nothing more than the token for API access
and the station number:

```
{
    "token": "TOKEN_HERE",
    "station": "####"
}
```
