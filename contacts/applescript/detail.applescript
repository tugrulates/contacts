-- Returns full contacts with given ids.
--
--   $ osascript brief.applescript [contact_id_1] [contact_id_2] ... [contact_id_N]
--   stdout:
--   {
--     "data": [
--       {
--         "id": "[contact_id_1]",
--         "name": "[name_1]",
--         ...
--         "notes": "[notes_1]"
--       },
--       {
--         "id": "[contact_id_2]",
--         "name": "[name_2]",
--         ...
--         "notes": "[notes_2]"
--       },
--       ...
--       {
--         "id": "[contact_id_N]",
--         "name": "[name_N]",
--         ...
--         "notes": "[notes_N]"
--       }
--     ]
--   }


on findAndReplaceInText(theText, theSearchString, theReplacementString)
    set AppleScript's text item delimiters to theSearchString
    set theTextItems to every text item of theText
    set AppleScript's text item delimiters to theReplacementString
    set theText to theTextItems as string
    set AppleScript's text item delimiters to ""
    return theText
end


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
                set theValue to my findAndReplaceInText(theValue, "\\n", "\\\\n")
                set theValue to my findAndReplaceInText(theValue, "\n", "\\n")
                set theValue to my findAndReplaceInText(theValue, "\"", "\\\"")
                set theValue to "\"" & theValue & "\""
            end if
            return "\"" & theName & "\": " & theValue
        end if
    end tell
end logContactValue


on logContactDate(theName, theDate)
    tell application "Contacts"
        set [theDay, theMonth, theYear] to [day, month, year] of theDate
        if theYear >= 1900
            set theDateStr to "" & theMonth & " " & theDay & ", " & theYear
        else
            set theDateStr to "" & theMonth & " " & theDay
        end if
        return my logContactValue(theName, theDateStr as text)
    end tell
end


on logContactInfo(theName, theInfos, areDates)
    tell application "Contacts"
        if count of theInfos > 0
            set theResults to {}

            repeat with theInfo in theInfos
                set theEntries to {}

                tell theInfo
                    copy my logContactValue("id", id) to the end of theEntries
                    copy my logContactValue("label", label) to the end of theEntries
                    if areDates
                        copy my logContactDate("value", value) to the end of theEntries
                    else
                        copy my logContactValue("value", value) to the end of theEntries
                    end if
                end tell

                copy my encloseList("      {", "          ", theEntries, "        }") to the end of theResults
            end repeat

            return my encloseList("\"" & theName & "\": [", "  ", theResults, "      ]")
        end if
    end tell
end


on logContactAddresses(theContact)
    tell application "Contacts"
        tell theContact
            if count of addresses > 0
                set theResults to {}

                repeat with theAddress in every address
                    set theEntries to {}

                    tell theAddress
                        copy my logContactValue("id", id) to the end of theEntries
                        copy my logContactValue("label", label) to the end of theEntries
                        copy my logContactValue("value", formatted address) to the end of theEntries
                        copy my logContactValue("country_code", country code) to the end of theEntries
                        copy my logContactValue("street", street) to the end of theEntries
                        copy my logContactValue("city", city) to the end of theEntries
                        copy my logContactValue("state", state) to the end of theEntries
                        copy my logContactValue("zip_code", zip) to the end of theEntries
                        copy my logContactValue("country", country) to the end of theEntries
                    end tell

                    copy my encloseList("      {", "          ", theEntries, "        }") to the end of theResults
                end repeat

                return my encloseList("\"addresses\": [", "  ", theResults, "      ]")
            end if
        end tell
    end tell
end


on logContactBirthDate(theContact)
    tell application "Contacts"
        tell theContact
            set theBirthDate to birth date
            if theBirthDate exists
                return my logContactDate("birth_date", theBirthDate)
            end if
        end tell
    end tell
end


on logContactSocialProfiles(theContact)
    tell application "Contacts"
        tell theContact
            if count of social profiles > 0
                set theResults to {}

                repeat with theSocialProfile in every social profile
                    set theEntries to {}

                    tell theSocialProfile
                        copy my logContactValue("id", id) to the end of theEntries
                        copy my logContactValue("label", service name) to the end of theEntries
                        copy my logContactValue("value", user name) to the end of theEntries
                        copy my logContactValue("user_identifier", user identifier) to the end of theEntries
                        copy my logContactValue("url", url of theSocialProfile) to the end of theEntries
                    end tell

                    copy my encloseList("      {", "          ", theEntries, "        }") to the end of theResults
                end repeat

                return my encloseList("\"social_profiles\": [", "  ", theResults, "      ]")
            end if
        end tell
    end tell
end


on logInstantMessages(theContact)
    tell application "Contacts"
        tell theContact
            if count of instant messages > 0
                set theResults to {}

                repeat with theInstantMessage in every instant message
                    set theEntries to {}

                    tell theInstantMessage
                        --- value is missing
                        copy my logContactValue("id", id) to the end of theEntries
                        copy my logContactValue("label", service name) to the end of theEntries
                        copy my logContactValue("value", user name) to the end of theEntries
                    end tell

                    copy my encloseList("      {", "          ", theEntries, "        }") to the end of theResults
                end repeat

                return my encloseList("\"instant_messages\": [", "  ", theResults, "      ]")
            end if
        end tell
    end tell
end


on detailContact(theIds)
    tell application "Contacts"
        set theResults to {}

        repeat with theId in theIds
            set theEntries to {}

            set theContact to person id theId
            set theEntries to {}

            tell theContact
                copy my logContactValue("id", id) to the end of theEntries

                copy my logContactValue("name", name) to the end of theEntries
                copy my logContactValue("has_image", image exists) to the end of theEntries
                copy my logContactValue("is_company", company) to the end of theEntries

                copy my logContactValue("prefix", title) to the end of theEntries
                copy my logContactValue("first_name", first name) to the end of theEntries
                copy my logContactValue("phonetic_first_name", phonetic first name) to the end of theEntries
                copy my logContactValue("middle_name", middle name) to the end of theEntries
                copy my logContactValue("phonetic_middle_name", phonetic middle name) to the end of theEntries
                copy my logContactValue("last_name", last name) to the end of theEntries
                copy my logContactValue("phonetic_last_name", phonetic last name) to the end of theEntries
                copy my logContactValue("maiden_name", maiden name) to the end of theEntries
                copy my logContactValue("suffix", suffix) to the end of theEntries
                copy my logContactValue("nickname", nickname) to the end of theEntries

                copy my logContactValue("job_title", job title) to the end of theEntries
                copy my logContactValue("department", department) to the end of theEntries
                copy my logContactValue("organization", organization) to the end of theEntries

                copy my logContactInfo("phones", every phone, false) to the end of theEntries
                copy my logContactInfo("emails", every email, false) to the end of theEntries
                copy my logContactValue("home_page", home page) to the end of theEntries
                copy my logContactInfo("urls", every url, false) to the end of theEntries

                copy my logContactAddresses(theContact) to the end of theEntries

                copy my logContactBirthDate(theContact) to the end of theEntries
                copy my logContactInfo("custom_dates", custom dates, true) to the end of theEntries

                copy my logContactInfo("related_names", every related names, false) to the end of theEntries

                copy my logContactSocialProfiles(theContact) to the end of theEntries
                copy my logInstantMessages(theContact) to the end of theEntries

                copy my logContactValue("note", note) to the end of theEntries
            end tell

            copy my encloseList(" {", "      ", theEntries, "    }") to the end of theResults
        end repeat

        return my encloseList("{\n  \"data\": [", "   ", theResults, "  ]\n}")
    end tell
end


on run argv
    detailContact(argv)
end
