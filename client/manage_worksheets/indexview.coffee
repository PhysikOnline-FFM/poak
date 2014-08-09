# on document ready
$ ->
    # get a JSON-file with all tags
    $.getJSON "tags", (data) ->
        tag_html = (tag_id, tag_name) ->
            "<li><input type=\"checkbox\" name=\"tag\" value=\"#{tag_id}\" id=\"tag#{tag_id}\"/>
            <label for=\"tag#{tag_id}\">#{tag_name}</label></li>"

        # loop over all tags
        for tag in data.tags
            tag_id = tag[0]
            tag_name = tag[1]

            # create the list items
            $("#tags ul").append(tag_html tag_id, tag_name)

            # register function for the change event
            $("#tag"+tag[0]).change -> on_change_tag($(this))

    # html-code for the links with placeholders
    ws_html = (pokal_url, worksheet_id, worksheet_title, details_base_url) ->
        "<li id=\"ws#{worksheet_id}\"><a href=\"#{pokal_url}/#{worksheet_id}\">
        <span class=\"ws_link\">#{worksheet_title}</span></a>
        <a href=\"#{details_base_url}#{worksheet_id}\">(Kommentare)</a></li>"

    $.getJSON "worksheet_list", (data) ->
        worksheets = data.worksheet_list
        pokal_url =  data.pokal_url
        details_base_url = data.details_base_url
        for worksheet_id in worksheets
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
