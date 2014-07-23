// useful function
String.prototype.format = function () {
  var args = arguments;
  return this.replace(/\{(\d+)\}/g, function (m, n) { return args[n]; });
};

// onload
$(function() {
    // get a JSON-file with all tags
    $.getJSON("tags", function( data ) {
        var tag_html = '<li><input type="checkbox" name="tag" value="{0}" id="tag{0}"/>' +
                '<label for="tag{0}">{1}</label></li>';
        // loop over all tags
        $.each(data.tags, function(index, tag) {
            $("#tags ul").append(
                $('<li>').append(tag_html.format(tag[0], tag[1]))
            );
        });
    });

    // html-code for the links with placeholders
    var ws_html = '<li><a href="{0}/home/pub/{1}"><span class="ws_link">{2}</span></a> '+
            '<a href="u/{1}">(Kommentare)</a></li>';
    $.getJSON("worksheet_list", function( data ) {
        worksheets = data.worksheet_list;
        pokal_url = data.pokal_url;
        $.each(worksheets, function(index, worksheet_id) {
            $.getJSON("worksheet_details/"+worksheet_id, function( worksheet ) {
                $("#worksheets ul").append(
                    // fill the placeholders in the html-code
                    ws_html.format(pokal_url, worksheet.worksheet_id, worksheet.title)
                );
            });
        });
    });
});
