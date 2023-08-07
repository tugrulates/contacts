on findContacts(theKeywords)
    tell application "Contacts"
        if count of theKeywords = 0
            repeat with theContact in people
                log id of the theContact as text
            end repeat
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
                    organization contains theKeyword or ¬
                    job title contains theKeyword or ¬
                    city of addresses contains theKeyword or ¬
                    country of addresses contains theKeyword)
                end ignoring
                repeat with theId in theFound
                    if theId as text is not in theIds
                        log theId as text
                        copy theId as text to the end of theIds
                    end if
                end repeat
            end repeat
        end if
    end tell
end findContacts


on run argv
    findContacts(argv)
    return
end run
