-- Updates contact field with given value.
--
--   $ osascript update.applescript [contact_id] prefix [prefix]
--   $ osascript update.applescript [contact_id] first_name [first_name]
--   $ osascript update.applescript [contact_id] middle_name [middle_name]
--   $ osascript update.applescript [contact_id] last_name [prelast_namefix]
--   $ osascript update.applescript [contact_id] maiden_name [maiden_name]
--   $ osascript update.applescript [contact_id] suffix [suffix]
--   $ osascript update.applescript [contact_id] nickname [nickname]
--   $ osascript update.applescript [contact_id] phone [phone_id] [phone_number]


on updateInfo(thePersonId, theField, theInfoId, theLabel, theValue)
    tell application "Contacts"
        tell person id thePersonId
            if theField is "phones"
                set theInfo to phone id theInfoId
            else if theField is "emails"
                set theInfo to email id theInfoId
            else if theField is "urls"
                set theInfo to url id theInfoId
            end if

            tell theInfo
                set label to theLabel
                set value  to theValue
            end tell
        end tell
        save()
    end tell
end


on updateField(thePersonId, theField, theValue)
    tell application "Contacts"
        tell person id thePersonId
            if theField is "prefix"
                set prefix to theValue
            else if theField is "first_name"
                set first name to theValue
            else if theField is "middle_name"
                set middle name to theValue
            else if theField is "last_name"
                set last name to theValue
            else if theField is "maiden_name"
                set maiden name to theValue
            else if theField is "suffix"
                set suffix to theValue
            else if theField is "nickname"
                set nickname to theValue
            else
                error "Cannot update " & theField
            end if
        end tell
        save()
    end tell
end


on run argv
    set thePersonId to item 1 of argv
    set theField to item 2 of argv

    if theField is in {"phones", "urls"}
        set theInfoId to item 3 of argv
        set theLabel to item 4 of argv
        set theValue to item 5 of argv
        updateInfo(thePersonId, theField, theInfoId, theLabel, theValue)
    else
        set theValue to item 3 of argv
        updateField(thePersonId, theField, theValue)
    end if
end
