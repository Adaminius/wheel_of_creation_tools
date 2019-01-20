$('document').ready(function () {

$.get("/getAllTagLists", function (data) {
    console.log(data);
    $('#tagListDropdown').html(data);
});

$.get("/getAllStatblocks", function (data) {
    console.log(data);
    $('#statblockDropdown').html(data);
});

});

function selectTagList(filename) {
    console.log('selectTagList ' + filename);
    $.get("/getTagList", {'filename': filename}, function (data) {
        console.log(data);
        $('#availableTagTable').html(data);
    })
}
