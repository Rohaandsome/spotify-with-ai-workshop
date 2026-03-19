from azure.data.tables import TableServiceClient, TableEntity
from datetime import datetime
import os
import uuid

class TableStorageClient:
    def __init__(self):
        connection_string = os.getenv("AZURE_BLOB_STORAGE_CONNECTION_STRING")
        self.table_service_client = TableServiceClient.from_connection_string(connection_string)
        self.table_name = "GeneratedCovers"
        self._ensure_table_exists()
    
    def _ensure_table_exists(self):
        """Create table if it doesn't exist"""
        try:
            self.table_service_client.create_table_if_not_exists(self.table_name)
        except Exception as e:
            print(f"ERROR creating table: {type(e).__name__}: {str(e)}")
    
    def save_generation_record(self, playlist_id: str, playlist_name: str, 
                               blob_url: str, prompt: str) -> bool:
        """
        Save a record of a generated cover image
        
        Table schema:
        - PartitionKey: playlist_id
        - RowKey: unique generation ID
        - PlaylistName: name of the playlist
        - BlobUrl: URL to the image in blob storage
        - Prompt: the prompt used to generate the image
        - Timestamp: when it was generated
        """
        try:
            table_client = self.table_service_client.get_table_client(self.table_name)
            
            entity = {
                "PartitionKey": playlist_id,
                "RowKey": str(uuid.uuid4()),
                "PlaylistName": playlist_name,
                "BlobUrl": blob_url,
                "Prompt": prompt[:1000],  # Truncate if too long
                "GeneratedAt": datetime.utcnow().isoformat()
            }
            
            table_client.create_entity(entity=entity)
            print(f"Saved generation record for playlist: {playlist_id}")
            return True
            
        except Exception as e:
            print(f"ERROR saving to table storage: {type(e).__name__}: {str(e)}")
            return False
    
    def save_description_record(self, playlist_id: str, playlist_name: str, 
                                description: str, prompt: str) -> bool:
        """
        Save a record of a generated description
        
        Table schema:
        - PartitionKey: playlist_id
        - RowKey: unique generation ID
        - PlaylistName: name of the playlist
        - Description: the generated description
        - Prompt: the prompt used to generate the description
        - Timestamp: when it was generated
        """
        try:
            table_client = self.table_service_client.get_table_client(self.table_name)
            
            entity = {
                "PartitionKey": playlist_id,
                "RowKey": str(uuid.uuid4()),
                "PlaylistName": playlist_name,
                "Description": description[:4000],  # Truncate if too long
                "Prompt": prompt[:1000],  # Truncate if too long
                "GeneratedAt": datetime.utcnow().isoformat(),
                "Type": "Description"
            }
            
            table_client.create_entity(entity=entity)
            print(f"Saved description record for playlist: {playlist_id}")
            return True
            
        except Exception as e:
            print(f"ERROR saving description to table storage: {type(e).__name__}: {str(e)}")
            return False
    
    def get_playlist_history(self, playlist_id: str):
        """Get all generated covers for a playlist"""
        try:
            table_client = self.table_service_client.get_table_client(self.table_name)
            
            # Query by partition key
            query = f"PartitionKey eq '{playlist_id}'"
            entities = table_client.query_entities(query)
            
            results = []
            for entity in entities:
                results.append({
                    "id": entity.get("RowKey"),
                    "playlist_name": entity.get("PlaylistName"),
                    "blob_url": entity.get("BlobUrl"),
                    "prompt": entity.get("Prompt"),
                    "generated_at": entity.get("GeneratedAt")
                })
            
            return results
            
        except Exception as e:
            print(f"ERROR querying table storage: {type(e).__name__}: {str(e)}")
            return []
    
    def get_all_generations(self, limit: int = 50):
        """Get recent generations across all playlists"""
        try:
            table_client = self.table_service_client.get_table_client(self.table_name)
            entities = table_client.list_entities()
            
            results = []
            count = 0
            for entity in entities:
                if count >= limit:
                    break
                results.append({
                    "playlist_id": entity.get("PartitionKey"),
                    "id": entity.get("RowKey"),
                    "playlist_name": entity.get("PlaylistName"),
                    "blob_url": entity.get("BlobUrl"),
                    "generated_at": entity.get("GeneratedAt")
                })
                count += 1
            
            return results
            
        except Exception as e:
            print(f"ERROR listing from table storage: {type(e).__name__}: {str(e)}")
            return []
