import os
import email
from email.policy import default


def parse_raw_email(raw_email):
    parsed_email = email.message_from_string(raw_email, policy=default)
    subject = str(parsed_email["subject"]) or ""
    body = parsed_email.get_body(preferencelist=("plain", "html")).get_content()

    from_email = str(parsed_email["from"]) or ""
    to_emails = str(parsed_email["to"]) or ""

    # Split comma-separated email addresses in the 'to' field if necessary
    if to_emails:
        to_emails = [addr.strip() for addr in to_emails.split(",")]

    cc_emails = str(parsed_email["cc"]) or ""
    bcc_emails = str(parsed_email["bcc"]) or ""
    date = str(parsed_email["date"]) or ""
    message_id = str(parsed_email["message-id"]) or ""

    return {"subject": subject,
            "body": body,
            "from": from_email,
            "to": to_emails,
            "cc": cc_emails,
            "bcc": bcc_emails,
            "date": date,
            "message_id": message_id}

def get_emails_from_directory(directory):
    emails = []

    count = 0

    for root, _, files in os.walk(directory):

        for file in files:
            count += 1

            if count % 1000 == 0:
                print(count)

            if file.lower().endswith("."):
                with open(os.path.join(root, file), "r", encoding="latin1") as f:
                    raw_email = f.read()
                    try:
                        emails.append(parse_raw_email(raw_email))
                    except:
                        print('ERROR RUNNING PARSE RAW EMAIL')

    print(f"Loaded {len(emails)} emails from the Enron dataset.")

    return emails

def load_emails_from_json(filepath):

    with open(filepath, 'r') as f:
        emails = json.load(f)

    print("Emails loaded")

    return emails

def save_emails_to_json(emails, filepath):
    # Save the combined data to a JSON file

    with open(filepath, 'w') as f:
        json.dump(emails, f)

    print(f"Emails saved to {filepath}.json.")

