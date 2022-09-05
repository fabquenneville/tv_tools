======
Manual
======

Name
----

tv_tools

Synopsis
--------

.. code-block:: bash

    ./tv_tools.py
        rename,organize
        [-options:print,noact,doubleep,keepep,preserve]
        [-paths:]
        [-marker:]
        [-fseparator:]
        [-eseparator:]


**for multiple paths use double comma separated values ",,"**

default options are:

.. code-block:: bash

    -marker:"***"
    -fseparator:" - "
    -eseparator:" - "

::

    tv_tools rename -options:print,noact -fseparator:"" -eseparator:"" -paths:"path"
    Before:
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

    after:
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

Description
-----------
tv_tools is a Python command line tool to rename TV episodes from an absolute to an aired order.

Commands
--------

rename
======
Use tv_tools to rename the files according to the options.

organize
========
Use tv_tools to organize the episodes from a single folder to a season based organisation.

::

    tv_tools organize -paths:"path"

    Before:
    parent_path
        S01E01.mkv
        S01E02.mkv
        ...
        S02E01.mkv
        S02E02.mkv
        ...

    after:
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

Options
-------

print
=====
Print more detailed information

noact
=====
Prevent actions except printing

doubleep
========
To use if video files contain two episodes each

keepep
======
Keep the episode number and only prepend season numbers

::

    tv_tools rename -fseparator:"" -eseparator:"" -options:keepep -paths:"path"

    Before:
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

    after:
    parent_path
        Season 01
            S01E01.mkv
            S01E02.mkv
            ...
        Season 02
            S02E25.mkv
            S02E26.mkv
            ...
        ...

preserve
========

::

    Preserve the filename except for a marker  that is to be reaplaced by a seasoned episode number

    *** by default

    tv_tools rename -marker:"&&" -fseparator:"" -options:preserve -paths:"path"

    Before:
    parent_path
        Season 01
            &&01.mkv
            &&02.mkv
            ...
        Season 02
            &&25.mkv
            26,mkv
            ...
        ...

    After:
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

marker
======

::

    The marker to replace, default is "***"



fseparator
==========

::

    The front separator, default is " - "
    can be remove with the -fseparator:"" option

    example from "show03.mkv" to "show - S01E03.mkv"

eseparator
==========

::

    The end separator, default is " - "
    can be remove with the -eseparator:"" option

    example from "03The.show.mkv" to "S01E03 - The.show.mkv"


Examples
--------


See Also
--------


Author
------

Fabrice Quenneville
