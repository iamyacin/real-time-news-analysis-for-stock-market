# Kafka Streams Crypto Tweets → Elasticsearch

Java/Kafka Streams companion job imported from the
`Kafka-Streams-Tweets-To-ElasticSearch` repository. It consumes tweets from the
`crypto-tweets` Kafka topic, keeps tweets from users with more than 4,999
followers, calls this project's Flask prediction service, and indexes the
classified tweets into Elasticsearch.

## Relationship to the main project

The job is not part of the main news collection pipeline. It shows how
`NewsPredictionMicroservice/` can serve a streaming consumer:

- `POST http://localhost:5000/NewsOrNot` — filters business/crypto news
- `POST http://localhost:5000/Polarity` — predicts sentiment

The enriched tweet is written to the `crypto-tweets` index in Elasticsearch.

## Running

1. Start the Flask service:

   ```bash
   cd NewsPredictionMicroservice
   python app.py
   ```

2. Start Kafka on `localhost:9092` and Elasticsearch on `localhost:9200`.
3. Create the `crypto-tweets` topic and feed it with a Twitter producer.
4. Build and run the job (Maven is required; it may not be installed in this
   environment):

   ```bash
   mvn package
   ```

The original source repository contained only the Kafka Streams job, not the
producer that fills the `crypto-tweets` topic.
