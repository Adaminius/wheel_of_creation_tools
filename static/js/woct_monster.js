$('document').ready(function () {
    $.get("/getAllTagLists", function (data) {
        // console.log(data);
        $('#tagListDropdown').html(data);
    });

    $.get("/getAllStatblocks", function (data) {
        console.log(data);
        $('#statblockDropdown').html(data);
    });

    $('#tagsToApplyDiv').on('click', '.tag-button', function () {
        $(this).closest('button').remove();
    });

    $('#applyTagsButton').on('click', function () {
        let tags = [];
        $('#tagsToApplyDiv').children().each(function() {
            tags.push({'name': $(this).attr('data-name'), 'filename': $(this).attr('data-filename')});
        });

        console.log('sending tags ' + tags);
        console.log(tags);

        let payload = {'tags[]': tags, 'statblock': $('#baseStatblockTextArea').val()};
        $.ajax({
            type: 'POST',
            url: '/modifyStatblock',
            data: JSON.stringify(payload),
            dataType: 'text',
            contentType: 'application/json; charset=utf-8',
            success: function (data) {
                console.log(data);
                $('#modifiedStatblockTextArea').html(data);
            },
            error: function (data) {
                console.log(data)
            }
        });
    });

    $('#clearButton').on('click', function() {
        $('#tagsToApplyDiv').children().remove();
    });

    $('#addRandomButton').on('click', function () {
        // remove stuff that we already have that doesn't stack
        let existingNonstackingTags = [];
        $('#tagsToApplyDiv').children().each(function() {
            tagNode = $(this);
            if (tagNode.attr('data-stacks') === 'False')
                existingNonstackingTags.push(tagNode.attr('data-name') + tagNode.attr('data-filename'));
        });

        let choices = [];
        let weights = [];
        $('#availableTagTable').children().each(function() {
            tagNode = $(this);
            if(existingNonstackingTags.indexOf(tagNode.attr('data-name') + tagNode.attr('data-filename')) < 0) {
                choices.push(tagNode);
                weights.push(parseFloat(tagNode.attr('data-weight')));
            }
        });

        if (choices.length === 0)
            return;

        let tag = chooseWeighted(choices, weights);
        console.log('addRandom ' + tag.attr('data-filename') + ' ' + tag.attr('data-name'));
        selectTag(tag.attr('data-filename'), tag.attr('data-name'), tag.attr('data-stacks'));
    })
});

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
    for (let i = 0; i < weights.length; i++)
    {
        rand -= weights[i];
        if (rand <= 0)
            return choices[i];
    }
    console.log("chooseWeighted failed, I don't know what I'm doing");
    return choices[0];
}

function selectTagList(filename) {
    console.log('selectTagList ' + filename);
    $.get("/getTagList", {'filename': filename}, function (data) {
        // console.log(data);
        $('#availableTagTable').html(data);
    })
}

function selectStatblock(filename) {
    console.log('selectStatblock ' + filename);
    $.get("/getStatblock", {'filename': filename}, function (data) {
        // console.log(data);
        $('#baseStatblockTextArea').text(data);
    })
}

    // <div class="col-md-6" id="tagsToApplyDiv"
    //      style="border-left: solid 1px rgba(0,0,0,.1); margin-left: 1rem; padding-left: 1rem; min-width: 6rem">
    //   <button class="btn btn-danger"><strong>&times</strong> lumbering</button>
    // </div>

function selectTag(filename, tagName, stacks) {
    console.log('selectTag ' + filename + ' ' + tagName);
    $('#tagsToApplyDiv').append(`<button class="btn btn-danger tag-button" data-stacks="${stacks}" data-filename="${filename}" data-name="${tagName}" title="${filename}"><strong>&times</strong> ${tagName}</button>`)
}





