from django.core.files.storage import Storage
from django.conf import settings
from supabase import create_client
from io import BytesIO

# class SupabaseStorage(Storage):
#     def __init__(self, bucket_name='media'):
#         self.bucket_name = bucket_name
#         self.supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
#         self.storage_client = self.supabase.storage.from_(self.bucket_name)

#     def _open(self, name, mode='rb'):
#         response = self.storage_client.download(name)
#         if response.status_code == 200:
#             return BytesIO(response.content)
#         else:
#             raise FileNotFoundError(f"File {name} not found in Supabase Storage.")

#     def _save(self, name, content):
#         content.seek(0)
#         data = content.read()
#         content_type = getattr(content, 'content_type', 'application/octet-stream')
        
#         response = self.storage_client.upload(
#             path=name,
#             file=data,
#             headers={'content-type': content_type},
#             options={'upsert': 'true'}  # Some clients require string values
#         )
        
#         if response.get('error'):
#             raise Exception(f"Failed to upload {name}: {response['error']['message']}")
#         return name



#     def exists(self, name):
#         # Extract folder path from name
#         folder = '/'.join(name.split('/')[:-1]) or ''
#         # List files in the folder
#         files = self.storage_client.list(path=folder)
#         # files is a list of dicts with 'name' keys
#         filename = name.split('/')[-1]
#         return any(file['name'] == filename for file in files)

#     def url(self, name):
#         # Public URL format for Supabase Storage
#         return f"{settings.SUPABASE_URL}/storage/v1/object/public/{self.bucket_name}/{name}"

class SupabaseStorage(Storage):
    def __init__(self, bucket_name='media'):
        self.bucket_name = bucket_name
        self.supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        self.storage_client = self.supabase.storage.from_(self.bucket_name)

    def _open(self, name, mode='rb'):
        response = self.storage_client.download(name)
        if not response.get('error'):
            return BytesIO(response.data)
        else:
            raise FileNotFoundError(f"File {name} not found in Supabase Storage.")

    def _save(self, name, content):
            content.seek(0)
            data = content.read()
            content_type = getattr(content, 'content_type', 'application/octet-stream')
            response = self.storage_client.upload(
                path=name,
                file=data,
                file_options={'content-type': content_type, 'upsert': True}
            )
            # Basic success check
            if response.status_code != 200:
                raise Exception(f"Failed to upload {name} to Supabase Storage.")
            return name

# New update method to replace existing files
    def update(self, name, content):
        content.seek(0)
        data = content.read()
        content_type = getattr(content, 'content_type', 'application/octet-stream')
        response = self.storage_client.update(
            path=name,
            file=data,
            file_options={'content-type': content_type, 'upsert': False}  # upsert False means replace only
        )
        if hasattr(response, 'status_code') and response.status_code != 200:
            raise Exception(f"Failed to update {name}: HTTP {response.status_code}")
        if not getattr(response, 'data', None):
            raise Exception(f"Failed to update {name}: no data returned")
        return name


    def exists(self, name):
        folder = '/'.join(name.split('/')[:-1]) or ''
        files = self.storage_client.list(folder)
        filename = name.split('/')[-1]
        return any(file['name'] == filename for file in files)

    def url(self, name):
        return f"{settings.SUPABASE_URL}/storage/v1/object/public/{self.bucket_name}/{name}"
