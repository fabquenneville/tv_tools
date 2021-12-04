#!/usr/bin/env python3
'''
    These are various tools used by mediacurator
'''

import os
import shutil
import sys
import re
import json

from tmdbv3api import TMDb, TV, Season
from tmdbv3api.exceptions import TMDbException

def load_arguments():
    ''' Get/load command parameters

    Args:

    Returns:
        Dictionary (arguments): The command parameters passed by the users
    '''

    arguments = {
        "auto":False,
        "rename":False,
        "organize":False,
        "add_tmdb":False,
        "print_config":False,
        "key":None,
        "token":None,
        "options":list(),
        "paths":list(),
        "marker":"***",
        "fseparator":" - ",
        "eseparator":" - ",
    }

    if len(sys.argv) >= 2:
        arguments["action"] = sys.argv[1]

    for arg in sys.argv:
        if arg in ["auto", "rename", "organize", "add_tmdb", "print_config"]:
            arguments[arg] = True
        for paramhead in ["-key:", "-token:", "-marker:", "-fseparator:", "-eseparator:"]:
            if paramhead in arg:
                arguments[arg[1:len(paramhead) - 1]] = arg[len(paramhead):]
        for paramhead in ["-options:"]:
            if paramhead in arg:
                arguments[arg[1:len(paramhead) - 1]] += arg[len(paramhead):].split(",")
        for paramhead in ["-paths:"]:
            if paramhead in arg:
                arguments[arg[1:len(paramhead) - 1]] += arg[len(paramhead):].split(",,")

    return arguments

def get_content(parent_path, directories = False):
    ''' get the list of the content in a filepath

    Args:
        parent_path: the parent path to work on
        directories = False: If true only directories will be returned

    Returns:
        folderlist: Operations success
    '''
    if directories:
        folderlist = [ name for name in os.listdir(parent_path) if os.path.isdir(os.path.join(parent_path, name)) ]
    else:
        folderlist = os.listdir(parent_path)
    
    folderlist.sort()
    return folderlist

def replace_ss(parent_path, old = " ", new = "_"):
    ''' Replaces a specific substring trough a filetree

    Args:
        parent_path: the parent path to work on
        old: the substring to replace
        new: the new substring

    Returns:
        Bool: Operations success
    '''
    positive = False
    folderlist = get_content(parent_path)
    for n in range(len(folderlist)):
        # dont act on hidden folders/files
        if "." != folderlist[n][0]:
            newname = folderlist[n].replace(old, new, 1)
            os.rename(parent_path + folderlist[n],parent_path + newname)
            folderlist[n] = newname
            positive = True
    return positive

def add_numbering(arguments, parent_path, episode_per_file = 1):
    ''' This function will replace a marker (*** by default) by a searialized and delimited episode number while preserving the rest of the naming

    Example: calling add_numbering(arguments, parent_path) would result in:
        from:
        parent_path
            Season 01
                ***01.mkv
                ***02.mkv
                ...
            Season 02
                ***25.mkv
                26,mkv
                ...
            ...

        to:
        parent_path
            Season 01
                S01E01 - 01.mkv
                S01E02 - 02.mkv
                ...
            Season 02
                S02E01 - 25.mkv
                26,mkv
                ...
            ...

    Args:
        arguments: the options selected by the user
        parent_path: the parent path to work on
        episode_per_file: the number of episodes per file

    Returns:
        bool: Returns a positive if there was at least a match
    '''
    positive = False
    folderlist = get_content(parent_path, directories = True)
    for n in range(len(folderlist)):
        if len(re.findall('\d+', folderlist[n] )) <= 0:
            continue
        season_nb = re.findall('\d+', folderlist[n] )[0]
        episode_itt = 0
        part_itt = 0
        filelist = get_content(parent_path + folderlist[n])

        # get rid of non numbered files
        filelist = [item for item in filelist if len(re.findall('\d+', item))>0]
        
        # order the list by the fist number found in the name
        filelist.sort(key=lambda line: int(re.findall('\d+', line )[0]))
        numbers = [re.findall('\d+', line )[0] for line in filelist]
        lastnum = -1
        lastpart = 0
        for m in range(len(filelist)):
            # Get the first number in the filename  see its link to other files
            oldepnum = re.findall('\d+', filelist[m] )[0]
            newepnum = ""
            # If it is not the same episode number as the last file we start a new episode and reset the parts and start working
            if oldepnum != lastnum:
                episode_itt += 1
                part_itt = 0
            lastnum = oldepnum
            
            # Find and prepare the zeros before the actual season, episode and part numbers
            seasonzero = ""
            zero = ""
            partzero = ""

            # Select number of zeros in season number
            if int(season_nb) < 10 and season_nb[0] != "0":
                seasonzero = "0"

            # Select number of zeros in episode number
            if len(filelist) >= 100 and episode_itt < 10:
                zero = "00"
            elif len(filelist) >= 100 and episode_itt < 100:
                zero = "0"
            elif episode_itt < 10:
                zero = "0"

            # If there is more that one part to the episode use the multi-part filename template
            if len([i for i in numbers if i == oldepnum]) > 1:
                part_itt += 1
                
                # Select number of zeros in part number
                if part_itt < 10:
                    partzero = "0"
                
                newepnum += f'{arguments["fseparator"]}S{seasonzero}{season_nb}E{zero}{episode_itt} Part {partzero}{part_itt}{arguments["eseparator"]}'
            else:
                part_itt = 0
                newepnum += f'{arguments["fseparator"]}S{seasonzero}{season_nb}E{zero}{episode_itt}{arguments["eseparator"]}'

            # Print and/or act on the selected changes
            newname = filelist[m].replace(arguments["marker"], newepnum, 1)
            if "print" in arguments["options"]:
                print(f"{folderlist[n]:<25}/{filelist[m]:<50} -> {folderlist[n]:<25}/{newname:<50}")
            if not "noexec" in arguments["options"]:
                os.rename(f"{parent_path}{folderlist[n]}/{filelist[m]}",f"{parent_path}{folderlist[n]}/{newname}")
            positive = True
    return positive

