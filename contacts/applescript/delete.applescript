-- Delete contact field with given value.
--
--   $ osascript delete.applescript [contact_id] home_page


on deleteField(thePersonId, theField)
    tell application "Contacts"
        tell person id thePersonId
            if theField is "home_page"
                delete home_page
            else
                error "Cannot delete " & theField
            end if
        end tell
        save()
    end tell
end


on deleteInfo(thePersonId, theField, theInfoId)
    tell application "Contacts"
        tell person id thePersonId
            if theField is "phones"
                delete phone id theInfoId
            else if theField is "emails"
                delete email id theInfoId
            else if theField is "urls"
                delete url id theInfoId
            else if theField is "addresses"
                delete address id theInfoId
            else if theField is "custom_dates"
                delete custom date id theInfoId
            else if theField is "social_profiles"
                set service name of social profile id theInfoId to ""
                set user name of social profile id theInfoId to ""
                set user identifier of social profile id theInfoId to ""
                set url of social profile id theInfoId to ""
            else if theField is "instant_messages"
                -- duplicates are automatically deleted on save
            else
                error "Cannot delete " & theField
            end if
        end tell
        save()
    end tell
end


on run argv
    set argc to count of argv

    if argc is 2
        set thePersonId to item 1 of argv
        set theField to item 2 of argv
        deleteField(thePersonId, theField)
    else
        set thePersonId to item 1 of argv
        set theField to item 2 of argv
        set theInfoId to item 3 of argv
        deleteInfo(thePersonId, theField, theInfoId)
    end

    return
end
