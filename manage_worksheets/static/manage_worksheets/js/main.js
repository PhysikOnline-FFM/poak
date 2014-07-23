// onload
$(function() {
    // get a JSON-file with all tags
    $.getJSON("tags", function( data ) {

        // loop over all tags
        $.each(data['tags'], function(index, value) {
            $("#tags ul").append(
                $('<li>').append(value)
            )
        });
    });

    $.getJSON("worksheet_list", function( data ) {
        worksheets = data['worksheet_list']
        pokal_url = data['pokal_url']
        $.each(worksheets, function(index, worksheet_id) {
            $.getJSON("worksheet_details/"+worksheet_id, function( worksheet ) {
                $("#worksheets ul").append(
                    '<li><a href="'+pokal_url+'/home/pub/'+worksheet['worksheet_id']+'">'
                    +'<span class="ws_link">'+worksheet['title']+'</span></a> '
                    +'<a href="u/'+worksheet['worksheet_id']+'">(Kommentare)</a></li>'
                )
            });
        });
    });
});
