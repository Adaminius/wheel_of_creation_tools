$('document').ready(function () {
    /**
     * Request the list of tag tables to choose from
     */
    $.get("/getAllTagLists", function (data) {
        $('#tagListDropdown').html(data);
    });

    /**
     * Request the list of statblocks to choose from
     */
    $.get("/getAllStatblocks", function (data) {
        console.log(data);
        $('#statblockDropdown').html(data);
    });

    /**
     * Click on a tag in the list of tags to be applied to remove it
     */
    $('#tagsToApplyDiv').on('click', '.tag-button', function () {
        $(this).closest('button').remove();
    });

    /**
     * Send the base statblock and list of tags to be applied to the server, receive the modified statblock and preview,
     * update page to show modified statblock and preview
     */
    $('#applyTagsButton').on('click', function () {
        let tags = [];
        $('#tagsToApplyDiv').children().each(function () {
            tags.push({'name': $(this).attr('data-name'), 'filename': $(this).attr('data-filename')});
        });

        console.log('sending tags ' + tags);
        console.log(tags);

        let payload = {'tags[]': tags, 'statblock': $('#baseStatblockTextArea').val()};

        let numHitDice = parseInt($('#hitDiceRange').val());
        if (numHitDice > 0)
            payload['hitdice'] = numHitDice;

        $.ajax({
            type: 'POST',
            url: '/modifyStatblock',
            data: JSON.stringify(payload),
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            success: function (data) {
                console.log(data);
                $('#modifiedStatblockTextArea').text(data['markdown']);
                $('#mdPreview').empty().append(data['html']);
                let lootTableElement = $('#lootMarker').parent().parent().parent();
                lootTableElement.addClass('lootTable');
                lootTableElement.addClass('table-striped');
            },
            error: function (data) {
                console.log(data)
            }
        });
    });

    /**
     * Clear all tags to be applied
     */
    $('#clearButton').on('click', function () {
        $('#tagsToApplyDiv').children().remove();
    });

    /**
     * This button adds a random tag based on whether the tag has already been applied, its weight, and whether its
     * required tags are present.
     */
    $('#addRandomButton').on('click', function () {
        // remove stuff that we already have that doesn't stack
        let existingNonstackingTags = [];
        let existingTags = [];
        let overwrittenFlagsArr = [];
        let overwrittenFlags = new Set();

        $('#tagsToApplyDiv').children().each(function () {
            let tagNode = $(this);
            overwrittenFlagsArr.push(new Set(tagNode.attr('data-overwritten').split(';')));
            for (const element of tagNode.attr('data-overwritten').split(';')) {
                overwrittenFlags.add(element);
            }
            if (tagNode.attr('data-stacks') === 'False')
                existingNonstackingTags.push(tagNode.attr('data-name') + '$' + tagNode.attr('data-filename'));
            existingTags.push(tagNode.attr('data-name') + '$' + tagNode.attr('data-filename'));
        });

        let choices = [];
        let weights = [];
        $('#availableTagTable').children().each(function () {
            let tagNode = $(this);
            if (existingNonstackingTags.indexOf(tagNode.attr('data-name') + '$' + tagNode.attr('data-filename')) < 0) {
                if (willOverwrite(tagNode, overwrittenFlags)) {
                    console.log(tagNode.attr('data-name') + ' will overwrite one or more already applied tags');
                    return;
                }
                if (!hasRequiredTags(tagNode, existingTags)) {
                    console.log('Missing required tags for ' + tagNode.attr('data-name'));
                    return;
                }
                choices.push(tagNode);
                weights.push(parseFloat(tagNode.attr('data-weight')));
            }
        });

        if (choices.length === 0)
            return;

        let tag = chooseWeighted(choices, weights);
        // console.log('addRandom ' + tag.attr('data-filename') + ' ' + tag.attr('data-name'));
        selectTag(tag.attr('data-filename'), tag.attr('data-name'), tag.attr('data-stacks'),
            tag.attr('data-overwritten'));
    });

    let similarMonsters = defaultDict = new Proxy({}, {
            get: (target, name) => name in target ? target[name] : ''
        });
    similarMonsters[1] = '(Goat)';
    similarMonsters[2] = '(Wolf)';
    for (let i = 3; i < 6; i++) similarMonsters[i] = '(Lion)';
    for (let i = 6; i < 9; i++) similarMonsters[i] = '(Ogre)';
    for (let i = 9; i < 13; i++) similarMonsters[i] = '(Fire Elemental)';
    for (let i = 13; i < 16; i++) similarMonsters[i] = '(Young Dragon)';
    for (let i = 16; i < 18; i++) similarMonsters[i] = '(Vampire)';
    for (let i = 18; i < 20; i++) similarMonsters[i] = '(Lich)';
    for (let i = 20; i < 24; i++) similarMonsters[i] = '(Storm Giant)';
    for (let i = 24; i < 32; i++) similarMonsters[i] = '(Ancient Dragon)';
    for (let i = 32; i < 34; i++) similarMonsters[i] = '(Tarrasque)';

    $('#hitDiceRange').change(function() {
        let newVal = parseInt(this.value);

        if (newVal === 0)
            $('#hitDiceDisplay').html('[Use statblock]');
        else
            $('#hitDiceDisplay').html(similarMonsters[newVal]);
    });

    /**
     * Copy textarea on click
     * Based on David Z. Chen's blog
     * http://davidzchen.com/tech/2016/01/19/bootstrap-copy-to-clipboard.html
     */
    let modifiedTextArea = $('#modifiedStatblockTextArea');
    modifiedTextArea.tooltip();

    modifiedTextArea.bind('click', function () {
        let input = document.querySelector('#modifiedStatblockTextArea');
        input.setSelectionRange(0, input.value.length + 1);
        try {
            let success = document.execCommand('copy');
            if (success) {
                modifiedTextArea.trigger('copied', ['Copied!']);
            }
            else {
                modifiedTextArea.trigger('copied', ['Copy with Ctrl-c']);
            }
        }
        catch (err) {
            modifiedTextArea.trigger('copied', ['Copy with Ctrl-c']);
        }
    });

    modifiedTextArea.bind('copied', function (event, message) {
        $(this).attr('title', message)
            .tooltip('_fixTitle')
            .tooltip('show')
            .attr('title', "Copy modified statblock to clipboard")
            .tooltip('_fixTitle');
    });
});