def replace_absolute(arguments, parent_path, episode_per_file = 1):
    ''' Changes filenames from an absolute to season based names:

    Example:
        from:
        parent_path
            Season 01
                01.mkv
                02.mkv
                ...
            Season 02
                25.mkv
                26,mkv
                ...
            ...

        to:
        parent_path
            Season 01
                S01E01.mkv
                S01E02.mkv
                ...
            Season 02
                S02E01.mkv
                S02E02.mkv
                ...
            ...

    Args:
        arguments: the options selected by the user
        parent_path: the parent path to work on
        episode_per_file: the number of episodes per file

    Returns:
        bool: Returns a positive if there was at least a match
    '''
    positive = False
    folderlist = get_content(parent_path, directories = True)
    for n in range(len(folderlist)):
        if len(re.findall('\d+', folderlist[n] )) <= 0:
            continue
        season_nb = re.findall('\d+', folderlist[n] )[0]
        episode_itt = 0
        filelist = get_content(parent_path + folderlist[n])

        # get rid of non numbered files
        filelist = [item for item in filelist if len(re.findall('\d+', item))>0]
        
        # order the list by the fist number found in the name
        filelist.sort(key=lambda item: int(re.findall('\d+', item )[0]))

        for m in range(len(filelist)):
            oldepnum = re.findall('\d+', filelist[m] )[0]
            newepnum = ""
            for i in range(episode_per_file):
                episode_itt += 1

                season_zeros, episode_zeros = get_zeros(
                    nb_season_items = len(filelist), # POSSIBLY BROKEN TODO
                    season_nb = season_nb,
                    episode_number = episode_itt
                )
                
                # If selected replace the episode number
                if "keepep" in arguments["options"]:
                    newepnum += f'{arguments["fseparator"]}S{season_zeros}{season_nb}E{oldepnum}'
                else:
                    newepnum += f'{arguments["fseparator"]}S{season_zeros}{season_nb}E{episode_zeros}{episode_itt}'
                if i < episode_per_file:
                    newepnum += arguments["eseparator"]
                newname = filelist[m].replace(oldepnum, newepnum, 1)
                positive = True
            if "print" in arguments["options"]:
                print(f"{folderlist[n]:<25}/{filelist[m]:<45} -> {folderlist[n]:<25}/{newname:<45}")
            if not "noexec" in arguments["options"]:
                os.rename(f"{parent_path}{folderlist[n]}/{filelist[m]}",f"{parent_path}{folderlist[n]}/{newname}")
    return positive

