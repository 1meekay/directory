# directory
Password-protected directory with the options to add, change, delete, find, and view contacts stored in a sqlite database.. also send SMS through Twilio API, and set and change password

1-- 10:47am 1/11/18 editing readme and adding python code files to directory fold.. ready to push to github

contactDirectory.db   -- database file to store contacts
directory.py          -- main python file, heart of program
directoryClass.py     -- driver, contains contacts class and sqlite3 connection
sendSMS.py            -- for sending SMS messages, contains Twilio API import and a send function
twiliocredentials.py  -- contains account SID, authToken, and recovery code for Twilio account
vault_pass.txt        -- contains password of vault

Message to viewer:

Due to my hiding of the Twilio credentials, the SMS function inside of my program will not work unless you create your own.