/**
 * Return a weighted random choice from a list
 * @param choices - list of objects/values to choose from
 * @param weights - probability each element in choices will be chosen (should be same length as choices). Probability
 * will be recalculated over 1
 * @returns {*} - an element from choices
 */
function chooseWeighted(choices, weights) {
    // recalculate weights to total up to 1
    let total = 0;
    weights.forEach(function (weight) {
        total += weight;
    });
    let normalizedWeights = [];
    weights.forEach(function (weight) {
        normalizedWeights.push(weight / total);
    });
    weights = normalizedWeights;
    // generate number from 0 to 1
    let rand = Math.random();
    // subtract off weights until we are <= 0
    for (let i = 0; i < weights.length; i++) {
        rand -= weights[i];
        if (rand <= 0)
            return choices[i];
    }
    console.log("chooseWeighted failed, I don't know what I'm doing");
    return choices[0];
}

/**
 * When the user chooses a tag table, requests info on all tags in the table.
 * @param filename
 */
function selectTagList(filename) {
    console.log('selectTagList ' + filename);
    $.get("/getTagList", {'filename': filename}, function (data) {
        $('#availableTagTable').empty().append(data['tags']);
        $('#tagTableDescription').empty().append(data['description']);
    }, 'json')
}

/**
 * When the user chooses a statblock filename, requests the contents of the corresponding markdown file on the server
 * @param filename
 */
function selectStatblock(filename) {
    console.log('selectStatblock ' + filename);
    $.get("/getStatblock", {'filename': filename}, function (data) {
        // console.log(data);
        $('#baseStatblockTextArea').val(data);
    })
}

/**
 * When the user clicks to add a tag or adds a random tag, requests add it to the list of tags to be applied
 * @param filename - filename of the tag table module to look in (shown on mouseover, future mouseover should include more info)
 * @param tagName
 * @param stacks - whether the tag stacks (can be applied multiple times)
 * @param overwritten - comma-delimited string of flags which are used to determine whether this tag is overwritten by another tag
 */
function selectTag(filename, tagName, stacks, overwritten) {
    console.log('selectTag ' + filename + ' ' + tagName);
    $('#tagsToApplyDiv').append(`<button class="btn btn-danger tag-button" data-stacks="${stacks}" data-filename="${filename}" data-name="${tagName}" title="${filename}" data-overwritten="${overwritten}"><strong>&times</strong> ${tagName}</button>`)
}

/**
 * If a tag has other tags in its Requirements column, check to see if at least one required tag is present
 * @param tagNode - DOM node of the tag we want to check requirements on
 * @param existingTags - names of the tags we've already applied
 * @returns {Boolean}
 */
function hasRequiredTags(tagNode, existingTags) {
    // console.log('hasRequiredTags ' + tagNode.attr('data-requires').split(',') + ' ' + existingTags);
    if (tagNode.attr('data-requires') === '-')
        return true;
    let requiredTags = tagNode.attr('data-requires').split(',');
    let cleanedExistingTags = [];
    existingTags = existingTags.forEach(function (tagName) {
        cleanedExistingTags.push(tagName.split('$')[0]);
    });
    existingTags = cleanedExistingTags;

    let requirementsFailed = true;
    requiredTags.forEach(function (requiredTag) {
        if (!requirementsFailed)
            return;
        if (existingTags.indexOf(requiredTag) >= 0)
            requirementsFailed = false;
    });
    return !requirementsFailed;
}

/**
 * Checks if a tag would overwrite any tags with the flags given in overwrittenFlags
 * @param tagNode
 * @param overwrittenFlags {Set}
 * @returns {Boolean}
 */
function willOverwrite(tagNode, overwrittenFlags) {
    let will_overwrite = false;
    tagNode.attr('data-overwrites').split(';').forEach(function(overwritesFlag) {
        if (overwrittenFlags.has(overwritesFlag)) {
            will_overwrite = true;
        }
    });
    return will_overwrite;
}
