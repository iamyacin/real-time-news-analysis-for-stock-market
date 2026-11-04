package com.pfe.stockmarket.controllers;

import com.pfe.stockmarket.entities.News;
import com.pfe.stockmarket.entities.NewsCount;
import com.pfe.stockmarket.entities.Society;
import com.pfe.stockmarket.repositories.NewsRepository;
import com.pfe.stockmarket.repositories.SocietyRepository;
import com.pfe.stockmarket.service.NewsService;
import com.pfe.stockmarket.service.SocietyService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.aggregation.*;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.OffsetDateTime;
import java.util.*;

import static org.springframework.data.mongodb.core.aggregation.Aggregation.*;
import static org.springframework.data.mongodb.core.query.Criteria.where;

@CrossOrigin(origins = "*", maxAge = 3600, allowedHeaders = "*")
@RestController
@RequestMapping("/api")
public class NewsController {

    @Autowired
    private NewsService newsService;

    @Autowired
    private NewsRepository repository;

    @Autowired
    MongoTemplate mongoTemplate;

    @GetMapping(value = "/news")
    @PreAuthorize("hasRole('USER') or hasRole('MODERATOR') or hasRole('ADMIN')")
    public List<News> getAllNews() {
        return newsService.findAll();
    }

    @RequestMapping("/news/ticker/{ticker}/{page}/{size}")
    public List<News> getNewsByTickerPaging(
            @PathVariable("ticker")String ticker,
            @PathVariable("page") int page,
            @RequestParam(defaultValue = "30") int size
            ) {
        Pageable paging = PageRequest.of(page, size);
        Page<News> pageNews;
        pageNews = newsService.findByTicker(ticker, paging);
        return pageNews.getContent();
    }

    @RequestMapping("/news/ticker/{ticker}")
    public List<News> getNewsByTicker(@PathVariable("ticker")String ticker) {
        return newsService.findByTickerOrderByPublishedAtAsc(ticker);
    }

    @GetMapping("/news/ticker-asc/{ticker}")
    public List<News> getNewsByTickerAsc(@PathVariable("ticker")String ticker) {
        return newsService.findByTickerOrderByPublishedAtAsc(ticker);
    }

    @GetMapping("/news/sentiment/{prediction}")
    public List<News> getNewsByPrediction(@PathVariable("prediction")String prediction) {
        return newsService.findByPrediction(prediction);
    }

    @GetMapping("/news/ticker/{ticker}/sentiment/{prediction}")
    public List<News> getNewsByTicker(@PathVariable("ticker")String ticker, @PathVariable("prediction")String prediction) {
        return newsService.findByTickerAndPrediction(ticker, prediction);
    }

    @GetMapping("/news/all-ops")
    public List<NewsCount> getAllOps() {
        Aggregation agg = newAggregation(
                match(where("prediction").is("Positive")),
                group("prediction", "ticker").count().as("total"),
                project("total")
                        .and("prediction").as("prediction")
                        .and("ticker").as("ticker"),
                sort(Sort.Direction.DESC, "total")
        );

        AggregationResults<NewsCount> groupResults
                = mongoTemplate.aggregate(agg, News.class, NewsCount.class);
        List<NewsCount> result = groupResults.getMappedResults();

        for(int i = 0; i<result.size(); i++) {
            Query query = new Query();
            query.addCriteria(where("ticker").is(result.get(i).getTicker()));
            List<News> allNews = mongoTemplate.find(query, News.class);

            result.get(i).setPercent(allNews.isEmpty() ? 0 : (100f * result.get(i).getTotal()) / allNews.size());
        }

        return result;
    }

    @GetMapping("/news/ops/{ticker}")
    public List<NewsCount> getOps(@PathVariable("ticker")String ticker) {
        Query query = new Query();
        query.addCriteria(where("ticker").is(ticker));
        List<News> allNews = mongoTemplate.find(query, News.class);

        Aggregation agg = newAggregation(
                match(where("ticker").is(ticker)),
                group("prediction").count().as("total"),
                project("total").and("prediction").previousOperation(),
                sort(Sort.Direction.DESC, "total")
        );

        AggregationResults<NewsCount> groupResults
                = mongoTemplate.aggregate(agg, News.class, NewsCount.class);
        List<NewsCount> result = groupResults.getMappedResults();
        int total = allNews.size();
        System.out.println(total);
        for(int i = 0; i<result.size(); i++)
            result.get(i).setPercent((100 * result.get(i).getTotal()) / total);

        return result;
    }

    @GetMapping("/news/ops-last-month/{ticker}/{days}")
    public List<NewsCount> getLastMonthOps(@PathVariable("ticker")String ticker, @PathVariable("days") int days) {
        LocalDateTime now = LocalDateTime.now();
        LocalDateTime start = now.minusDays(days);

        Criteria criteria = new Criteria().andOperator(
                where("publishedAt").lte(now.toString()).gte(start.toString()).and("ticker").is(ticker)
        );

        Query query = new Query();
        query.addCriteria(criteria);
        List<News> allNews = mongoTemplate.find(query, News.class);

        Aggregation agg = newAggregation(
                match(criteria),
                group("prediction").count().as("total"),
                project("total").and("prediction").previousOperation(),
                sort(Sort.Direction.DESC, "total")
        );

        AggregationResults<NewsCount> groupResults
                = mongoTemplate.aggregate(agg, News.class, NewsCount.class);
        List<NewsCount> result = groupResults.getMappedResults();
        int total = allNews.size();

        for(int i = 0; i<result.size(); i++)
            result.get(i).setPercent(total == 0 ? 0 : (100f * result.get(i).getTotal()) / total);

        return result;
    }

