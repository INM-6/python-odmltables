# -*- coding: utf-8 -*-
"""
pages
=====

Classes to create dialog pages for the wizard interface of python-odmltables.

Classes
-------

WelcomePage        - Class generating the first dialog page, where the user has
                     to decide which odmltable operation he/she wants to
                     perform

LoadodMLPage       - Class generating a dialog page, where the user has to
                     specify the odML file he/she wants to transform into a
                     table and define the corresponding table format

LoadTablePage      - Class generating a dialog page, where the user has to
                     specify the table file he/she wants to transform into an
                     odML file and state if the item names of the table header
                     were modified

HeaderOrderPage    - Class generating a dialog page, where the user has to
                     choose which table header items should be used, can change
                     in which order the table header items are displayed, and
                     state if the item names should be modified

HeaderDefNamesPage - Class generating a dialog page, where the user can modify
                     the names for all chosen header items for the wanted table

HeaderModNamesPage - Class generating a dialog page, where the user has to
                     match the default names of the odML header items to all
                     modified header item names of the loaded table

RedundancyPage     - Class generating a dialog page, where the user can state
                     if and which redundant information should be displayed in
                     the wanted table

MarkColumnPage     - Class generating a dialog page, where the user can decide
                     if and which column of the wanted table should be
                     emphasized compared to the remaining columns

BackPatternPage    - Class generating a dialog page, where the user can decide
                     if and which background pattern type should be used for
                     the wanted table

StylePage          - Class generating a dialog page, where the user can see the
                     style (background color, font style) of the chosen pattern
                     and can decide to change the style for the pattern fields,
                     individually

StyleModPage       - Class generating a dialog page, where the user can change
                     the background colors, the font colors, and the font style
                     for a selected pattern field of the wanted table

SavePage           - Class generating a dialog page, where the user defines the
                     location, and filename of the file that he wants to save


@author: zehl
"""

