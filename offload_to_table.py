import datetime
from azure.cosmos import CosmosClient
from azure.data.tables import TableServiceClient

# ====== CONFIGURATION ======
COSMOS_URI = "<COSMOS_DB_URI>"  # TODO: Your Cosmos DB URI
COSMOS_KEY = "<COSMOS_DB_KEY>"  # TODO: Your Cosmos DB Primary Key
COSMOS_DB_NAME = "<DATABASE_NAME>"  # TODO
COSMOS_CONTAINER = "<CONTAINER_NAME>"  # TODO

TABLE_CONN_STR = "<TABLE_STORAGE_CONN_STRING>"  # TODO
TABLE_NAME = "<TABLE_NAME>"  # TODO (e.g., "BillingArchive")

def migrate_cosmos_to_table():
    # Connect to databases
    cosmos = CosmosClient(COSMOS_URI, COSMOS_KEY)
    container = cosmos.get_database_client(COSMOS_DB_NAME).get_container_client(COSMOS_CONTAINER)
    table_service = TableServiceClient.from_connection_string(TABLE_CONN_STR)
    table = table_service.get_table_client(TABLE_NAME)

    cutoff = (datetime.datetime.utcnow() - datetime.timedelta(days=90)).isoformat()
    query = "SELECT * FROM c WHERE c.timestamp < @cutoff"
    params = [{"name": "@cutoff", "value": cutoff}]

    print("Migrating records older than:", cutoff)
    count = 0
    for item in container.query_items(query, parameters=params):
        entity = {
            "PartitionKey": item.get("customerId", "default"),
            "RowKey": item["id"],
            "Amount": item.get("amount"),
            "Timestamp": item.get("timestamp"),
            # Add further fields as needed
        }
        table.upsert_entity(entity)
        # Remove original from Cosmos after successful insert
        container.delete_item(item, partition_key=item["partitionKey"])
        count += 1
    print(f"Migration complete, {count} records moved.")

if __name__ == "__main__":
    migrate_cosmos_to_table()
