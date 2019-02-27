# Wheel of Creation Tools

https://wheelofcreation.net

***The Wheel of Creation*** is my upcoming setting and rules supplement for the **5th Edition of the world's 
most popular roleplaying game**, using the Open Gaming License (OGL, see OpenGameLicense.txt). 
This project provides is intended to provide tools with a web interface to 
make the lives of gamemasters running the Wheel of Creation easier.

Want to know more about the book? Check out [what_is_woc.md!](https://github.com/Adaminius/wheel_of_creation_tools/blob/master/what_is_woc.md)

Want to join the mailing list to receive updates on the development of the WoC web tools and ruleset? [Click here!
](https://goo.gl/forms/heNTn65JcNjKm6hZ2)

## Monster Generator

This first (and currently, only) tool is for the most rules-heavy portion of the supplement, 
random monster generation. 
It parses 5e monster statistics in the form of markdown, which is used on sites like 
[GM Binder](https://www.gmbinder.com/) and [the Homebrewery](https://homebrewery.naturalcrit.com/) 
to format statistics and abilities for non-player characters (NPCs) in the style of official 5e books 
(***statblocks***).

You can then add different ***tags*** of your choice or at random which modify these statblocks
in various ways. The tagging system is quite robust, and includes callbacks for applying tags,
overwriting tags, removing tags, and stacking tags.

Once all tags are applied, any arithmetic expressions in the block (contained in curly braces, 
e.g. '{1d6 + STR}') are calculated, such as for determining the damage an attack deals 
based on the monster's strength. A new markdown file with all modifications is generated that 
can be pasted into GM Binder or Homebrewery documents, and a preview is shown.

Many more features and content are planned, including  
more base statblocks, more tag tables, additions to current tag tables, and additional ways to save, view, and use your monsters.

## Project Structure

* **static/**
    * **js/** Client-side code
    * **css/** Website styling
    * **html/** Static HTML
* **templates/** Webpage HTML templates for Flask
* **tags/** Tag tables live here, each in their own Python file. Each contains a dictionary of tags,
a table name, and a table description. They are reimported by the server each time a client makes a 
tag apply request, if the DEBUG flag for the server is set, making it possible to iterate on tag
design without tearing down and relaunching the server
* **tags_unused/** Tag tables which I don't think have enough content to be worth sharing yet
* **statblocks/** Markdown statblocks which will be modified by the application
* **tests/** Pytest tests
* **main.py** This is where the Flask server code lives. Looks up statblocks, looks up tag tables, 
and applies tags as requested by the client
* **statblock.py** Code for parsing, modifying, and outputting Statblocks. Includes the Tag and
Stablock classes and supporting functions.
* **utils.py** Misc utility functions and building blocks of lower-level game mechanics, including the 
RollableTable, Dice, AbilityScore, and ChallengeRating classes. Of note is the Feature class: objects of this class represent special abilities and the
actions a creature can take, and this includes the code for parsing the variables and
operators in curly braces '{}' as described above.
* **common_features.csv** A list of frequently-used creature features (e.g. '***Amphibious.*** This creature can breathe both air and water.') that are parsed as 
Feature by utils.py and referenced in tag tables
* **requirements.txt** Required Python modules for running the server (use *pip* to install)
* **app.yaml** For hosting on Google App Engine
* **OpenGameLicense.txt** License required to use the content of the 5th Edition System Reference Document (SRD)

Copyright (c) 2019 Adam Mansfield
