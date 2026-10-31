# Integrations

Companion projects that connect to this repository's prediction service.

## `kafka-streams-crypto-tweets/`

A Java/Kafka Streams job imported from the
`Kafka-Streams-Tweets-To-ElasticSearch` repository. It consumes crypto tweets
from Kafka, calls the Flask microservice in `NewsPredictionMicroservice/`
(`POST /NewsOrNot` and `POST /Polarity`), and indexes the classified tweets
into Elasticsearch.

This module is not required to run the main news pipeline. It demonstrates how
the prediction service can be reused by a streaming consumer. See the module's
own README for run instructions.
