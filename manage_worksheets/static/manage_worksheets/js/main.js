$(function() {
    // start
    $.getJSON("tags", function( data ) {
        alert(data['tags']);
    });
});
