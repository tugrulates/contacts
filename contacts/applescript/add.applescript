-- Adds contact info with given label and value.
--
--   $ osascript add.applescript [contact_id] url [url_label] [url_value]


on addInfo(thePersonId, theField, theLabel, theValue)
    tell application "Contacts"
        tell person id thePersonId
            set theProperties to {label: theLabel, value: theValue}
            if theField is "phones"
                make new phone at end of phones with properties theProperties
            else if theField is "urls"
                make new url at end of urls with properties theProperties
            end if
        end tell
        save()
    end tell
end


on run argv
    set thePersonId to item 1 of argv
    set theField to item 2 of argv
    set theLabel to item 3 of argv
    set theValue to item 4 of argv

    if theField is in {"phones", "urls"}
        addInfo(thePersonId, theField, theLabel, theValue)
    else
        error "Cannot update " & theField
    end if

    return
end
