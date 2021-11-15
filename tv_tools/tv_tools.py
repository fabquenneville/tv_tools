#!/usr/bin/env python3
'''
    tv_tools is a Python command line tool to rename TV episodes from an absolute to an aired order.
        * Rename all TV episodes in a file structure to the S00E00 standard
    ex:
    tv_tools -options:print,noact -paths:/mnt/media/


    options:
        print       : print more detailed information
        noact       : dont act
        doubleep    : if video files contain two episodes each
        keepep      : keep the episode number
        preserve    : Preserve the filename except for a marker (*** by default)
'''

# TODO functions commands to be revised
import os
import shutil

# Normal import
try:
    from tv_tools.library.tools import load_arguments, get_content, replace_ss, add_numbering, replace_absolute, organize_episodes
# Allow local import for development purposes
except ModuleNotFoundError:
    from library.tools import load_arguments, get_content, replace_ss, add_numbering, replace_absolute, organize_episodes

def main():
    ''' Controls the tasks

    Args:

    Returns:
    '''
    arguments = load_arguments()

    if arguments["organize"]:
        if len(arguments["paths"]) > 0:
            for path in arguments["paths"]:
                organize_episodes(path)
                
    if arguments["rename"]:
        if len(arguments["paths"]) > 0:
            for path in arguments["paths"]:
                if "preserve" in arguments["options"]:
                    add_numbering(arguments = arguments, parent_path = path)
                elif "doubleep" not in arguments["options"]:
                    replace_absolute(arguments = arguments, parent_path = path)
                else:
                    replace_absolute(arguments = arguments, parent_path = path, episode_per_file = 2)
                

if __name__ == '__main__':
    main()

