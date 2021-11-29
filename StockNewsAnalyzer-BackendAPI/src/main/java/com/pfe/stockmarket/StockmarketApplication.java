package com.pfe.stockmarket;

import com.pfe.stockmarket.entities.ERole;
import com.pfe.stockmarket.entities.Role;
import com.pfe.stockmarket.entities.Society;
import com.pfe.stockmarket.entities.User;
import com.pfe.stockmarket.repositories.RoleRepository;
import com.pfe.stockmarket.repositories.SocietyRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.web.client.RestTemplate;

@SpringBootApplication
public class StockmarketApplication implements CommandLineRunner {

	@Autowired
	SocietyRepository repository;

	@Autowired
	RoleRepository roleRepository;

	public static void main(String[] args) {
		SpringApplication.run(StockmarketApplication.class, args);
	}

	@Override
	public void run(String... args) throws Exception {
		addSampleData();
	}

	public void addSampleData() {
		System.out.println("Adding sample data");

		/*repository.save(new Society("1111","Amazon", "Amazon [ˈæməˌzɑːn] est une entreprise de commerce électronique américaine basée à Seattle. Elle est un des géants du Web, regroupés sous l'acronyme GAFAM, aux côtés de Google, Apple, Facebook et Microsoft.", "Ecommerce"));
		repository.save(new Society("2222","Nike", "Nike est une société américaine créée en 1971 par Philip Knight et Bill Bowerman. Basée à Beaverton dans l'Oregon, elle est spécialisée dans la fabrication d'articles de sport", "Sport Brand"));
		repository.save(new Society("3333","Facebook", "Facebook [ˈfeɪsbʊk] est une société américaine créée en 2004 par Mark Zuckerberg. Initialement concentrée sur le réseau social Facebook, la compagnie a racheté Instagram en 2012, ainsi que WhatsApp et Oculus VR en 2014.", "Social Network"));
		repository.save(new Society("4444","Ebay", "eBay est une entreprise américaine de courtage en ligne, connue par son site web de ventes aux enchères du même nom. Elle a été créée en 1995 par le Français Pierre Omidyar. Elle est devenue une référence mondiale dans son secteur et un phénomène de société.", "Ecommerce"));

		System.out.println("Adding sample users data");
		roleRepository.save(new Role(ERole.ROLE_USER));
		roleRepository.save(new Role(ERole.ROLE_MODERATOR));
		roleRepository.save(new Role(ERole.ROLE_ADMIN));*/
	}

	@Bean
	public RestTemplate restTemplate() {
		return new RestTemplate();
	}
}
