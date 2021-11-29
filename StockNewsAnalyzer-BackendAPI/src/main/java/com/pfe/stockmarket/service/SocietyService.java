package com.pfe.stockmarket.service;

import com.pfe.stockmarket.entities.Society;

import java.util.List;
import java.util.Optional;

public interface SocietyService {
    List<Society> findAll();
    List<Society> findBySector(String sector);
    Optional<Society> findById(String id);

    //Society findById(String id);
}
