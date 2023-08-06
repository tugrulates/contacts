on findContacts(theKeywords)
    tell application "Contacts"
        if count of theKeywords = 0
            repeat with theContact in people
                log id of the theContact as text
            end repeat
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
                    log id of the theContact as text
                end repeat
            end repeat
        end if
    end tell
end findContacts

on run argv
    findContacts(argv)
end run
