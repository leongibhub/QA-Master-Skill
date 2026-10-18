package com.example.api;
import io.restassured.builder.RequestSpecBuilder;
import io.restassured.specification.RequestSpecification;
import org.junit.jupiter.api.BeforeEach;

public class BaseApiTest {
    protected RequestSpecification requestSpec;
    protected static String requiredEnv(String name) {
        String value = System.getenv(name);
        if (value == null || value.isBlank()) throw new IllegalStateException("Set " + name + " before execution");
        return value;
    }
    @BeforeEach
    void setupSpec() {
        requestSpec = new RequestSpecBuilder().setBaseUri(requiredEnv("BASE_URL")).build();
    }
}
