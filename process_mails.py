from email import message
import os
import json
import datetime

from django.db.models import Q

from google_helper import authenticate, build_gmail_service
from app.config import *
from app.models import Email


RULE_DB_NAME_MAPPER = {
    "from": "sender",
    "to": "receiver",
    "subject": "subject",
    "date received": "date",
}


def action_body_builder(actions):
    action_body = {"addLabelIds": [], "removeLabelIds": []}
    for action in actions:
        if action["action"] == "mark as read":
            action_body["removeLabelIds"].append("UNREAD")
        elif action["action"] == "mark as unread":
            action_body["addLabelIds"].append("UNREAD")
        elif action["action"] == "move message":
            action_body["addLabelIds"].append(action["label"])
        else:
            continue

    return action_body


def query_builder(rules):
    or_query = Q()
    filter_query = {}
    exclude_query = {}
    for rule in rules:
        db_column = RULE_DB_NAME_MAPPER[rule["field_name"]]
        value = rule["value"]
        if rule["predicate"] == "contains":
            query_key = "{}__icontains".format(db_column)
            filter_query[query_key] = value
            or_query |= Q(**{query_key: value})
        elif rule["predicate"] == "does not contain":
            query_key = "{}__icontains".format(db_column)
            exclude_query[query_key] = value
            or_query |= ~Q(**{query_key: value})
        elif rule["predicate"] == "equals":
            query_key = db_column
            filter_query[query_key] = value
            or_query |= Q(**{query_key: value})
        elif rule["predicate"] == "does not equal":
            query_key = db_column
            exclude_query[query_key] = value
            or_query |= ~Q(**{query_key: value})
        elif rule["predicate"] == "less than days":
            value = datetime.datetime.now() - datetime.timedelta(days=value)
            query_key = "{}__lt".format(db_column)
            filter_query[query_key] = value
            or_query |= Q(**{query_key: value})
        elif rule["predicate"] == "greater than days":
            value = datetime.datetime.now() - datetime.timedelta(days=value)
            query_key = "{}__gt".format(db_column)
            filter_query[query_key] = value
            or_query |= Q(**{query_key: value})
        elif rule["predicate"] == "less than months":
            value = datetime.datetime.now() - datetime.timedelta(days=value * 60)
            query_key = "{}__lt".format(db_column)
            filter_query[query_key] = value
            or_query |= Q(**{query_key: value})
        elif rule["predicate"] == "greater than months":
            value = datetime.datetime.now() - datetime.timedelta(days=value * 60)
            query_key = "{}__gt".format(db_column)
            filter_query[query_key] = value
            or_query |= Q(**{query_key: value})
        else:
            continue

    return (or_query, filter_query, exclude_query)


def validate_rules():
    # TODO: To be implemented
    with open("rules.json", "r") as rules:
        rules_json = json.loads(rules.read())

    return rules_json


def update_emails(message_ids, actions):
    authenticate()
    service = build_gmail_service()
    body = action_body_builder(actions)

    for message_id in message_ids:
        service.users().messages().modify(
            userId="me", id=message_id, body=body
        ).execute()


def process_rules(rules_json):
    or_query, filter_query, exclude_query = query_builder(rules_json["rules"])
    if rules_json["collective_predicate"] == "all":
        records = Email.objects.filter(**filter_query).exclude(**exclude_query)
    else:
        records = Email.objects.filter(or_query)

    message_ids = records.values_list("message_id", flat=True).distinct()
    update_emails(message_ids, rules_json["actions"])


def main():
    if os.path.exists("rules.json"):
        rules_json = validate_rules()
        process_rules(rules_json)
    else:
        raise ("'rules.json' file not found")


if __name__ == "__main__":
    main()
