# directory
Password-protected directory with the options to add, change, delete, find, and view contacts stored in a sqlite database.. also send SMS through Twilio API, and set and change password

also features a pandas DataFrame to represent the contacts database

================================================================

contactDirectory.db   -- database file to store contacts

directory.py          -- main python file, heart of program

directoryClass.py     -- foundation, contains Contacts class and sqlite3 connection

sendSMS.py            -- for sending SMS messages, contains Twilio API import and a send function

twiliocredentials.py  -- contains account SID, authToken, and recovery code for Twilio account

vault_pass.txt        -- contains password of vault

================================================================

Message to viewer:

1) Should you choose to run the program, be sure to uncomment out the first_run() function at the end of the program.

2) Due to my hiding of the Twilio credentials, the SMS function inside of my program will not work unless you create your own.

================================================================

update 1/17
    -- updated to check if program is running for the first time
    -- added:

        if __name__ == '__main__':
          start()


    -- use pickle for reading file name input
