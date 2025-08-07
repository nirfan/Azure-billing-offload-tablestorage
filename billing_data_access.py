from azure.cosmos import CosmosClient
from azure.data.tables import TableServiceClient

# CONFIGURE as per your environment
COSMOS_URI = "<COSMOS_DB_URI>"      # TODO
COSMOS_KEY = "<COSMOS_DB_KEY>"
COSMOS_DB_NAME = "<DATABASE_NAME>"
COSMOS_CONTAINER = "<CONTAINER_NAME>"

TABLE_CONN_STR = "<TABLE_STORAGE_CONN_STRING>"
TABLE_NAME = "<TABLE_NAME>"

def get_billing_record(record_id, customer_id):
    # Try Cosmos DB first
    cosmos = CosmosClient(COSMOS_URI, COSMOS_KEY)
    container = cosmos.get_database_client(COSMOS_DB_NAME).get_container_client(COSMOS_CONTAINER)
    try:
        item = container.read_item(record_id, partition_key=customer_id)
        return item
    except Exception:
        # Not found in hot storage, check Table Storage
        table_service = TableServiceClient.from_connection_string(TABLE_CONN_STR)
        table = table_service.get_table_client(TABLE_NAME)
        entity = table.get_entity(partition_key=customer_id, row_key=record_id)
        if entity:
            return entity
        else:
            raise Exception("Record not found in either storage.")

# Example usage
if __name__ == "__main__":
    print(get_billing_record("RECORD123", "CUSTOMER456"))
