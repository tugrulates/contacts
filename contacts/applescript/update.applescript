-- Updates contact field with given value.
--
--   $ osascript update.applescript [contact_id] prefix [prefix]
--   $ osascript update.applescript [contact_id] first_name [first_name]
--   $ osascript update.applescript [contact_id] middle_name [middle_name]
--   $ osascript update.applescript [contact_id] last_name [prelast_namefix]
--   $ osascript update.applescript [contact_id] maiden_name [maiden_name]
--   $ osascript update.applescript [contact_id] suffix [suffix]
--   $ osascript update.applescript [contact_id] nickname [nickname]
--   $ osascript update.applescript [contact_id] phones [phone_id] {label [label]} {value [phone]}
--   $ osascript update.applescript [contact_id] emails [email_id] {label [label]} {value [email]}
--   $ osascript update.applescript [contact_id] urls [url_id] {label [label]} {value [url]}
--   $ osascript update.applescript [contact_id] addresses [address_id] ([field] [value])...
--   $ osascript update.applescript [contact_id] custom_dates [custom_date_id] {label [label]} {value [date]}
--   $ osascript update.applescript [contact_id] social_profiles [social_profile_id] {label [service]} {value [user]} {url [url]}


on updateField(thePersonId, theField, theValue)
    tell application "Contacts"
        tell person id thePersonId
            if theField is "prefix"
                set prefix to theValue
            else if theField is "first_name"
                set first name to theValue
            else if theField is "phonetic_first_name"
                set phonetic first name to theValue
            else if theField is "middle_name"
                set middle name to theValue
            else if theField is "phonetic_middle_name"
                set phonetic middle name to theValue
            else if theField is "last_name"
                set last name to theValue
            else if theField is "phonetic_last_name"
                set phonetic last name to theValue
            else if theField is "maiden_name"
                set maiden name to theValue
            else if theField is "suffix"
                set suffix to theValue
            else if theField is "job_title"
                set job title to theValue
            else if theField is "department"
                set department to theValue
            else if theField is "organization"
                set organization to theValue
            else if theField is "nickname"
                set nickname to theValue
            else if theField is "home_page"
                set home_page to theValue
            else if theField is "note"
                set note to theValue
            else
                error "Cannot update " & theField
            end if
        end tell
        save()
    end tell
end


on updateInfo(thePersonId, theField, theInfoId, theArgs)
    tell application "Contacts"
        tell person id thePersonId
            if theField is "phones"
                set theInfo to phone id theInfoId
            else if theField is "emails"
                set theInfo to email id theInfoId
            else if theField is "urls"
                set theInfo to url id theInfoId
            else if theField is "addresses"
                set theInfo to address id theInfoId
            else if theField is "custom_dates"
                set theInfo to custom date id theInfoId
            else
                error "Cannot update " & theField
            end if

            tell theInfo
                repeat with i from 1 to (count of theArgs) by 2
                    set { theKey, theValue } to { item i of theArgs, item (i + 1) of theArgs }
                    if theKey is "label"
                        set the label to theValue
                    else if theKey is "value"
                        set the value to theValue
                    end if
                end repeat
            end tell
        end tell

        save()
    end tell
end


on updateAddress(thePersonId, theAddressId, theArgs)
    tell application "Contacts"
        tell person id thePersonId
            set theAddress to the address id theAddressId

            tell theAddressId
                repeat with i from 1 to (count of theArgs) by 2
                    set { theKey, theValue } to { item i of theArgs, item (i + 1) of theArgs }
                    if theKey is "label"
                        set the label to theValue
                    else if theKey is "street"
                        set the street of theAddress to theValue
                    else if theKey is "city"
                        set the city of theAddress to theValue
                    else if theKey is "zip_code"
                        set the zip of theAddress to theValue
                    else if theKey is "country"
                        set the country of theAddress to theValue
                    else if theKey is "country_code"
                        set the country code of theAddress to theValue
                    end if
                end repeat
            end tell
        end tell

        save()
    end tell
end


on updateSocialProfile(thePersonId, theSocialProfileId, theArgs)
    tell application "Contacts"
        tell person id thePersonId
            set theSocialProfile to the social profile id theSocialProfileId

            repeat with i from 1 to (count of theArgs) by 2
                set { theKey, theValue } to { item i of theArgs, item (i + 1) of theArgs }
                if theKey is "label"
                    set the label of theSocialProfile to theValue
                else if theKey is "value"
                    set the user name of theSocialProfile to theValue
                else if theKey is "user identifier"
                    set the user identifier of theSocialProfile to theValue
                else if theKey is "url"
                    set the url of theSocialProfile to theValue
                end if
            end repeat
        end tell

        save()
    end tell
end


on run argv
    if count of argv > 3
        set { thePersonId, theField, theInfoId, theArgs } to {  Â
            item 1 of argv,                          Â
            item 2 of argv,                          Â
            item 3 of argv,                          Â
            items 4 thru (count of argv) of argv     Â
        }
        if theField is "addresses"
            updateAddress(thePersonId, theInfoId, theArgs)
        else if theField is "social_profiles"
            updateSocialProfile(thePersonId, theInfoId, theArgs)
        else
            updateInfo(thePersonId, theField, theInfoId, theArgs)
        end if
    else
        set { thePersonId, theField, theValue } to argv & { 1, 2, 3 }
        updateField(thePersonId, theField, theValue)
    end if

    return
end
