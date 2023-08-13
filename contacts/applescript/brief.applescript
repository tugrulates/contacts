-- Returns minimal contacts with given ids.
--
--   $ osascript brief.applescript [contact_id_1] [contact_id_2] ... [contact_id_N]
--   stdout:
--   [
--     { "id": "[contact_id_1]", "name": "[name_1]", "company": [company_1] },
--     { "id": "[contact_id_1]", "name": "[name_2]", "company": [company_2] },
--     ...
--     { "id": "[contact_id_N]", "name": "[name_N]", "company": [company_N] }
--   ]


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
end


on logContactValue(theName, theValue)
    tell application "Contacts"
        if exists theValue
            if class of theValue is text
                set theValue to "\"" & theValue & "\""
            end if
            return "\"" & theName & "\": " & theValue
        end if
    end tell
end logContactValue


on detailContact(theIds)
    tell application "Contacts"
        set theResults to {}

        repeat with theId in theIds
            set theEntries to {}

            set theContact to person id theId
            set theName to name of theContact
            set theCompany to company of theContact
            set theEntry to " { \"id\": \"" & theId & "\", \"name\": \"" & theName & "\", \"company\": " & theCompany & " }"

            copy theEntry to the end of theResults
        end repeat

        return my encloseList("[", " ", theResults, "]")
    end tell
end


on run argv
    detailContact(argv)
end
