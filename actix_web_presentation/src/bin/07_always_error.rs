use actix_web::{App, HttpServer, get};
use std::str::Utf8Error;

#[get("/")]
async fn index() -> Result<String, Utf8Error> {
    let invalid_bytes = vec![0, 159, 100];
    let error = String::from_utf8(invalid_bytes);
    Err(error.unwrap_err().utf8_error())
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
    async fn test_always_error() {
        let app = test::init_service(App::new().service(index)).await;
        let request = test::TestRequest::default()
            .insert_header(ContentType::plaintext())
            .to_request();
        let response = test::call_service(&app, request).await;
        // Testing for a failure here. Notice the !
        assert!(!response.status().is_success());
        let body_bytes = test::read_body(response).await;
        let body_str = std::str::from_utf8(&body_bytes).unwrap();
        assert_eq!(body_str, "invalid utf-8 sequence of 1 bytes from index 1");
    }
}
