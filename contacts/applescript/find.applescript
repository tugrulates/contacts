on findAndReplaceInText(theText, theSearchString, theReplacementString)
    set AppleScript's text item delimiters to theSearchString
    set theTextItems to every text item of theText
    set AppleScript's text item delimiters to theReplacementString
    set theText to theTextItems as string
    set AppleScript's text item delimiters to ""
    return theText
end findAndReplaceInText


on findContacts(theKeywords)
    tell application "Contacts"
        set theContacts to {}
        if count of TheKeywords = 0
            set theContacts to people
        else
            repeat with theKeyword in theKeywords
                ignoring diacriticals
                    set found to people where ( ¬
                        id is theKeyword or ¬
                        name is theKeyword or ¬
                        first name is theKeyword or ¬
                        middle name is theKeyword or ¬
                        last name is theKeyword or ¬
                        organization is theKeyword)
                end ignoring
                repeat with theContact in found
                    copy theContact to end of theContacts
                end repeat
            end repeat
        end if
    end tell
    return theContacts
end findContacts


on logContactValue(theOutput, theName, theValue)
    tell application "Contacts"
        if exists theValue
            if class of theValue is text
                set theValue to my findAndReplaceInText(theValue, "\\n", "\\\\n")
                set theValue to my findAndReplaceInText(theValue, "\n", "\\n")
                set theValue to "\"" & theValue & "\""
            end if
            copy "    \"" & theName & "\": " & theValue & "," to the end of theOutput
        end if
    end tell
end logContactValue


on logContactInfo(theOutput, theName, theInfos)
    tell application "Contacts"
        if count of theInfos > 0
            copy "    \"" & theName & "\": [" to the end of theOutput
            repeat with theInfo in theInfos
                copy "    {" to the end of theOutput
                my logContactValue(theOutput, "id", id of theInfo)
                my logContactValue(theOutput, "label", label of theInfo)
                my logContactValue(theOutput, "value", value of theInfo)
                copy "    }," to the end of theOutput
            end repeat
            copy "    ]," to the end of theOutput
        end if
    end tell
end logContactInfo


on logContactAddresses(theOutput, theContact)
    tell application "Contacts"
        set theAddresses to every address of theContact
        if count of theAddresses > 0
            copy "    \"addresses\": [" to the end of theOutput
            repeat with theAddress in every address of theContact
                copy "    {" to the end of theOutput
                my logContactValue(theOutput, "id", id of theAddress)
                my logContactValue(theOutput, "country_code", country code of theAddress)
                my logContactValue(theOutput, "label", label of theAddress)
                my logContactValue(theOutput, "street", street of theAddress)
                my logContactValue(theOutput, "city", city of theAddress)
                my logContactValue(theOutput, "state", state of theAddress)
                my logContactValue(theOutput, "zip", zip of theAddress)
                my logContactValue(theOutput, "country", country of theAddress)
                copy "    }," to the end of theOutput
            end repeat
            copy "    ]," to the end of theOutput
        end if
    end tell
end logContactAddresses


on logContactBirthDate(theOutput, theContact)
    tell application "Contacts"
        set theBirthDate to birth date of theContact
        if theBirthDate exists
            my logContactValue(theOutput, "birth_date", short date string of (theBirthDate))
        end if
    end tell
end logContactBirthDate


on listContacts(theContacts)
    tell application "Contacts"
        set theOutput to {"["}
        repeat with theContact in theContacts
            copy "  {" to the end of theOutput

            my logContactValue(theOutput, "id", id of theContact)

            my logContactValue(theOutput, "name", name of theContact)
            my logContactValue(theOutput, "has_image", image of theContact exists)
            my logContactValue(theOutput, "is_company", company of theContact)

            my logContactValue(theOutput, "nickname", nickname of theContact)
            my logContactValue(theOutput, "first_name", first name of theContact)
            my logContactValue(theOutput, "middle_name", middle name of theContact)
            my logContactValue(theOutput, "last_name", last name of theContact)

            my logContactValue(theOutput, "organization", organization of theContact)
            my logContactValue(theOutput, "job_title", job title of theContact)

            my logContactInfo(theOutput, "phones", every phone of theContact)
            my logContactInfo(theOutput, "emails", every emails of theContact)
            my logContactInfo(theOutput, "urls", every urls of theContact)

            my logContactAddresses(theOutput, theContact)
            my logContactBirthDate(theOutput, theContact)

            copy "  }," to the end of theOutput
        end repeat
        copy "]" to the end of theOutput
        set AppleScript's text item delimiters to "\n"
        return theOutput as text
    end tell
end detailContacts


on run argv
    listContacts(findContacts(argv))
end run
