from decouple import Config, AutoConfig
from azure.storage.blob import BlobServiceClient
import datetime
from flask import Flask, render_template, url_for
from services.blob_service import BlobService

config = AutoConfig()
key = config('azure_storage_key')
name = config('azure_storage_name')
blob_service  =  BlobService(name, key, "test")
blob_list = blob_service.list_files_in_blob("sss")
blob_list_url = []
for blob in blob_list:
    blob_list_url.append(blob_service.get_blob_sas_url(blob))

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/photos')
def photos():
    photos = blob_list_url[:30]
    folders = ["Engagement","Sangeet","Reception", "Marriage","Mugurtham", "Reception"]
    return render_template('photo_viewer.html',photos = photos, folders=folders)

if __name__ == '__main__':
    app.run(debug=True)
