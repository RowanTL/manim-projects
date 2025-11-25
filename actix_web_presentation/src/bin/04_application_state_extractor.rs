use actix_web::{App, HttpServer, Responder, web};
use std::cell::Cell;

#[derive(Clone)]
struct AppState {
    count: Cell<usize>,
}

async fn show_count(data: web::Data<AppState>) -> impl Responder {
    format!("count: {}", data.count.get())
}

async fn add_one(data: web::Data<AppState>) -> impl Responder {
    let count = data.count.get();
    data.count.set(count + 1);

    format!("count: {}", data.count.get())
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let data = AppState {
        count: Cell::new(0),
    };

    HttpServer::new(move || {
        App::new()
            .app_data(web::Data::new(data.clone()))
            .route("/", web::to(show_count))
            .route("/add", web::to(add_one))
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}

#[cfg(test)]
mod tests {
    use actix_web::{App, test};
    use bytes::Bytes; // library created & used by tokio-rs

    use super::*;

    #[actix_web::test]
    async fn test_app_state_extractor() {
        let data = AppState {
            count: Cell::new(0),
        };
        let app = test::init_service(
            App::new()
                .app_data(web::Data::new(data.clone()))
                .route("/", web::to(show_count))
                .route("/add", web::to(add_one)),
        )
        .await;
        let request = test::TestRequest::get().uri("/").to_request();
        let response: Bytes = test::call_and_read_body(&app, request).await;
        assert_eq!(response, Bytes::from("count: 0"));

        let request = test::TestRequest::get().uri("/add").to_request();
        let response: Bytes = test::call_and_read_body(&app, request).await;
        assert_eq!(response, Bytes::from("count: 1"));

        let request = test::TestRequest::get().uri("/").to_request();
        let response: Bytes = test::call_and_read_body(&app, request).await;
        assert_eq!(response, Bytes::from("count: 1"));
    }
}
