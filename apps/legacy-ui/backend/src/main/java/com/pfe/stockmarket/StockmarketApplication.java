package com.pfe.stockmarket;

import com.pfe.stockmarket.entities.ERole;
import com.pfe.stockmarket.entities.Role;
import com.pfe.stockmarket.entities.Society;
import com.pfe.stockmarket.entities.User;
import com.pfe.stockmarket.repositories.RoleRepository;
import com.pfe.stockmarket.repositories.SocietyRepository;
import com.pfe.stockmarket.repositories.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.client.RestTemplate;

import java.util.Set;

@SpringBootApplication
public class StockmarketApplication implements CommandLineRunner {

	@Autowired
	SocietyRepository repository;

	@Autowired
	RoleRepository roleRepository;

	@Autowired
	UserRepository userRepository;

	@Autowired
	PasswordEncoder passwordEncoder;

	@Value("${stockmarket.app.demoPassword:admin123}")
	String demoPassword;

	public static void main(String[] args) {
		SpringApplication.run(StockmarketApplication.class, args);
	}

	@Override
	public void run(String... args) {
		addSampleData();
	}

	public void addSampleData() {
		for (ERole roleName : ERole.values()) {
			if (roleRepository.findByName(roleName).isEmpty()) {
				roleRepository.save(new Role(roleName));
			}
		}
		Role adminRole = roleRepository.findByName(ERole.ROLE_ADMIN)
				.orElseGet(() -> roleRepository.save(new Role(ERole.ROLE_ADMIN)));
		if (!userRepository.existsByUsername("admin")) {
			User admin = new User("admin", "admin@example.com", passwordEncoder.encode(demoPassword));
			admin.setRoles(Set.of(adminRole));
			userRepository.save(admin);
			System.out.println("Seeded demo user: admin / " + demoPassword);
		}

		if (repository.count() == 0) {
			seedSociety("AAPL", "Apple", "Technology", "Consumer Electronics");
			seedSociety("MSFT", "Microsoft", "Technology", "Software");
			seedSociety("AMZN", "Amazon", "Consumer Discretionary", "E-commerce");
			seedSociety("GOOGL", "Alphabet", "Communication Services", "Internet Content");
			seedSociety("FB", "Meta Platforms", "Communication Services", "Social Media");
			seedSociety("TSLA", "Tesla", "Consumer Discretionary", "Automobiles");
			seedSociety("NFLX", "Netflix", "Communication Services", "Entertainment");
			seedSociety("JPM", "JPMorgan Chase", "Financials", "Banks");
			seedSociety("BAC", "Bank of America", "Financials", "Banks");
			seedSociety("V", "Visa", "Financials", "Payment Services");
			seedSociety("MA", "Mastercard", "Financials", "Payment Services");
			seedSociety("DIS", "Walt Disney", "Communication Services", "Entertainment");
			seedSociety("KO", "Coca-Cola", "Consumer Staples", "Beverages");
			seedSociety("MCD", "McDonald's", "Consumer Discretionary", "Restaurants");
			seedSociety("NKE", "Nike", "Consumer Discretionary", "Apparel");
			seedSociety("SBUX", "Starbucks", "Consumer Discretionary", "Restaurants");
			seedSociety("BA", "Boeing", "Industrials", "Aerospace");
			seedSociety("F", "Ford", "Consumer Discretionary", "Automobiles");
			seedSociety("GM", "General Motors", "Consumer Discretionary", "Automobiles");
			seedSociety("T", "AT&T", "Communication Services", "Telecom");
			seedSociety("VZ", "Verizon", "Communication Services", "Telecom");
			seedSociety("IBM", "IBM", "Technology", "IT Services");
			seedSociety("ORCL", "Oracle", "Technology", "Software");
			seedSociety("CRM", "Salesforce", "Technology", "Software");
			seedSociety("UBER", "Uber", "Industrials", "Transportation");
			seedSociety("SHOP", "Shopify", "Technology", "Software");
			seedSociety("BABA", "Alibaba", "Consumer Discretionary", "E-commerce");
		}
	}

	private void seedSociety(String ticker, String name, String sector, String industry) {
		Society society = new Society(ticker, ticker);
		society.setShortName(name);
		society.setLongName(name);
		society.setSector(sector);
		society.setIndustry(industry);
		society.setLogo_url("/imgs/logo.png");
		society.setCountry("United States");
		society.setCurrency("USD");
		society.setQuoteType("EQUITY");
		repository.save(society);
	}

	@Bean
	public RestTemplate restTemplate() {
		return new RestTemplate();
	}
}
