-- Adds contact info with given label and value.
--
--   $ osascript add.applescript [contact_id] phones label [label] value [phone]
--   $ osascript add.applescript [contact_id] emails label [label] value [email]
--   $ osascript add.applescript [contact_id] urls label [label] value [url]
--   $ osascript add.applescript [contact_id] addresses label [label] ([field] [value])...
--   $ osascript add.applescript [contact_id] social_profiles label [service] value [user] url [url]


on addInfo(thePersonId, theField, theArgs)
    tell application "Contacts"
        set theProperties to { label: null, value: null }
        repeat with i from 1 to (count of theArgs) by 2
            set { theKey, theValue } to { item i of theArgs, item (i + 1) of theArgs }
            if theKey is "label"
                set the label of theProperties to theValue
            else if theKey is "value"
                set the value of theProperties to theValue
            end if
        end repeat

        tell person id thePersonId
            if theField is "phones"
                make new phone at end of phones with properties theProperties
            else if theField is "emails"
                make new email at end of emails with properties theProperties
            else if theField is "urls"
                make new url at end of urls with properties theProperties
            else
                error "Cannot add " & theField
            end if
        end tell

        save()
    end tell
end


on addAddress(thePersonId, theArgs)
    tell application "Contacts"
        tell person id thePersonId
            tell make new address at end of addresses
                repeat with i from 1 to (count of theArgs) by 2
                    set { theKey, theValue } to { item i of theArgs, item (i + 1) of theArgs }
                    if theKey is "label"
                        set the label to theValue
                    else if theKey is "street"
                        set the street to theValue
                    else if theKey is "city"
                        set the city to theValue
                    else if theKey is "zip_code"
                        set the zip to theValue
                    else if theKey is "country"
                        set the country to theValue
                    else if theKey is "country_code"
                        set the country code to theValue
                    end if
                end repeat
            end tell
        end tell

        save()
    end tell
end


on addSocialProfile(thePersonId, theArgs)
    tell application "Contacts"
        tell person id thePersonId
            set theSocialProfile to make new social profile at end of social profiles

            repeat with i from 1 to (count of theArgs) by 2
                set { theKey, theValue } to { item i of theArgs, item (i + 1) of theArgs }
                if theKey is "label"
                    set the service name of theSocialProfile to theValue
                else if theKey is "value"
                    set the user name of theSocialProfile to theValue
                else if theKey is "user_identifier"
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
    set { thePersonId, theField, theArgs } to {  Â
        item 1 of argv,                          Â
        item 2 of argv,                          Â
        items 3 thru (count of argv) of argv     Â
    }

    if theField is "addresses"
        addAddress(thePersonId, theArgs)
    else if theField is "social_profiles"
        addSocialProfile(thePersonId, theArgs)
    else
        addInfo(thePersonId, theField, theArgs)
    end if

    return
end
