#### Todo

* ~~Update Stablock.from_markdown() to create a new class first instead of building from dictionary~~
* ~~Fix Action descriptions~~
* ~~Update applying tags to modify a copy of class~~
* ~~Use deep copies and Statblock.applied_tags to remove tags e.g.:~~
    * You've got a statblock with two tags: *Dumb*, *Nice Jacket*
    * We want to apply the tag *Smart*
    * *Smart* has an override for *Dumb*, and it wants to remove *Dumb* in its on_override()
    * We should roll back the Statblock to its untagged state, then apply *Nice Jacket* and *Smart*
    * Our final Statblock will just have the tags: *Nice Jacket*, *Smart*
* ~~Add some tests~~
    * Might be useful to have a method that determines which attributes in one Statblock object
    are different from another
* ~~Include applied tags in statblock~~
* ~~Split parser/website code into separate dirs~~
* ~~Get web code actually working~~
* Markdown preview
* CR calculation
* Set desired hit dice slider
* ~~Fix www~~
* ~~Fix language input/output~~
* Write tags!
* Write a real README/License
* Add OGL info from WotC
* Add burrow speed
* Need to infer skills/ability score to use in actions?
* ~~Handle damage for melee/spell/ranged attacks~~
* Handle spells
* Add to_json() and flatten_json() methods for Statblock? 
