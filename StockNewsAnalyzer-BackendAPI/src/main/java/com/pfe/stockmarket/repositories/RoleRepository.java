package com.pfe.stockmarket.repositories;

import com.pfe.stockmarket.entities.ERole;
import com.pfe.stockmarket.entities.Role;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.Optional;

public interface RoleRepository extends MongoRepository<Role, String> {
    Optional<Role> findByName(ERole name);
}