    @GetMapping("/news/ops-date/{ticker}")
    public TreeMap<String, List<NewsCount>> getOpsByDate(@PathVariable("ticker")String ticker) {
        LocalDateTime now = LocalDateTime.now();
        LocalDateTime start = now.minusDays(90);

        Criteria criteria = new Criteria().andOperator(
                where("publishedAt").lte(now.toString()).gte(start.toString()).and("ticker").is(ticker)
        );

        ProjectionOperation dateProjection = project()
                .and("prediction").as("prediction")
                .and("publishedAt").substring(0, 10).as("publishedAt");

        GroupOperation groupBy = group("publishedAt", "prediction")
                .count().as("total");

        Aggregation agg = newAggregation(
                match(criteria),
                dateProjection,
                groupBy,
                project("total")
                        .and("prediction").as("predict")
                        .and("publishedAt").substring(0, 10).as("publishedAt"),
                sort(Sort.Direction.DESC, "publishedAt")
        );

        AggregationResults<NewsCount> groupResults
                = mongoTemplate.aggregate(agg, News.class, NewsCount.class);
        List<NewsCount> result = groupResults.getMappedResults();

        TreeMap<String, List<NewsCount>> datesOps = new TreeMap<>();
        List ops = new ArrayList();
        TreeMap<String, String> dates = new TreeMap<String, String>();
        int total = result.size();
        for(int i = 0; i<result.size(); i++) {
            dates.put(result.get(i).getPublishedAt(), result.get(i).getPublishedAt());
        }
        int t = 0;
        for (Map.Entry<String, String> element : dates.entrySet()) {
            List<NewsCount> lst = new ArrayList<NewsCount>();
            String cur_dt = element.getValue();
            for (int k = 0; k < result.size(); k++) {
                if(cur_dt.equals(result.get(k).getPublishedAt())) {
                    lst.add(result.get(k));
                }
            }
            //System.out.println(lst);
            datesOps.put(cur_dt, lst);
        }

        return datesOps;
    }

    @GetMapping("/news/ops-month/{ticker}")
    public TreeMap<String, List<NewsCount>> getOpsByMonth(@PathVariable("ticker")String ticker) {
        Criteria criteria = new Criteria().andOperator(
                where("ticker").is(ticker)
        );

        ProjectionOperation dateProjection = project()
                .and("prediction").as("prediction")
                .and("publishedAt").substring(0, 7).as("publishedAt");

        GroupOperation groupBy = group("publishedAt", "prediction")
                .count().as("total");

        Aggregation agg = newAggregation(
                match(criteria),
                dateProjection,
                groupBy,
                project("total")
                        .and("prediction").as("predict")
                        .and("publishedAt").substring(0, 7).as("publishedAt"),
                sort(Sort.Direction.ASC, "publishedAt")
        );

        AggregationResults<NewsCount> groupResults
                = mongoTemplate.aggregate(agg, News.class, NewsCount.class);
        List<NewsCount> result = groupResults.getMappedResults();

        TreeMap<String, List<NewsCount>> datesOps = new TreeMap<>();
        List ops = new ArrayList();
        TreeMap<String, String> dates = new TreeMap<String, String>();
        int total = result.size();
        for(int i = 0; i<result.size(); i++) {
            dates.put(result.get(i).getPublishedAt(), result.get(i).getPublishedAt());
        }
        int t = 0;
        for (Map.Entry<String, String> element : dates.entrySet()) {
            List<NewsCount> lst = new ArrayList<NewsCount>();
            String cur_dt = element.getValue();
            for (int k = 0; k < result.size(); k++) {
                if(cur_dt.equals(result.get(k).getPublishedAt())) {
                    lst.add(result.get(k));
                }
            }
            //System.out.println(lst);
            datesOps.put(cur_dt, lst);
        }

        return datesOps;
    }

    @GetMapping("/news/all-ops-date")
    public TreeMap<String, List<NewsCount>> getAllOpsByDate() {
        LocalDateTime now = LocalDateTime.now();
        LocalDateTime start = now.minusDays(90);

        Criteria criteria = new Criteria().andOperator(
                where("publishedAt").lte(now.toString()).gte(start.toString())
        );

        ProjectionOperation dateProjection = project()
                .and("prediction").as("prediction")
                .and("publishedAt").substring(0, 10).as("publishedAt");

        GroupOperation groupBy = group("publishedAt", "prediction")
                .count().as("total");

        Aggregation agg = newAggregation(
                match(criteria),
                dateProjection,
                groupBy,
                project("total")
                        .and("prediction").as("predict")
                        .and("publishedAt").substring(0, 10).as("publishedAt"),
                sort(Sort.Direction.DESC, "publishedAt")
        );

        AggregationResults<NewsCount> groupResults
                = mongoTemplate.aggregate(agg, News.class, NewsCount.class);
        List<NewsCount> result = groupResults.getMappedResults();

        TreeMap<String, List<NewsCount>> datesOps = new TreeMap<>();
        List ops = new ArrayList();
        TreeMap<String, String> dates = new TreeMap<String, String>();
        int total = result.size();
        for(int i = 0; i<result.size(); i++) {
            dates.put(result.get(i).getPublishedAt(), result.get(i).getPublishedAt());
        }
        int t = 0;
        for (Map.Entry<String, String> element : dates.entrySet()) {
            List<NewsCount> lst = new ArrayList<NewsCount>();
            String cur_dt = element.getValue();
            for (int k = 0; k < result.size(); k++) {
                if(cur_dt.equals(result.get(k).getPublishedAt())) {
                    lst.add(result.get(k));
                }
            }
            //System.out.println(lst);
            datesOps.put(cur_dt, lst);
        }

        return datesOps;
    }
}
