
import os
import sys
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import argparse

# Define scopes
SCOPES = ['https://www.googleapis.com/auth/drive']
export_mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-fid', '--file_id', required = True, help='id of the google drive file')
    parser.add_argument('-output', '--output_folder', required = True, help='Output folder where file needs to be downloaded')
    parser.add_argument('-sfile', '--service_account_file_path', required = True, help='Path of the service account file')
    args = parser.parse_args()
    return args

def authenticate(service_account_file_path):
    """Authenticate the user and return a Google Drive API service instance."""
    creds = None
 
    creds = service_account.Credentials.from_service_account_file(
        service_account_file_path, scopes=SCOPES)

    return build('drive', 'v3', credentials=creds)


def download_file(service, file_id, output_folder):
    """Download a file from Google Drive given a file ID."""
    try:
        request = service.files().export_media(fileId=file_id, mimeType=export_mime_type)
        fh = io.FileIO(os.path.join(output_folder, file_id), 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")
        print(f"Downloaded file with ID {file_id} to {output_folder}")
    except Exception as e:
        print(f"Failed to download file: {str(e)}")


def main(file_id, output_folder, service_account_file_path):
    if not os.path.exists(output_folder):
        print(f"Output folder {output_folder} does not exist.")
        sys.exit(1)

    service = authenticate(service_account_file_path)
    download_file(service, file_id, output_folder)


if __name__ == "__main__":

    args = parse_arguments()
    file_id = args.file_id
    output_folder = args.output_folder
    service_account_file_path = args.service_account_file_path
    main(file_id, output_folder, service_account_file_path)