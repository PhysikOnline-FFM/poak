# html-code for the links with placeholders
ws_html = (pokal_url, worksheet_id, worksheet_title, details_base_url, tags) ->
    ret = "<li id=\"ws#{worksheet_id}\"><a href=\"#{pokal_url}/#{worksheet_id}\">
    <span class=\"ws_link\">#{worksheet_title}</span></a>
    <a href=\"#{details_base_url}#{worksheet_id}\">(Kommentare)</a>"
    for tag in tags
        ret += "<span class=\"tag\">#{tag}</span>"
    ret += "</li>"
    return ret

ws_list_set = (worksheet_ids) ->
    $("#worksheets ul").empty()
    ws_list_add worksheet_ids

ws_list_add = (worksheet_ids) ->            
    # TODO: test for duplicates
    for worksheet_id in worksheet_ids
        $.getJSON "worksheet_details/"+worksheet_id, (worksheet) ->
            $("#worksheets ul").append(
                # fill the placeholders in the html-code
                ws_html window.pokal_url, worksheet.worksheet_id,
                    worksheet.title, window.details_base_url, worksheet.tags
                )

ws_list_remove = (worksheet_ids) ->
    # thats a bit harder
    $("#worksheets ul").children()

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
    $("#tagall").change -> on_change_tagall($(this))

    $.getJSON "worksheet_list", (data) ->
        worksheets = data.worksheet_list

        # save as global variables
        window.pokal_url =  data.pokal_url
        window.details_base_url = data.details_base_url

        ws_list_set worksheets


on_change_tag = (tag_obj) ->
    $.getJSON "worksheets_for_tag/"+tag_obj.attr("value"), (data) ->
        worksheet_ids = data.worksheet_list
        tagall = $("#tagall")
        if tag_obj.prop("checked")
            if tagall.prop("checked")
                $("#tagall").prop "checked", false
                ws_list_set worksheet_ids
            else
                ws_list_add worksheet_ids

# gets called if the checkbox "Alle" is clicked
on_change_tagall = (tagall) ->
    if tagall.prop("checked") #checkbox was checked
        tags = $("#tags ul").find("input").prop("checked", false)
        $.getJSON "worksheet_list", (data) ->
            worksheet_ids = data.worksheet_list
            ws_list_set worksheet_ids
    else
        # remove all worksheets
        ws_list_set []
