# Assignment

This project does two things:
1. Authorize & fetch emails from your gmail account along with saving it to a database. This is done by running the `fetch_emails.py` script.
2. Process the saved emails based on the "rules" defined in a `rules.json` file that queries the db and performs the "action" defined therewithin on the resulting records. This is done by running the `process_emails.py` script.

The project uses Django's ORM capability for everything related to databases.

## Setting up

1. Clone the repository.
`git clone git@github.com:harisibrahimkv/assignment.git`

2. Create and activate a virtualenv. Insall requirements.
`pip install -r requirements.txt`

3. Follow https://developers.google.com/docs/api/quickstart/python#set_up_your_environment until the step where you download the `credentials.json` file.

4. Run the migrations to create the database and tables.
`python -m manage migrate app`

This will create an `emails.db` file in your root folder.

## Execution

1. Fetching Emails:

Once you're done setting up, run the following to fetch emails from your gmail inbox

`python3 fetch_mails.py`

The default has been hardcoded to fetch 100 messages. Feel free to refer to https://developers.google.com/gmail/api/reference/rest/v1/users.messages/list and set the maxResults value. 

If you are running the script for the first time, it will open a gmail page on the browser asking you to sign in and grant specific permissions. Once you've successfully done that, feel free to close the browser tab. If the authorization was successful, this will have generated a `token.json` file in the project root and started fetching emails.

2. Processing Emails:

Once you're done fetching emails and saving them in the db, feel free to tinker around with the `rules.json` file. In order to process the rules and actions defined in the `rules.json` file, run the following in order to process the email within the database accordingly and use the Gmail REST API to perform that actions you defined:

`python3 process_mails.py`

You should be able to see changes in your inbox

## Obvious problems

1. The DB schema

The `Email` table is extremely simple and *only* stores what is needed for the assignment and its queries. In a real world scenario where different kinds of queries can be expected, a lot more info of the email as well as better schema structure that supports Foreign Key relations should be used.

2. Hardcoding 100 emails to be fetched

This should be controlled with an environment variable.

3. Lack of clarity on email threads and parts

The Gmail API returns information on threads as well as parts. This project simply stores each part as a new row and doesn't maintain and information related to threads

4. Lack of validation for the rules.json file

Ideally, since the `rules.json` file is modified by the user, the script should validate that the structure and expected keys as well their values are defined properly. That is skipped.

5. Edge cases around date and certain field values

There will be bugs around date queries related to beginning or end of day and probably timezones as well. The field values in the db doesn't have any serialization and hence no validations around where a proper email is what is being saved or not both in `sender` & `receiver` fields

6. Not using the `bulkModify` endpoint that Gmail API offers.

Instead of looping through each message_id and making a `modify` API call, we can use the `bulkModify` endpoint that Gmail offers.

7. Tests