import hazelcast

# Connect to Hazelcast cluster.
client = hazelcast.HazelcastClient()
distributed_map = client.get_map("logs-map")
distributed_map.clear()
client.shutdown()