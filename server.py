import httplib2
import os

import schedule
import time
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

from flask import Flask, render_template
app = Flask(__name__)


SLIDESHOW_FOLDER = 'Front Display Slideshow'

SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

urls = []


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

def get_images():
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
	return results.get('files', [])


def update_urls():
	global urls
	urls = []
	for i in get_images():
		print(i['name'] + " " + i['webContentLink'])
		urls.append(i['webContentLink'].replace("export=download",""))
	print("read " + str(len(urls)) + " images")

@app.route("/")
def display():
	return render_template('client.html', images=urls)

if __name__ == "__main__":
	# save pid to file for easy killing
	pid_file = open("server_pid", "w")
	pid_file.write(str(os.getpid()))
	pid_file.close()

	update_urls()
	app.run(host='0.0.0.0')
	schedule.every(6).hour.do(update_urls)
	
