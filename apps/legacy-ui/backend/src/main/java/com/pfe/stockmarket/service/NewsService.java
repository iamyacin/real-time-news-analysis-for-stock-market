package com.pfe.stockmarket.service;

import com.pfe.stockmarket.entities.News;
import com.pfe.stockmarket.entities.Society;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.util.List;
import java.util.Optional;

public interface NewsService {
    List<News> findAll();
    Page<News> findByTicker(String ticker, Pageable pageable);
    List<News> findByPrediction(String prediction);
    List<News> findByTickerAndPrediction(String Ticker, String prediction);
    List<News> findByTickerOrderByPublishedAtAsc(String ticker);
    List<News> findByPredictionOrderByPublishedAtAsc(String prediction);
    //List<News> aggregationByAll(String ticker);
}
