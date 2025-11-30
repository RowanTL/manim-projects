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
