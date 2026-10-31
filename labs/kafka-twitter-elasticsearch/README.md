# Kafka Twitter → Elasticsearch lab

Java producer/consumer lab imported from the
`kafka-with-twitter-and-elasticsearch` repository.

- `TwitterProducer.java` streams tweets matching `bitcoin` into the
  `Tweets-from-java` Kafka topic.
- `ElasticSearchConsumer.java` reads that topic and indexes the raw tweets into
  the `twitter` index in Elasticsearch.

`TwitterCredentials.java` was removed from the source repository before the
import, so this lab does not compile until you provide your own class containing:

```java
CONSUMER_KEY
CONSUMER_SECRET
TOKEN
TOKEN_SECRET
```

Kafka is expected on `localhost:9092` and Elasticsearch on `localhost:9200`.
