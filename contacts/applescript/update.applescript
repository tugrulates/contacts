-- Updates contact fields with given values.
--
--   $ osascript update.applescript prefix [prefix] [contact_id]
--   $ osascript update.applescript first_name [first_name] [contact_id]
--   $ osascript update.applescript middle_name [middle_name] [contact_id]
--   $ osascript update.applescript last_name [prelast_namefix] [contact_id]
--   $ osascript update.applescript maiden_name [maiden_name] [contact_id]
--   $ osascript update.applescript suffix [suffix] [contact_id]
--   $ osascript update.applescript nickname [nickname] [contact_id]
--   $ osascript update.applescript phone [phone_number] [contact_id] [phone_id]


on updatePhone(thePersonId, thePhoneId, thePhoneValue)
    tell application "Contacts"
        set thePerson to person id thePersonId
        set thePhone to phone id thePhoneId of thePerson
        set value of thePhone to thePhoneValue
    end tell
end


on updateField(thePersonId, theField, theValue)
    tell application "Contacts"
        set thePerson to person id thePersonId
        if theField is "prefix"
            set prefix of thePerson to theValue
        else if theField is "first_name"
            set first name of thePerson to theValue
        else if theField is "middle_name"
            set middle name of thePerson to theValue
        else if theField is "last_name"
            set last name of thePerson to theValue
        else if theField is "maiden_name"
            set maiden name of thePerson to theValue
        else if theField is "suffix"
            set suffix of thePerson to theValue
        else if theField is "nickname"
            set nickname of thePerson to theValue
        end if
    end tell
end


on run argv
    set argc to count of argv
    set theField to item 1 of argv
    set theValue to item 2 of argv
    set thePerson to item 3 of argv
    if argc > 4
        set theIds to item 4 thru argc of argv
    else
        set theIds to {}
    end if

    if theField is "phone"
        updatePhone(thePerson, item 1 of theIds, theValue)
    else
        updateField(thePerson, theField, theValue)
    end if
end
