package com.pfe.stockmarket.controllers;

import com.pfe.stockmarket.entities.Society;
import com.pfe.stockmarket.repositories.SocietyRepository;
import com.pfe.stockmarket.service.SocietyService;
import net.minidev.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import javax.validation.constraints.NotEmpty;
import java.util.*;

@CrossOrigin(origins = "*", maxAge = 3600, allowedHeaders = "*")
@RestController
@RequestMapping("/api")
public class SocietyController {

    @Autowired
    private SocietyService societyService;

    @Autowired
    private SocietyRepository repository;

    @Autowired
    private RestTemplate restTemplate;

    @Autowired
    MongoTemplate mongoTemplate;

    @GetMapping(value = "/societies")
    @PreAuthorize("hasRole('USER') or hasRole('MODERATOR') or hasRole('ADMIN')")
    public List<Society> getAllSocieties() {
        return societyService.findAll();
    }

    @GetMapping(value = "/sectors")
    public TreeSet<String> getAllSectors() {
        Query query = new Query();
        List<Society> societies = mongoTemplate.find(query, Society.class);
        TreeSet<String> sectors = new TreeSet<>();
        for(int i = 0; i<societies.size(); i++) {
            if(societies.get(i).getSector() != null)
                sectors.add(societies.get(i).getSector());
        }

        return sectors;
    }

    @GetMapping(value = "/societies/{id}")
    public Optional<Society> getSocietyById(@PathVariable("id") String id) {
        return societyService.findById(id);
    }

    @GetMapping(value = "/societies-sector/{sector}")
    public List<Society> getSocietiesBySector(@PathVariable("sector") String sector) {

        return societyService.findBySector(sector);
    }

    @GetMapping(value = "/fill-societies")
    public String[] fillSocietiesFromYahooFinance() {
        //String url = "https://query1.finance.yahoo.com/v7/finance/options/";
        String[] symbols = {
                "a", "aapl", "intc", "msft", "wmt", "ko",
                "mmm", "v", "amzn", "nflx", "nike", "nok",
                "fb", "vici", "ebay", "apa", "uber", "upwk",
                "inds", "ndaq", "tsla", "goog", "googl", "jnj",
                "brk.b", "brk.a", "cl", "bac", "ba", "bk", "banc",
                "bachy", "azre", "etsy", "bmy", "djia", "spx", "vz"
        };
        List<Object> objects = new ArrayList<Object>();
        for (String symbol: symbols) {
            String url = "https://query1.finance.yahoo.com/v7/finance/options/" + symbol;
            Object ste = restTemplate.getForObject(url, Object.class);
            JSONObject jsonSte = new JSONObject((Map<String, ?>) ste);
            JSONObject optionChain = new JSONObject((Map<String, ?>) jsonSte.get("optionChain"));
            ArrayList result = (ArrayList) optionChain.get("result");
            boolean r = result.isEmpty();
            if(r == true)
                continue;
            JSONObject quote = new JSONObject((Map<String, ?>) result.get(0));
            objects.add(quote.get("quote"));
            //JSONObject res = (JSONObject) result.get(0);
            //objects.add(result.get(0));
            //repository.save(new Society("2222","Nike"));
        }

        /*for(Object info: objects) {
            JSONObject ste = new JSONObject((Map<String, ?>) info);
            System.out.println("Add ste" + ste.get("symbol"));
            Society society = new Society("20" + ste.get("symbol"), (String) ste.get("symbol"));
            society.setCurrency((String) ste.get("currency"));
            society.setShort_name((String) ste.get("shortName"));
            society.setLong_name((String) ste.get("longName"));
            society.setLanguage((String) ste.get("language"));
            society.setDisplayName((String) ste.get("displayName"));
            society.setRegion((String) ste.get("region"));
            society.setExchange((String) ste.get("exchange"));
            if(ste.get("forwardPE") != null) society.setForward_pe((double) ste.get("forwardPE"));
            if(ste.get("priceToBook") != null) society.setPrice_to_book((double) ste.get("priceToBook"));
            if(ste.get("marketCap") != null) {
                Long cap = new Long(ste.get("marketCap").toString());
                society.setMarket_cap(cap);
            }
            if(ste.get("bookValue") != null) society.setBook_value((double) ste.get("bookValue"));
            society.setMarket((String) ste.get("market"));
            repository.save(society);
        }*/

        return symbols;
    }

    /*@DeleteMapping(value = "/{id}")
    public Society getSociety(@PathVariable String id) {
        return societyService.findOne(id);
    }*/
}
