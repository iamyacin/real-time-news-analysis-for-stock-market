package com.pfe.stockmarket.repositories;

import com.pfe.stockmarket.entities.News;
import com.pfe.stockmarket.entities.Society;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface NewsRepository extends MongoRepository<News, String> {
    List<News> findAll();
    Page<News> findByTicker(String ticker, Pageable pageable);
    List<News> findByPrediction(String prediction);
    List<News> findByTickerAndPrediction(String Ticker, String prediction);
    List<News> findByTickerOrderByPublishedAtAsc(String ticker);
    List<News> findByPredictionOrderByPublishedAtAsc(String prediction);
    //List<News> aggregationByAll(String ticker);
}
