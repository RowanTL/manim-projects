use actix_web::{
    App, HttpResponse, HttpServer, error, get,
    http::{StatusCode, header::ContentType},
};
use derive_more::derive::{Display, Error};

#[derive(Debug, Display, Error)]
enum MyError {
    // display macro from derive_more crate
    #[display("internal error")]
    InternalError,

    #[display("bad request")]
    BadClientData,

    #[display("timeout")]
    Timeout,
}

impl error::ResponseError for MyError {
    fn error_response(&self) -> HttpResponse {
        HttpResponse::build(self.status_code())
            .insert_header(ContentType::html())
            .body(self.to_string())
    }

    fn status_code(&self) -> StatusCode {
        match *self {
            MyError::InternalError => StatusCode::INTERNAL_SERVER_ERROR,
            MyError::BadClientData => StatusCode::BAD_REQUEST,
            MyError::Timeout => StatusCode::GATEWAY_TIMEOUT,
        }
    }
}

#[get("/bad")]
async fn bad_client() -> Result<&'static str, MyError> {
    Err(MyError::BadClientData)
}

#[get("/internal")]
async fn internal_error() -> Result<&'static str, MyError> {
    Err(MyError::InternalError)
}

#[get("/timeout")]
async fn timeout() -> Result<&'static str, MyError> {
    Err(MyError::Timeout)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .service(bad_client)
            .service(timeout)
            .service(internal_error)
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}

#[cfg(test)]
mod tests {
    use actix_web::{App, http::header::ContentType, test};

    use super::*;

    #[actix_web::test]
    async fn test_custom_bad_client() {
        let app = test::init_service(
            App::new()
                .service(bad_client)
                .service(timeout)
                .service(internal_error),
        )
        .await;
        let request = test::TestRequest::default()
            .uri("/bad")
            .insert_header(ContentType::plaintext())
            .to_request();
        let response = test::call_service(&app, request).await;
        assert!(!response.status().is_success());
        let body_bytes = test::read_body(response).await;
        let body_str = std::str::from_utf8(&body_bytes).unwrap();
        assert_eq!(body_str, "bad request");
    }

    #[actix_web::test]
    async fn test_custom_timeout() {
        let app = test::init_service(
            App::new()
                .service(bad_client)
                .service(timeout)
                .service(internal_error),
        )
        .await;
        let request = test::TestRequest::default()
            .uri("/timeout")
            .insert_header(ContentType::plaintext())
            .to_request();
        let response = test::call_service(&app, request).await;
        assert!(!response.status().is_success());
        let body_bytes = test::read_body(response).await;
        let body_str = std::str::from_utf8(&body_bytes).unwrap();
        assert_eq!(body_str, "timeout");
    }

    #[actix_web::test]
    async fn test_custom_internal_error() {
        let app = test::init_service(
            App::new()
                .service(bad_client)
                .service(timeout)
                .service(internal_error),
        )
        .await;
        let request = test::TestRequest::default()
            .uri("/internal")
            .insert_header(ContentType::plaintext())
            .to_request();
        let response = test::call_service(&app, request).await;
        assert!(!response.status().is_success());
        let body_bytes = test::read_body(response).await;
        let body_str = std::str::from_utf8(&body_bytes).unwrap();
        assert_eq!(body_str, "internal error");
    }
}
