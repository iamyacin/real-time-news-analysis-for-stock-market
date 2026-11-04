package com.pfe.stockmarket.controllers;

import com.pfe.stockmarket.entities.Society;
import com.pfe.stockmarket.repositories.SocietyRepository;
import com.pfe.stockmarket.service.SocietyService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;
import java.util.TreeSet;

@CrossOrigin(origins = "*", maxAge = 3600, allowedHeaders = "*")
@RestController
@RequestMapping("/api")
public class SocietyController {

    @Autowired
    private SocietyService societyService;

    @Autowired
    private SocietyRepository repository;

    @Autowired
    MongoTemplate mongoTemplate;

    @GetMapping(value = "/societies")
    public List<Society> getAllSocieties() {
        return societyService.findAll();
    }

    @GetMapping(value = "/sectors")
    public TreeSet<String> getAllSectors() {
        Query query = new Query();
        List<Society> societies = mongoTemplate.find(query, Society.class);
        TreeSet<String> sectors = new TreeSet<>();
        for (Society society : societies) {
            if (society.getSector() != null) {
                sectors.add(society.getSector());
            }
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
}
