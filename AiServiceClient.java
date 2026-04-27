import org.springframework.http.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.client.RestClientException;
import org.springframework.http.client.SimpleClientHttpRequestFactory;

import java.util.HashMap;
import java.util.Map;

public class AiServiceClient {

    private final RestTemplate restTemplate;
    private final String BASE_URL = "http://127.0.0.1:5000";

    public AiServiceClient() {
        this.restTemplate = createRestTemplate();
    }

    
    private RestTemplate createRestTemplate() {
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout(10000);
        factory.setReadTimeout(10000);
        return new RestTemplate(factory);
    }

    
    public String getChatResponse(String message) {
        String url = BASE_URL + "/chat";

        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            Map<String, String> body = new HashMap<>();
            body.put("message", message);

            HttpEntity<Map<String, String>> request = new HttpEntity<>(body, headers);

            ResponseEntity<Map> response = restTemplate.postForEntity(url, request, Map.class);

            if (response.getStatusCode() == HttpStatus.OK) {
                return (String) response.getBody().get("response");
            } else {
                return null;
            }

        } catch (RestClientException e) {
            System.out.println("Error calling AI service: " + e.getMessage());
            return null; 
        }
    }
}