import utils
from apiclient import errors

def list():

    cred = utils.get_cred()

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])

def delete_by_email_sender(email_sender):

    user_id = "me"

    service = utils.get_service()

    messagens = list_messages_by_email_sender(service, email_sender, user_id)

    for msg in messagens:
        delete_message_by_id(service, user_id, msg['id'], email_sender)

def list_messages_by_email_sender(service, email_sender, user_id):

    query = "from:{}".format(email_sender)

    try:
        response = service.users().messages().list(userId=user_id,q=query).execute()
        
        messages = []
        
        if 'messages' in response:
            messages.extend(response['messages'])
        else:
            print("No result: {}".format(email_sender))
            
        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query,pageToken=page_token).execute()
            if response and response['resultSizeEstimate']>0:
                messages.extend(response['messages'])

        return messages
    
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

def delete_message_by_id(service, user_id, msg_id, email_sender):
    
    try:
        service.users().messages().delete(userId=user_id, id=msg_id).execute()
        print('{} Message with id: {} deleted successfully.'.format(email_sender, msg_id))
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

if __name__ == '__main__':

    #Email sender
    email_sender = "@xxx.xxx"
    delete_by_email_sender(email_sender)
