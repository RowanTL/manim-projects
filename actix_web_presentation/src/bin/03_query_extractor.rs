use actix_web::{App, HttpServer, get, web};
use serde::Deserialize;

#[derive(Deserialize)]
struct Info {
    username: String,
}

#[derive(Deserialize)]
struct Address {
    street_name: String,
    zip_code: u32,
}

// this handler gets called if the query deserializes into `Info` successfully
// otherwise a 400 Bad Request error response is returned
#[get("/")]
async fn index(info: web::Query<Info>) -> String {
    format!("Welcome {}!", info.username)
}

#[get("/address")]
async fn addr(address: web::Query<Address>) -> String {
    format!(
        "Street Name: {}, Zip Code: {}",
        address.street_name, address.zip_code
    )
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
    use actix_web::{App, body::MessageBody, test};
    use bytes::Bytes; // library created & used by tokio-rs

    use super::*;

    #[actix_web::test]
    async fn test_query_extractor_info() {
        let app = test::init_service(App::new().service(index)).await;
        let request = test::TestRequest::get()
            .uri("/?username=rowan")
            .to_request();
        let response = test::call_service(&app, request).await;
        let res_body = response.into_body();
        assert_eq!(
            res_body.try_into_bytes().unwrap(),
            Bytes::from("Welcome rowan!")
        );
    }

    #[actix_web::test]
    async fn test_query_extractor_address() {
        let app = test::init_service(App::new().service(addr)).await;
        let request = test::TestRequest::get()
            .uri("/address?street_name=Bowles&zip_code=63026")
            .to_request();
        let response = test::call_service(&app, request).await;
        let res_body = response.into_body();
        assert_eq!(
            res_body.try_into_bytes().unwrap(),
            Bytes::from("Street Name: Bowles, Zip Code: 63026")
        );
    }
}
