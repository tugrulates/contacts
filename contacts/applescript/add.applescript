-- Adds contact info with given label and value.
--
--   $ osascript add.applescript [contact_id] url [url_label] [url_value]


on addUrl(thePersonId, theLabel, theValue)
    tell application "Contacts"
        tell person id thePersonId
            make new url at end of urls with properties {label: theLabel, value: theValue}
        end tell
        save()
    end tell
end


on run argv
    set thePersonId to item 1 of argv
    set theField to item 2 of argv
    set theLabel to item 3 of argv
    set theValue to item 4 of argv

    if theField is "urls"
        addUrl(thePersonId, theLabel, theValue)
    else
        error "Cannot update " & theField
    end if

    return
end
