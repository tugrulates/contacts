on findAndReplaceInText(theText, theSearchString, theReplacementString)
    set AppleScript's text item delimiters to theSearchString
    set theTextItems to every text item of theText
    set AppleScript's text item delimiters to theReplacementString
    set theText to theTextItems as string
    set AppleScript's text item delimiters to ""
    return theText
end findAndReplaceInText


on encloseList(theOpening, theIndent, theList, theClosing)
    set theInner to {}
    repeat with theLine in theList
        if class of theLine is text
            copy theIndent & theLine as text to the end of theInner
        end if
    end repeat
    if count of theInner = 0
        return theOpening & "\n" & theClosing
    else
        set AppleScript's text item delimiters to ",\n"
        set theInner to theInner as text
        set AppleScript's text item delimiters to ""
        return theOpening & "\n" & theInner & "\n" & theClosing
    end if
end encloseList


on findContacts(theKeywords)
    tell application "Contacts"
        set theContacts to {}
        if count of theKeywords = 0
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


on logContactValue(theName, theValue)
    tell application "Contacts"
        if exists theValue
            if class of theValue is text
                set theValue to my findAndReplaceInText(theValue, "\\n", "\\\\n")
                set theValue to my findAndReplaceInText(theValue, "\n", "\\n")
                set theValue to "\"" & theValue & "\""
            end if
            return "\"" & theName & "\": " & theValue
        end if
    end tell
end logContactValue


on logContactInfo(theName, theInfos)
    tell application "Contacts"
        if count of theInfos > 0
            set theResults to {}

            repeat with theInfo in theInfos
                set theEntries to {}

                copy my logContactValue("id", id of theInfo) to the end of theEntries
                copy my logContactValue("label", label of theInfo) to the end of theEntries
                copy my logContactValue("value", value of theInfo) to the end of theEntries

                copy my encloseList("    {", "        ", theEntries, "      }") to the end of theResults
            end repeat

            return my encloseList("\"" & theName & "\": [", "  ", theResults, "    ]")
        end if
    end tell
end logContactInfo


on logContactAddresses(theContact)
    tell application "Contacts"
        set theAddresses to every address of theContact
        if count of theAddresses > 0
            set theResults to {}

            repeat with theAddress in every address of theContact
                set theEntries to {}

                copy my logContactValue("id", id of theAddress) to the end of theEntries
                copy my logContactValue("country_code", country code of theAddress) to the end of theEntries
                copy my logContactValue("label", label of theAddress) to the end of theEntries
                copy my logContactValue("street", street of theAddress) to the end of theEntries
                copy my logContactValue("city", city of theAddress) to the end of theEntries
                copy my logContactValue("state", state of theAddress) to the end of theEntries
                copy my logContactValue("zip", zip of theAddress) to the end of theEntries
                copy my logContactValue("country", country of theAddress) to the end of theEntries

                copy my encloseList("    {", "        ", theEntries, "      }") to the end of theResults
            end repeat

            return my encloseList("\"addresses\": [", "  ", theResults, "    ]")
        end if
    end tell
end logContactAddresses


on logContactBirthDate(theContact)
    tell application "Contacts"
        set theBirthDate to birth date of theContact
        if theBirthDate exists
            return my logContactValue("birth_date", short date string of (theBirthDate))
        end if
    end tell
end logContactBirthDate


on detailContact(theId)
    tell application "Contacts"
        set theContact to person id theId
        set theEntries to {}

        copy my logContactValue("id", id of theContact) to the end of theEntries

        copy my logContactValue("name", name of theContact) to the end of theEntries
        copy my logContactValue("has_image", image of theContact exists) to the end of theEntries
        copy my logContactValue("is_company", company of theContact) to the end of theEntries

        copy my logContactValue("nickname", nickname of theContact) to the end of theEntries
        copy my logContactValue("first_name", first name of theContact) to the end of theEntries
        copy my logContactValue("middle_name", middle name of theContact) to the end of theEntries
        copy my logContactValue("last_name", last name of theContact) to the end of theEntries

        copy my logContactValue("organization", organization of theContact) to the end of theEntries
        copy my logContactValue("job_title", job title of theContact) to the end of theEntries

        copy my logContactInfo("phones", every phone of theContact) to the end of theEntries
        copy my logContactInfo("emails", every emails of theContact) to the end of theEntries
        copy my logContactInfo("urls", every urls of theContact) to the end of theEntries

        copy my logContactAddresses(theContact) to the end of theEntries
        copy my logContactBirthDate(theContact) to the end of theEntries

        return my encloseList("{", "    ", theEntries, "  }")
    end tell
end detailContact


on run argv
    detailContact(argv)
end run
