from django.core.files.storage import Storage
from django.conf import settings
from supabase import create_client
from io import BytesIO

class SupabaseStorage(Storage):
    def __init__(self, bucket_name='media'):
        self.bucket_name = bucket_name
        self.supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        self.storage_client = self.supabase.storage.from_(self.bucket_name)

    def _open(self, name, mode='rb'):
        response = self.storage_client.download(name)
        if response.status_code == 200:
            return BytesIO(response.content)
        else:
            raise FileNotFoundError(f"File {name} not found in Supabase Storage.")

    def _save(self, name, content):
        content.seek(0)
        data = content.read()
        response = self.storage_client.upload(name, data, {'content-type': content.content_type})
        if response.status_code != 200:
            raise Exception(f"Failed to upload {name} to Supabase Storage.")
        return name

    def exists(self, name):
        response = self.storage_client.list(path=name)
        return len(response.data) > 0 if response.status_code == 200 else False

    def url(self, name):
        # Public URL format for Supabase Storage
        return f"{settings.SUPABASE_URL}/storage/v1/object/public/{self.bucket_name}/{name}"
