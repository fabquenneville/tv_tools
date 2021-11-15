# tv_tools
tv_tools is a Python command line tool to rename TV episodes from an absolute to an aired order.

The source can be found on the [Github](https://github.com/fabquenneville/tv_tools).

## Documentation
The documentation can be found on the [Github page](https://fabquenneville.github.io/tv_tools/).

## Releases
Instalation instructions are found on the [Github page](https://fabquenneville.github.io/tv_tools/usage/installation.html).

## Usage

commands:

* rename: Rename files as per options.
* organize: Organize tv episodes per season.

options:

* print: Print more detailed information.
* noact: Dont act.
* doubleep: If video files contain two episodes each.
* keepep: Keep the episode number.

```
tv_tools rename -options:print,noact -paths:/mnt/media/
tv_tools organize -paths:/mnt/media/
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
The bug tracker can be found on the [Github page](https://github.com/fabquenneville/tv_tools/issues).

Please make sure to update tests as appropriate.

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)