-- Delete contact field with given value.
--
--   $ osascript delete.applescript [contact_id] home_page


on deleteField(thePersonId, theField)
    tell application "Contacts"
        set thePerson to person id thePersonId
        if theField is "home_page"
            delete home page of thePerson
        else
            error "Cannot delete " & theField
        end if
        save()
    end tell
end


on run argv
    set thePersonId to item 1 of argv
    set theField to item 2 of argv

    deleteField(thePersonId, theField)

    return
end
