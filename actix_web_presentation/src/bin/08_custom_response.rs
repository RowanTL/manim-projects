use actix_web::{
    App, HttpRequest, HttpResponse, HttpServer, Responder, body::BoxBody, get,
    http::header::ContentType,
};
use serde::Serialize;

#[derive(Serialize)]
struct MyObj {
    name: &'static str,
}

impl Responder for MyObj {
    type Body = BoxBody;

    fn respond_to(self, _req: &HttpRequest) -> HttpResponse<Self::Body> {
        let body = serde_json::to_string(&self).unwrap();

        // Create response and set content type
        // literally responds with: {"name": "user"}
        HttpResponse::Ok()
            .content_type(ContentType::json())
            .body(body)
    }
}

#[get("/")]
async fn index() -> impl Responder {
    MyObj { name: "user" }
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| App::new().service(index))
        .bind(("127.0.0.1", 8080))?
        .run()
        .await
}

#[cfg(test)]
mod tests {
    use actix_web::{App, http::header::ContentType, test};

    use super::*;

    #[actix_web::test]
    async fn test_custom_response_get() {
        let app = test::init_service(App::new().service(index)).await;
        let request = test::TestRequest::default()
            .insert_header(ContentType::plaintext())
            .to_request();
        let response = test::call_service(&app, request).await;
        assert!(response.status().is_success());
        let body_bytes = test::read_body(response).await;
        let body_str = std::str::from_utf8(&body_bytes).unwrap();
        assert_eq!(body_str, "{\"name\":\"user\"}");
    }
}
