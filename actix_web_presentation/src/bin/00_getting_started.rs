use actix_web::{App, HttpResponse, HttpServer, Responder, get, post, web};

#[get("/")]
async fn hello() -> impl Responder {
    HttpResponse::Ok().body("Hello world!")
}

#[post("/echo")]
async fn echo(req_body: String) -> impl Responder {
    HttpResponse::Ok().body(req_body)
}

async fn manual_hello() -> impl Responder {
    HttpResponse::Ok().body("Hey there!")
}

async fn all_users() -> impl Responder {
    HttpResponse::Ok().body("All users!")
}

async fn user_info() -> impl Responder {
    HttpResponse::Ok().body("Info on users!")
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .service(
                web::scope("/users")
                    .route("/all", web::get().to(all_users))
                    .route("/info", web::get().to(user_info)),
            )
            .service(echo)
            .route("/hey", web::get().to(manual_hello))
    })
    .workers(4) // set amount of workers
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}

#[cfg(test)]
mod tests {
    use actix_web::{App, http::header::ContentType, test};

    use super::*;

    #[actix_web::test]
    async fn test_getting_started_get() {
        let app = test::init_service(App::new().service(hello)).await;
        let request = test::TestRequest::default()
            .insert_header(ContentType::plaintext())
            .to_request();
        let response = test::call_service(&app, request).await;
        assert!(response.status().is_success());
        let body_bytes = test::read_body(response).await;
        let body_str = std::str::from_utf8(&body_bytes).unwrap();
        assert_eq!(body_str, "Hello world!");
    }

    #[actix_web::test]
    async fn test_getting_started_scope_all_get() {
        let app = test::init_service(
            App::new().service(web::scope("/users").route("/all", web::get().to(all_users))),
        )
        .await;
        let request = test::TestRequest::default()
            .uri("/users/all")
            .insert_header(ContentType::plaintext())
            .to_request();
        let response = test::call_service(&app, request).await;
        assert!(response.status().is_success());
        let body_bytes = test::read_body(response).await;
        let body_str = std::str::from_utf8(&body_bytes).unwrap();
        assert_eq!(body_str, "All users!");
    }

    #[actix_web::test]
    async fn test_getting_started_scope_info_get() {
        let app = test::init_service(
            App::new().service(web::scope("/users").route("/info", web::get().to(user_info))),
        )
        .await;
        let request = test::TestRequest::default()
            .uri("/users/info")
            .insert_header(ContentType::plaintext())
            .to_request();
        let response = test::call_service(&app, request).await;
        assert!(response.status().is_success());
        let body_bytes = test::read_body(response).await;
        let body_str = std::str::from_utf8(&body_bytes).unwrap();
        assert_eq!(body_str, "Info on users!");
    }
}
