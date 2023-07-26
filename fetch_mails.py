import base64
import json

from datetime import datetime
from googleapiclient.errors import HttpError

from google_helper import authenticate, build_gmail_service
from app.config import *
from app.models import Email


def purge_db():
    Email.objects.all().delete()


def decode_data(data):
    return base64.b64decode(data.replace("-", "+").replace("_", "/"))


def process_and_save_email(email_json, payload):
    if payload.get("parts", None):
        for part in payload.get("parts"):
            process_and_save_email(email_json, part)
    elif payload["body"].get("data", None):
        email_json["body"] = decode_data(payload["body"]["data"])
        Email.objects.create(**email_json)
    else:
        return


def fetch_and_save_emails():
    try:
        service = build_gmail_service()
        result = service.users().messages().list(maxResults=100, userId="me").execute()
        messages = result.get("messages")

        print("Fetching emails: ", end=" ", flush=True)
        for i, msg in enumerate(messages):
            print(i, end=", ", flush=True)
            txt = service.users().messages().get(userId="me", id=msg["id"]).execute()
            email_json = {"message_id": msg["id"]}

            payload = txt["payload"]
            headers = payload["headers"]

            for header in headers:
                if header["name"] == "Subject":
                    email_json["subject"] = header["value"]
                elif header["name"] == "From":
                    email_json["sender"] = header["value"]
                elif header["name"] == "To":
                    email_json["receiver"] = header["value"]
                elif header["name"] == "Date":
                    date_string = (
                        header["value"].split(",")[1].replace("(UTC)", "").strip()
                    )
                    email_json["date"] = datetime.strptime(
                        date_string, "%d %b %Y %H:%M:%S %z"
                    )

            process_and_save_email(email_json, payload)
    except HttpError as error:
        print(f"An error occurred: {error}")


def main():
    purge_db()
    authenticate()
    fetch_and_save_emails()


if __name__ == "__main__":
    main()
