|effect example|description|
|-|-|
|increase size by n|increases creature's size by n steps, e.g. from "small" to "medium"|
|decrease size by n|increases creature's size by n steps, e.g. from "small" to "medium"|
|set size to foo|sets creature's size to "foo"|
|set type to foo|sets creature's primary type to "foo"|
|set type to foo (bar)|sets creature's primary type to "foo" and secondary type to "bar"|
|foo bar-aligned|sets creature's alignment to "foo bar"|
|increase AC by n|increases creature's AC by n|
|decrease AC by n|decreases creature's AC by n|
|set AC to n|sets creature's AC to n|
|set AC to n + STAT|sets creature's AC to n + STAT, where STAT is an ability score such as DEX|
|set AC to n + XdY + STAT|sets creature's AC to n + XdY + STAT|
|set AC type to foo|sets creature's AC type to "foo", e.g. "natural armor"|
|set HP to n||
|reset HP|if creature has hit dice, recalculates the creatures HP|
|increase hit dice by n||
|set hit dice to XdY|proficiency bonus is also set to 2 + floor(num_hit_dice - 1 / 4)|
|set hit point bonus to n||
|set hit point bonus to STAT||
|set speed to n ft.||
|increase climb speed by n ft.||
|decrease swim speed by n ft.||
|set STAT to n||
|increase STAT by n||
|decrease STAT by n||
|clear damage resistances|remove all damage resistances|
|add resistance to foo, bar damage|adds "foo" and "bar" to damage resistances, and removes them from vulnerabilities|
|add immunity to foo, bar damage|adds "foo" and "bar" to damage immunities, removes them from resist/vuln|
|add vulnerability to foo, bar damage|adds "foo" and "bar" to damage vulnerabilities, removes from resist/immune|
|remove vulnerability to foo, bar damage||
|add resistance to bludgeoning, piercing, and slashing damage from...|special case for resist/immune/vulnerable|
|add immunity to foo, bar|adds "foo" and "bar" to condition immunities|
|set STAT saving throw to n + STAT||
|set foo skill to n + STAT||
|increase darkvision by n||
|add language foo||
|increase telepathy by n||
|add ability Foo: can foo bars|adds this ability to the section before the Action section|
|add action Foo: foos the bar with 2d6 + STR + proficiency||
|add bonus action Foo: foos the bar||
|add reaction Foo: foos the bar||
|add legendary action Foo: foos the bar||
|increase legendary actions by n|increase the number of legendary actions creature can take by n|
