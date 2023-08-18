-- Delete contact field with given value.
--
--   $ osascript delete.applescript [contact_id] [field]
--   $ osascript delete.applescript [contact_id] phones [phone_id]
--   $ osascript delete.applescript [contact_id] emails [email_id]
--   $ osascript delete.applescript [contact_id] urls [url_id]
--   $ osascript delete.applescript [contact_id] addresses [addresses_id]
--   $ osascript delete.applescript [contact_id] social_profiles [social_profile_id]
--   $ osascript delete.applescript [contact_id] instant_messages [instant_message_id]


on deleteField(thePersonId, theField)
    tell application "Contacts"
        tell person id thePersonId
            if theField is "prefix"
                delete prefix
            else if theField is "first_name"
                delete first name
            else if theField is "phonetic_first_name"
                delete phonetic first name
            else if theField is "middle_name"
                delete middle name
            else if theField is "phonetic_middle_name"
                delete phonetic middle name
            else if theField is "last_name"
                delete last name
            else if theField is "phonetic_last_name"
                delete phonetic last name
            else if theField is "maiden_name"
                delete maiden name
            else if theField is "suffix"
                delete suffix
            else if theField is "job_title"
                delete job title
            else if theField is "department"
                delete department
            else if theField is "organization"
                delete organization
            else if theField is "nickname"
                delete nickname
            else if theField is "home_page"
                delete home_page
            else if theField is "note"
                delete note
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
                -- automatically deleted on save
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
        set { thePersonId, theField } to argv & { 1, 2 }
        deleteField(thePersonId, theField)
    else
        set { thePersonId, theField, theInfoId } to argv & { 1, 2, 3 }
        deleteInfo(thePersonId, theField, theInfoId)
    end

    return
end
