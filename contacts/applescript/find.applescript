on findContacts(theKeywords, shouldLog)
    tell application "Contacts"
        if count of theKeywords = 0
            if shouldLog
                repeat with theContact in people
                    log id of the theContact as text
                end repeat
            end if
            return count of people
        else
            set theIds to {}
            repeat with theKeyword in theKeywords
                ignoring diacriticals
                set theFound to id of people whose ( ¬
                    id is theKeyword or ¬
                    name is theKeyword or ¬
                    first name is theKeyword or ¬
                    middle name is theKeyword or ¬
                    last name is theKeyword or ¬
                    nickname is theKeyword or ¬
                    organization contains theKeyword or ¬
                    job title contains theKeyword or ¬
                    organization is theKeyword or ¬
                    job title is theKeyword or ¬
                    city of addresses contains theKeyword or ¬
                    country of addresses contains theKeyword)
                end ignoring
                repeat with theId in theFound
                    if theId as text is not in theIds
                        if shouldLog
                            log theId as text
                        end if
                        copy theId as text to the end of theIds
                    end if
                end repeat
            end repeat
            return count of theIds
        end if
    end tell
end


on run argv
    set argc to count of argv
    if argc is greater than 0 and item 1 of argv is "?"
        if argc is 1
            set theKeywords to {}
        else
            set theKeywords to items 2 thru (count of argv) of argv
        end if
        set shouldLog to false
    else
        set theKeywords to argv
        set shouldLog to true
    end if
    return findContacts(theKeywords, shouldLog)
end
