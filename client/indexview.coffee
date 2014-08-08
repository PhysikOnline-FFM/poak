# on document ready
$ ->
    # get a JSON-file with all tags
    $.getJSON "tags", (data) ->
        tag_html = (tag_id, tag_name) ->
            "<li><input type=\"checkbox\" name=\"tag\" value=\"#{tag_id}\" id=\"tag#{tag_id}\"/>
            <label for=\"tag#{tag_id}\">#{tag_name}</label></li>"
        $.each data.tags, (index, tag) ->
            $("#tags ul").append(
                $("<li>").append(tag_html tag[0], tag[1])
            )
            $("#tag"+tag[0]).change ->
                on_change_tag($(this))

    # html-code for the links with placeholders
    ws_html = (pokal_url, worksheet_id, worksheet_title, details_base_url) ->
        "<li><a href=\"#{pokal_url}/#{worksheet_id}\">
        <span class=\"ws_link\">#{worksheet_title}</span></a>
        <a href=\"#{details_base_url}#{worksheet_id}\">(Kommentare)</a></li>"
    $.getJSON "worksheet_list", (data) ->
        worksheets = data.worksheet_list
        pokal_url =  data.pokal_url
        details_base_url = data.details_base_url
        $.each worksheets, (index, worksheet_id) ->
            $.getJSON "worksheet_details/"+worksheet_id, (worksheet) ->
                $("#worksheets ul").append(
                    # fill the placeholders in the html-code
                    ws_html pokal_url, worksheet.worksheet_id,
                        worksheet.title, details_base_url
                )


on_change_tag = (tag_obj) ->
    $.getJSON "worksheets_for_tag/"+tag_obj.attr("value"), (data) ->
        worksheet_ids = data.worksheet_list
        alert "passende worksheets: "+worksheet_ids.join()
