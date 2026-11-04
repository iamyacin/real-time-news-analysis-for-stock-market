package com.pfe.stockmarket.repositories;

import com.pfe.stockmarket.entities.Society;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface SocietyRepository extends MongoRepository<Society, String> {

    //Society save(Society society);

    //List<Society> saveAll(List<Society> societies);

    List<Society> findAll();

    //List<Society> findAll(List<String> ids);

    List<Society> findBySector(String sector);

    Optional<Society> findById(String id);

    //long count();

}
