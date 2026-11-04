package com.pfe.stockmarket.impl;

import com.pfe.stockmarket.entities.User;
import com.pfe.stockmarket.repositories.UserRepository;
import com.pfe.stockmarket.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class UserServiceImpl implements UserService {
    @Autowired
    private UserRepository userRepository;

    @Override
    public List<User> findAll() {
        return userRepository.findAll();
    }

    @Override
    public Optional<User> findByUsername(String username) {
        return userRepository.findByUsername(username);
    }

    /*@Override
    public Society findById(String id) {
        return societyRepository.findById(id);
    }*/
}
