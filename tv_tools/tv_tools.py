#!/usr/bin/env python3
'''
    tv_tools is a Python command line tool to rename TV episodes from an absolute to an aired order.
        * Rename all TV episodes in a file structure to the S00E00 standard
    ex:
    tv_tools -options:print,noexec -paths:/mnt/media/


    options:
        print       : print more detailed information
        noexec      : dont execute the operations
        doubleep    : if video files contain two episodes each
        keepep      : keep the episode number
        preserve    : Preserve the filename except for a marker (*** by default)
'''

# Normal import
try:
    from tv_tools.library.tools import load_arguments, get_content, replace_ss, add_numbering, replace_absolute, organize_episodes, auto
    from tv_tools.library.appconfig import AppConfig
# Allow local import for development purposes
except ModuleNotFoundError:
    from library.tools import load_arguments, get_content, replace_ss, add_numbering, replace_absolute, organize_episodes, auto
    from library.appconfig import AppConfig

def main():
    ''' Controls the tasks

    Args:

    Returns:
    '''
    arguments = load_arguments()

    config = AppConfig({
        "tmdb": {
            "key":None,
            "token":None
        }
    })

    if arguments["auto"]:
        if len(arguments["paths"]) > 0:
            for path in arguments["paths"]:
                auto(arguments, config, path)

    if arguments["organize"]:
        if len(arguments["paths"]) > 0:
            for path in arguments["paths"]:
                organize_episodes(arguments, path)
                
    if arguments["rename"]:
        if len(arguments["paths"]) > 0:
            for path in arguments["paths"]:
                if "preserve" in arguments["options"]:
                    add_numbering(arguments = arguments, parent_path = path)
                elif "doubleep" not in arguments["options"]:
                    replace_absolute(arguments = arguments, parent_path = path)
                else:
                    replace_absolute(arguments = arguments, parent_path = path, episode_per_file = 2)
    
    if arguments["print_config"]:
        print(config)
                
    if arguments["add_tmdb"]:
        if not arguments["key"]:
            print("Missing -key argument")
        if not arguments["token"]:
            print("Missing -token argument")
        config["tmdb"]["key"] = arguments["key"]
        config["tmdb"]["token"] = arguments["token"]
        config.save_config()


if __name__ == '__main__':
    main()

