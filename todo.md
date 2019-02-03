## Something need doing?

* A 'create lesser minions' or 'create lesser undead' action that does something like
   * Create d4 Undead Minions. They have:
      * Die if they take damage
      * AC 12 (armor scraps)
      * speed 30 ft.
      * +2 to hit, d6 damage, range 80/320 ft. (shortsword/shortbow)
      * +2 on STR/DEX/CON saves and skills
      * -2 on INT/WIS/CHA saves and skills
      * immunity to poison and necrotic damage
      * immunity to the poisoned condition
* Similar 'create greater undead' that have + 2 to all that, and die if they take damage twice, take radiant damage, or take a critical hit
* Necrin shouldn't have magic resistance, that's for Constructs. Need to give them something else defining?
* Use pyparsing to implement multiplication, basic functions, operator precedence in the curly bracket stuff
* Reconfigure proficiency bonus calculation to `1 + math.ceil(n / 4.)`
* Set minimum stats for different types?
* fix immunity to bps output, still getting extra semicolon
* fix Necrin output languages it knew **IN** life
* Need something that's vulnerable to poison damage and the various types of damage in general
* Hit dice slider
* CR calculation
* Need to rework multiattack
* Necrin should most of the time wear armor instead of having natural armor? maybe handle that with a humanoidish statblock?
* Export to Roll20
* Pretty horizontal rule similar to official books in preview
* In the preview: click to roll dice, form-fill HP (so you could use this to track HP if you were only using the site)
* Save preview PNG
* Max AC for each type of armor?
* Make copy a button instead of clicking on the box
* Add table descriptionis
* Random names by type e.g. drekavats for a Winter fey
* Maybe do something like size sets die size, hit dice set # of dice
* Size tags -- spritely?
* Write tags!
* Write a real README/License
* Add OGL info from WotC?
* Optimize for mobile
* Add burrow speed
* Need to infer skills/ability score to use in actions?
* Handle spells
* Add to_json() and flatten_json() methods for Statblock? 


## Job's done!

* Update Stablock.from_markdown() to create a new class first instead of building from dictionary
* Fix Action descriptions
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
