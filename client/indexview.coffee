String.prototype.format = ->
    args = arguments
    return @replace(/\{(\d+)\}/g, (m, n) -> return args[n])

$ ->
    # get a JSON-file with all tags
    $.getJSON "tags", (data) ->
        tag_html = '<li><input type="checkbox" name="tag" value="{0}" id="tag{0}"/>
            <label for="tag{0}">{1}</label></li>'
        $.each data.tags, (index, tag) ->
            $("#tags ul").append(
                $("<li>").append(tag_html.format(tag[0], tag[1]))
            )
            $("#tag"+tag[0]).change ->
                on_change_tag($(this))

    # html-code for the links with placeholders
    ws_html = '<li><a href="{0}/{1}"><span class="ws_link">{2}</span></a>
        <a href="{3}{1}">(Kommentare)</a></li>'
    $.getJSON "worksheet_list", (data) ->
        worksheets = data.worksheet_list
        pokal_url =  data.pokal_url
        details_base_url = data.details_base_url
        $.each worksheets, (index, worksheet_id) ->
            $.getJSON "worksheet_details/"+worksheet_id, (worksheet) ->
                $("#worksheets ul").append(
                    # fill the placeholders in the html-code
                    ws_html.format(pokal_url, worksheet.worksheet_id,
                        worksheet.title, details_base_url)
                )


on_change_tag = (tag_obj) ->
    $.getJSON "worksheets_for_tag/"+tag_obj.attr("value"), (data) ->
        worksheet_ids = data.worksheet_list
        alert "passende worksheets: "+worksheet_ids.join()