def replace_epiname_style_absolute(arguments, config, path, style_to = "standard"):
    regex_from = re.compile(get_regexes("absolute"))
    show_match = re.search(get_regexes("show_name"), os.path.basename(os.path.normpath(path)))
    if not show_match:
        return False
    show_name = show_match.group(1)
    show_year = show_match.group(2)
    
    # Getting TMDB data
    show_tmdb = get_tmdb_show(config, show_name, show_year)
    if not show_tmdb:
        return False

    # Getting items
    directories = []
    files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        directories.extend(dirnames)
        files.extend(filenames)
        break
    files = sorted(files, key=lambda x: get_filenumber(x))

    season_ep_nb = {}
    # Extracting the number of episodes
    for season_nb, season_data in show_tmdb["seasons"].items():
        season_ep_nb[season_nb] = len(season_data['episodes'])
    season_ep_nb[0] = len([file for file in files if re.search(regex_from, file) and int(re.search(regex_from, file).group(1)) < 1])

    current_season_nb = 0
    current_episode_nb = 1
    for file in files:
        # Removing file extension
        filename = str(os.path.splitext(file)[0])

        current_nb_match = re.search(regex_from, filename)
        if not current_nb_match:
            continue
        replaced = current_nb_match[1]
        replacing = ""
        current_nb = int(replaced)

        if current_episode_nb > season_ep_nb[current_season_nb]:
            current_season_nb += 1
            current_episode_nb = 1
        
        season_zeros, episode_zeros = get_zeros(
            nb_season_items = season_ep_nb[current_season_nb],
            season_nb = current_season_nb,
            episode_number = current_episode_nb
        )
        replacing = f'S{season_zeros}{current_season_nb}E{episode_zeros}{current_episode_nb}'

        newname = filename.replace(replaced, replacing)
        # Adding back extension
        newname += str(os.path.splitext(file)[1])
        
        if "print" in arguments["options"]:
            print(f"{file:<45} -> {newname:<45}")
            
        if not "noexec" in arguments["options"]:
            os.rename(os.path.join(path, file), os.path.join(path, newname))
        
        current_episode_nb += 1
    

def replace_epiname_style(arguments, config, path, style_from, style_to = "standard"):
    if style_from == "absolute":
        return replace_epiname_style_absolute(arguments, config, path, style_to = "standard")
    regex_from = re.compile(get_regexes(style_from))
    directories = []
    files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        directories.extend(dirnames)
        files.extend(filenames)
        break
    
    for file in files:
        # Removing file extension
        filename = str(os.path.splitext(file)[0])
        match = regex_from.search(filename)
        if not match:
            continue
        
        replaced = match[0]
        replacing = ""
        season_nb = None
        episode_nb = None
        nb_season_items = 0
        if style_from in ["standard_minuscule", "xseparated"]:
            season_nb = int(match[1])
            episode_nb = int(match[2])
            nb_season_items = len([episode for episode in files if regex_from.search(episode) and int(regex_from.search(episode)[1]) == season_nb])
        elif style_from == "flat":
            if len(replaced) > 2 and len(replaced) <= 4:
                season_nb = int(replaced[:-2])
                episode_nb = int(replaced[-2:])
                for episode in files:
                    # Removing file extension
                    episode = str(os.path.splitext(episode)[0])
                    if regex_from.search(episode) and int(regex_from.search(episode)[0][:-2]) == season_nb:
                        nb_season_items += 1
        
        season_zeros, episode_zeros = get_zeros(
            nb_season_items = nb_season_items,
            season_nb = season_nb,
            episode_number = episode_nb
        )
        replacing = f'S{season_zeros}{season_nb}E{episode_zeros}{episode_nb}'
        newname = filename.replace(replaced, replacing)
        # Adding back extension
        newname += str(os.path.splitext(file)[1])
        
        if "print" in arguments["options"]:
            print(f"{file:<45} -> {newname:<45}")
            
        if not "noexec" in arguments["options"]:
            os.rename(os.path.join(path, file), os.path.join(path, newname))
         
def auto(arguments, config, path):
    flat = False
    directories = []
    files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        directories.extend(dirnames)
        files.extend(filenames)
        break
    if len(directories) == 0:
        flat = True
    else:
        match = False
        for directory in directories:
            regex = get_regexes("season_folder")
            if re.search(regex, directory):
                match = True
        if not match:
            flat = True
        
    
    if flat:
        original_epiname_style = get_epiname_style(files)
        if original_epiname_style in ["standard_minuscule", "xseparated", "flat", "absolute"]:
            replace_epiname_style(arguments, config, path, original_epiname_style)
            
        organize_episodes(arguments, path)
    else:
        print(f"Not Flat")

