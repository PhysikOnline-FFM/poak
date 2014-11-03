# html-code for the links with placeholders
ws_html = (pokal_url, worksheet_pk, worksheet_id, worksheet_title, details_base_url, tags, comments) ->
    ret = "<li id=\"ws#{worksheet_pk}\" class=\"list-group-item\">"
    ret += "<a class=\"ws_link\" href=\"#{pokal_url}/#{worksheet_id}\">#{worksheet_title}</a>"
    ret += "<a class=\"btn btn-xs btn-default pull-right\" href=\"#{details_base_url}#{worksheet_pk}\">#{comments} Kommentare</a>"
    ret += "<div>"
    for tag in tags
        ret += "<span class=\"label label-primary\">#{tag}</span>"
    ret += "</div></li>"
    return ret

ws_list_set = (worksheet_pks) ->
    $("#worksheets ul").empty()
    ws_list_add worksheet_pks

ws_list_add = (worksheet_pks) ->
    lis = $("#worksheets ul").children()
    for worksheet_pk in worksheet_pks

        # test for duplicates
        found = false
        lis.each () ->
            if $(this).attr("id") == "ws"+worksheet_pk
                found = true
                return false # stop looking
        if found
            continue # skip this worksheet_pk

        # if there is no duplicate, get the details and append it to the list
        $.getJSON "worksheet_details/"+worksheet_pk, (worksheet) ->
            $("#worksheets ul").append(
                # fill the placeholders in the html-code
                ws_html window.pokal_url, worksheet.pk, worksheet.worksheet_id, worksheet.title, window.details_base_url, worksheet.tags, worksheet.comments
                )

ws_list_remove = (worksheet_pks) ->
    for worksheet_pk in worksheet_pks
        $("#ws"+worksheet_pk).remove()

all_checked_tags = () ->
    checked_tags = []
    tags = $("#tags ul").find("input").each () ->
        if $(this).prop("checked")
            checked_tags.push $(this).attr("value")
    return checked_tags

# on document ready
$ ->
    # get a JSON-file with all tags
    $.getJSON "tags", (data) ->
        tag_html = (tag_id, tag_name) ->
            "<li class=\"list-group-item\"><label><input type=\"checkbox\" name=\"tag\" value=\"#{tag_id}\" id=\"tag#{tag_id}\"/> #{tag_name}</label></li>"

        # loop over all tags
        for tag in data.tags
            tag_id = tag[0]
            tag_name = tag[1]

            # create the list items
            $("#tags ul").append(tag_html tag_id, tag_name)

            # register function for the change event
            $("#tag"+tag_id).change -> on_change_tag($(this))
    $("#tagall").change -> on_change_tagall($(this))

    $.getJSON "worksheet_list", (data) ->
        worksheets = data.worksheet_list

        # save as global variables
        window.pokal_url =  data.pokal_url
        window.details_base_url = data.details_base_url

        ws_list_set worksheets


on_change_tag = (tag_obj) ->
    if tag_obj.prop("checked") # we have to add worksheets to the list
        $.getJSON "worksheets_for_tag/"+tag_obj.attr("value"), (data) ->
            worksheet_pks = data.worksheet_list
            tagall = $("#tagall")
            if tagall.prop("checked")
                $("#tagall").prop "checked", false
                ws_list_set worksheet_pks
            else
                ws_list_add worksheet_pks
    else # we remove worksheets
        ch_tags = all_checked_tags()
        $.getJSON "minus_tag/"+tag_obj.attr("value"),
            {"checked_tags":ch_tags},
            (data) ->
                worksheet_pks = data.worksheet_list
                ws_list_remove worksheet_pks

# gets called if the checkbox "Alle" is clicked
on_change_tagall = (tagall) ->
    if tagall.prop("checked") #checkbox was checked
        $("#tags ul li input").not("#tagall").prop("checked", false)
        $.getJSON "worksheet_list", (data) ->
            worksheet_pks = data.worksheet_list
            ws_list_set worksheet_pks
    else
        # remove all worksheets
        ws_list_set []
