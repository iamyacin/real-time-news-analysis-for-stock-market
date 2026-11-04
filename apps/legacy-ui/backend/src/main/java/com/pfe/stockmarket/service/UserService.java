package com.pfe.stockmarket.service;

import com.pfe.stockmarket.entities.User;

import java.util.List;
import java.util.Optional;

public interface UserService {
    List<User> findAll();

    Optional<User> findByUsername(String username);

    //Society findById(String id);
}
