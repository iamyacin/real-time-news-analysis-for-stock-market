package com.pfe.stockmarket.impl;

import com.pfe.stockmarket.entities.News;
import com.pfe.stockmarket.repositories.NewsRepository;
import com.pfe.stockmarket.service.NewsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.util.List;

import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.core.MongoTemplate;

@Service
public class NewsServiceImpl implements NewsService {
    @Autowired
    private NewsRepository newsRepository;

    @Autowired
    MongoTemplate mongoTemplate;

    @Override
    public List<News> findAll() {
        return newsRepository.findAll(Sort.by(Sort.Direction.ASC, "publishedAt"));
    }

    @Override
    public Page<News> findByTicker(String ticker, Pageable pageable) {
        return newsRepository.findByTicker(ticker, pageable);
    }

    @Override
    public List<News> findByPrediction(String prediction) {
        return newsRepository.findByPrediction(prediction);
    }

    @Override
    public List<News> findByTickerAndPrediction(String ticker, String prediction) {
        return newsRepository.findByTickerAndPrediction(ticker, prediction);
    }

    @Override
    public List<News> findByTickerOrderByPublishedAtAsc(String ticker) {
        return newsRepository.findByTickerOrderByPublishedAtAsc(ticker);
    }

    @Override
    public List<News> findByPredictionOrderByPublishedAtAsc(String prediction) {
        return newsRepository.findByPredictionOrderByPublishedAtAsc(prediction);
    }

    /*@Override
    public List<News> aggregationByAll(String ticker) {
        Aggregation aggregation = newAggregation(group("prediction").count().as("total"));

        AggregationResults<News> groupResults = mongoTemplate.aggregate(
                aggregation, "predictions", News.class);

        List<News> newsReport = groupResults.getMappedResults();

        return newsReport;
    }*/
}
