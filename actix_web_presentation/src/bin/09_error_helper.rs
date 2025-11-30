use actix_web::{App, HttpServer, error, get};

#[derive(Debug)]
struct MyError {
    name: &'static str,
}

#[get("/")]
async fn index() -> actix_web::Result<String> {
    let result = Err(MyError { name: "test error" });

    result.map_err(|err| error::ErrorBadRequest(err.name))
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
    use actix_web::{App, http::StatusCode, http::header::ContentType, test};

    use super::*;

    #[actix_web::test]
    async fn test_error_helper() {
        let app = test::init_service(App::new().service(index)).await;
        let request = test::TestRequest::default()
            .insert_header(ContentType::plaintext())
            .to_request();
        let response = test::call_service(&app, request).await;
        assert_eq!(response.status(), StatusCode::BAD_REQUEST);
        let body_bytes = test::read_body(response).await;
        let body_str = std::str::from_utf8(&body_bytes).unwrap();
        assert_eq!(body_str, "test error");
    }
}
