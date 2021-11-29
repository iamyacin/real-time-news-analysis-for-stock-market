package com.pfe.stockmarket.impl;

import com.pfe.stockmarket.entities.Society;
import com.pfe.stockmarket.repositories.SocietyRepository;
import com.pfe.stockmarket.service.SocietyService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class SocietyServiceImpl implements SocietyService {
    @Autowired
    private SocietyRepository societyRepository;

    @Override
    public List<Society> findAll() {
        return societyRepository.findAll();
    }

    @Override
    public List<Society> findBySector(String sector) {
        return societyRepository.findBySector(sector);
    }

    @Override
    public Optional<Society> findById(String id) {
        return societyRepository.findById(id);
    }

    /*@Override
    public Society findById(String id) {
        return societyRepository.findById(id);
    }*/
}
