from google.cloud import language_v1
from google.cloud.language_v1 import enums
from google.oauth2 import service_account
import random as r
import SpamCloggerMessageResponses as inputs

credentials = service_account.Credentials.from_service_account_file("spamclogger-5dd55ad0a65c.json")

scam = {}
scam["body"] = "Hello Dear,how are you doing.Its my pleasure to contact you for a long term relationship.I was just surfing through the Internet when i found your email address." \
               "I want to make a new and special friend.\
Lets keep in touch and get to know more about each other and see what happens in future.\
My name is Tracy William,I am from the United States of America,but presently live and work in England.\
Pls reply to my personal email(tracymedicinemed3@yahoo.com)\
I will send my details and pictures as soon as i hear from you bye Tracy"

BASE_MESSAGE = "{} {}, \n\n I am {} to accept your {}. How do we {}? I have hopes for its success. What information exactly do you need me to {} ?.\n\n {}, \n {} {}"


def transpose_letter(string):
        tokens = string.split()
        token_pos = r.choice(range(len(tokens)))
        positions = r.sample(range(len(tokens[token_pos])), 2)
        l = list(tokens[token_pos])
        for first, second in zip(positions[::2], positions[1::2]):
            l[first], l[second] = l[second], l[first]
        tokens[token_pos] = ''.join(l)
        return ' '.join(tokens)


def remove_random_letter(string, number=3):
    counter = 0
    while counter < 2:
        index = r.randint(0, len(string) - 1)
        string = string[:index] + string[index + 1:]
        counter = counter + 1
    return string

def generate_message(scam):
    client = language_v1.LanguageServiceClient(credentials=credentials)
    type_ = enums.Document.Type.HTML
    document = {"content": scam, "type": type_}
    encoding_type = enums.EncodingType.UTF8
    response = client.analyze_entities(document, encoding_type=encoding_type)
    scammer_name = []
    for entity in response.entities:
        if enums.Entity.Type(entity.type).name == "PERSON":
            scammer_name.append(entity.name)

    if(len(scammer_name) < 1):
        scammer_name.append("Friend")

    message = BASE_MESSAGE.format(r.choice(inputs.SYNONYMS_OF_HI).capitalize(), r.choice(scammer_name),
                               r.choice(inputs.SYNONYMS_OF_PLEASED), r.choice(inputs.SYNONYMS_OF_PROPOSAL),
                               r.choice(inputs.SYNONYMS_Of_PROCEED), r.choice(inputs.SYNONYMS_Of_PROVIDE),
                               r.choice(inputs.SYNONYMS_Of_REGARDS), r.choice(inputs.LIST_OF_FIRST_NAMES),
                               r.choice(inputs.LIST_OF_LAST_NAMES))
    message = remove_random_letter(message)
    return message