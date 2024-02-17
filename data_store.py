from google.cloud import discoveryengine_v1alpha as ds

class DataStore:
    def __init__(self) -> None:
        self.client = ds.SearchService()

    def create(self, data_store_name: str, data_store_id: str) -> None:
        data_store = ds.DataStore()
        data_store.display_name = data_store_name

        request = ds.CreateDataStoreRequest(
            data_store=data_store,
            data_store_id=data_store_id,
        )

        op = self.client.create_data_store(request=request)
        response = op.result

        print("Data Store {data_store_name} with id {data_store_id}, created successfully")

    def push_documents(self) -> None:
        pass

    def delete_document(self, document_id: str) -> None:
        pass

    def search(self, query: str, **kwargs) -> None:
        pass