import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools


SLIDESHOW_FOLDER = 'Front Display Slideshow'

SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

def get_credentials():
	credential_dir = os.path.join(os.curdir, 'credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir, 'drive-quickstart.json')

	store = oauth2client.file.Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME

		credentials = tools.run_flow(flow, store, None)
	return credentials

def main():
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('drive', 'v3', http=http)

	results = service.files().list(
		q="mimeType = 'application/vnd.google-apps.folder' and name = '{0}'".format(SLIDESHOW_FOLDER),
		fields="files(id)").execute()
	folder = results.get('files', [])
	
	slideshow_id = None
	if folder:
		slideshow_id = folder[0]['id']
	else:
		raise Exception('Folder "{0}" does not exist'.format(SLIDESHOW_FOLDER))

	results = service.files().list(q="'{0}' in parents".format(slideshow_id), fields="files(name, webContentLink)").execute()
	images = results.get('files', [])
	for image in images:
		print("{0} @ {1}".format(image['name'], image['webContentLink']))
		


if __name__ == '__main__':
	main()
