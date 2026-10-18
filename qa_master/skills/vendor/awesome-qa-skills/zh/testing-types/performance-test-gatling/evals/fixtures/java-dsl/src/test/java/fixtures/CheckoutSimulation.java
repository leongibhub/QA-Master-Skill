package fixtures;

import io.gatling.javaapi.core.Simulation;
import static io.gatling.javaapi.core.CoreDsl.*;
import static io.gatling.javaapi.http.HttpDsl.*;

public class CheckoutSimulation extends Simulation {
  public CheckoutSimulation() {
    String baseUrl = required("fixture.baseUrl");
    double arrivals = Double.parseDouble(required("fixture.usersPerSec"));
    int seconds = Integer.parseInt(required("fixture.durationSeconds"));
    int p95Millis = Integer.parseInt(required("fixture.p95Millis"));
    double errorPercent = Double.parseDouble(required("fixture.errorPercent"));
    if (arrivals <= 0 || seconds <= 0 || p95Millis <= 0 || errorPercent < 0 || errorPercent > 100)
      throw new IllegalArgumentException("invalid supplied load/gates");
    var users = csv("users.csv").queue();
    var flow = scenario("checkout").feed(users)
      .exec(http("paid-order").get("/orders/#{order_id}")
        .check(status().is(200), jsonPath("$.state").is("paid"), jsonPath("$.amount").ofInt().is(20)));
    setUp(flow.injectOpen(constantUsersPerSec(arrivals).during(seconds)))
      .protocols(http.baseUrl(baseUrl))
      .assertions(global().responseTime().percentile(95.0).lte(p95Millis),
                  global().failedRequests().percent().lte(errorPercent));
  }
  private static String required(String key) {
    String value = System.getProperty(key);
    if (value == null || value.isBlank()) throw new IllegalArgumentException("missing project value: " + key);
    return value;
  }
}