def get_zeros(nb_season_items, season_nb, episode_number):

    # Select number of zeros in season number
    season_zeros = ""
    episode_zeros = ""
    if not isinstance(nb_season_items, int):
        nb_season_items = int(nb_season_items)
    if not isinstance(season_nb, int):
        season_nb = int(season_nb)
    if not isinstance(episode_number, int):
        episode_number = int(episode_number)
    
    if season_nb < 10:
        season_zeros = "0"
    if nb_season_items >= 100 and episode_number < 10:
        episode_zeros = "00"
    elif nb_season_items >= 100 and episode_number < 100:
        episode_zeros = "0"
    elif episode_number < 10:
        episode_zeros = "0"
    return season_zeros, episode_zeros
    
def get_epiname_style(files):
    original_epiname_style = None
    regexes = get_regexes("epinames_dict")
    for file in files:
        for epiname_style, regex in regexes.items():
            regex = re.compile(regex)
            if regex.search(file):
                original_epiname_style = epiname_style
                if original_epiname_style == "flat":
                    first_number = get_first_number(files)
                    if first_number <= 1:
                        original_epiname_style = "absolute"
                break
        if original_epiname_style:
            break
    return original_epiname_style

def get_filenumber(file):
    # Removing file extension
    filename = str(os.path.splitext(file)[0])
    regex = re.compile(get_regexes("absolute"))
    match = regex.search(filename)
    if not match:
        return False
    return int(match[0])

def get_first_number(files):
    files = sorted(files, key=lambda x: get_filenumber(x))
    regex = re.compile(get_regexes("absolute"))
    for file in files:
        # Removing file extension
        file = str(os.path.splitext(file)[0])
        if regex.search(file):
            return int(regex.search(file)[0])
    return False


def get_regexes(filter = "epinames_dict"):
    epinames = {
        "standard":r"S([0-9]{2,3})E([0-9]{2,3})",
        "standard_nozero":r"S([0-9]{1,3})E([0-9]{1,3})",
        "standard_minuscule":r"s([0-9]{2,3})e([0-9]{2,3})",
        "xseparated":r"([0-9]{1,3})x([0-9]{1,3})",
        "flat":r"([1-9][0-9]+)",
        "absolute":r"([0-9]+)",
    }
    if filter == "show_name":
        # Some time (1990)
        return r"^(.+) \(([0-9]{4})\)$"
    if filter == "season_folder":
        # s01/S01|Season 01/season_01
        return r"([Ss]([0-9]{1,3}))|([Ss][Ee][Aa][Ss][Oo][Nn][ \_\-.]*([0-9]{1,3}))"
    for epiname_style, regex in epinames.items():
        if filter == epiname_style:
            return regex
    return epinames

def organize_episodes(arguments, path):
    directories = []
    files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        directories.extend(dirnames)
        files.extend(filenames)
        break
    
    season_number = 0
    run = True
    while run:
        season_formated_number = str(season_number).zfill(2)
        if season_number > 99:
            season_formated_number = str(season_number).zfill(3)
        folder_name = f"Season {season_formated_number}"
        if season_number == 0:
            folder_name = "Specials"
        season_substring = f"S{season_formated_number}" # TODO Handle different naming styles

        skip = False
        run = False
        for file in files:
            if season_substring in file:
                episodes_found = True
                run = True
                break
            elif season_number == 0:
                skip = True
                break
        if skip:
            continue
        if not run:
            break

        if folder_name not in directories:
            fpath = os.path.join(path, folder_name)
            
            if "print" in arguments["options"]:
                print(f"Created directory: {fpath}")

            if not "noexec" in arguments["options"]:
                os.mkdir(fpath)
            
            directories.append(folder_name)

        episodes_moved = 0
        for filename in files:
            if season_substring in filename:
                if not "noexec" in arguments["options"]:
                    shutil.move(os.path.join(path, filename), os.path.join(path, folder_name, filename))
                episodes_moved += 1
        if "print" in arguments["options"]:
            print(f"Moved {episodes_moved} episodes for season {season_number}")
        season_number += 1

def get_tmdb_show(config, name, year):
    if not config["tmdb"]["key"]:
        return False

    # TMDB Objects
    tmdb = TMDb()
    tmdb.api_key = config["tmdb"]["key"]
    tv = TV()
    season = Season()

    # TMDB Show data
    show = None
    # Finding the show
    for result in tv.search(name):
        if name.lower() == result['name'].lower() and year == result['first_air_date'][:4]:
            show = result
    if not show:
        return False
    show["seasons"] = {}
    # Finding the seasons
    for i in range(1, 100):
        try:
            show_season = season.details(show["id"], i)
            show["seasons"][i] = show_season
        except TMDbException:
            break
    if len(show["seasons"]) <= 0:
        return False
    return show
