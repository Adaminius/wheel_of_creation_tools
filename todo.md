# Monster Builder

## Something need doing?

* Features
    * Include bloodied threshold in statblock to use for future mechanics
    * Use an int like 'num_can_multiattack' for actions instead of 'can_multiattack', might allow us to do stuff like claw-claw-bite
    * Open preview in new window
    * Use pyparsing to implement multiplication, basic functions, operator precedence in the curly bracket stuff
    * Need to rework multiattack -- could add can_multiattack attribute to Actions, then set # by hit dice/desired DPR?
    * Export to Roll20
    * In the preview: click to roll dice, form-fill HP (so you could use this to track HP if you were only using the site)
    * Save preview PNG
    * Max AC for each type of armor?
    * Make copy a button instead of clicking on the box
    * Random names by type e.g. drekavats for a Winter fey
    * Improve layout for mobile users
    * on_to_markdown Callback
    * Add burrow speed
    * Handle spells?
    * Add to_json() and flatten_json() methods for Statblock?
      * We can use this for a "save/load statblock to/from file" button below the output text.
      * Can just look like:
         ```
         {"original_statblock": "...",  // original markdown
          "tags": [{"name": "Aestival", "file": "fey_means.py"}, ...]
         }
         ```
      * Then to remake we just parse the original statblock and reapply the tags
* Design/Mechanics
    * Need something that's vulnerable to poison damage and the various types of damage in general
    * Kostlyavtsi should most of the time wear armor instead of having natural armor? maybe handle that with a humanoidish statblock?f
* Text changes
* Code health/quality
    * Split templates into external files instead of inline in flask code
    * Move styling over into separate CSS file
* Bugs
    * fix immunity to bps output, still getting extra semicolon?
* Uncategorized
    * Figure out licensing?


## Job's done!

* Maybe do something like size sets die size, hit dice set # of dice
* Set minimum stats for different types?
* A 'create lesser minions' or 'create lesser undead' action that does something like
       * Create d4 Undead Minions. They have:
* Figure out how to comply with FCP or OGL?
* Pretty horizontal rule similar to official books in preview
* Loot
* Update Stablock.from_markdown() to create a new class first instead of building from dictionary
* Fix Feature descriptions
* Update applying tags to modify a copy of class
* Use deep copies and Statblock.applied_tags to remove tags e.g.:
    * You've got a statblock with two tags: *Dumb*, *Nice Jacket*
    * We want to apply the tag *Smart*
    * *Smart* has an override for *Dumb*, and it wants to remove *Dumb* in its on_override()
    * We should roll back the Statblock to its untagged state, then apply *Nice Jacket* and *Smart*
    * Our final Statblock will just have the tags: *Nice Jacket*, *Smart*
* Add some tests
    * Might be useful to have a method that determines which attributes in one Statblock object
    are different from another
* Include applied tags in statblock
* Split parser/website code into separate dirs
* Get web code actually working
* Fix www
* Fix language input/output
* Handle damage for melee/spell/ranged attacks
* Markdown preview
* Prefill input markdown, output markdown, and preview
* Copy markdown on click
* Change "springy" to "vernal"
* Header fonts in preview need to be flipped?
* Fix result tooltip to say "copy to clipboard" instead of "copy to keyboard", make updated tooltip match this text
* fix Necrin output languages it knew **IN** life
* Reconfigure proficiency bonus calculation to `1 + math.ceil(n / 4.)` # actually 1 + int(max(math.ceil(self.hit_dice.count / 4), 0))
* Add table descriptions
* Hit dice slider
* CR calculation
* Rename "Action" class to "Feature"
