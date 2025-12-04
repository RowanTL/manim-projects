use actix_web::{App, HttpResponse, HttpServer, guard, web};

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .service(
                web::scope("/")
                    .guard(guard::Header("x-guarded", "secret"))
                    .route(
                        "",
                        web::to(|| async { HttpResponse::Ok().body("this is the secret") }),
                    ),
            )
            .service(
                web::scope("/")
                    .guard(guard::Header("arbitrary-header", "value"))
                    .route(
                        "",
                        web::to(|| async {
                            HttpResponse::Ok().body("value from arbitrary header")
                        }),
                    ),
            )
            // returns a "" to the user
            .route("/", web::to(HttpResponse::Ok))
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}

// Thank you gemini
#[cfg(test)]
mod tests {
    use actix_web::{App, HttpResponse, guard, test, web};

    #[actix_web::test]
    async fn test_application_guards() {
        // Initialize the service with the exact logic provided
        let app = test::init_service(
            App::new()
                .service(
                    web::scope("/")
                        .guard(guard::Header("x-guarded", "secret"))
                        .route(
                            "",
                            web::to(|| async { HttpResponse::Ok().body("this is the secret") }),
                        ),
                )
                .service(
                    web::scope("/")
                        .guard(guard::Header("arbitrary-header", "value"))
                        .route(
                            "",
                            web::to(|| async {
                                HttpResponse::Ok().body("value from arbitrary header")
                            }),
                        ),
                )
                // Fallback route
                .route("/", web::to(HttpResponse::Ok)),
        )
        .await;

        // TEST 1: Verify the "x-guarded" secret route
        let req = test::TestRequest::get()
            .uri("/")
            .insert_header(("x-guarded", "secret"))
            .to_request();

        let resp = test::call_service(&app, req).await;
        assert!(resp.status().is_success());
        let body = test::read_body(resp).await;
        assert_eq!(body, "this is the secret");

        // TEST 2: Verify the "arbitrary-header" route
        let req = test::TestRequest::get()
            .uri("/")
            .insert_header(("arbitrary-header", "value"))
            .to_request();

        let resp = test::call_service(&app, req).await;
        assert!(resp.status().is_success());
        let body = test::read_body(resp).await;
        assert_eq!(body, "value from arbitrary header");

        // TEST 3: Verify the fallback route (no headers or wrong headers)
        let req = test::TestRequest::get().uri("/").to_request();

        let resp = test::call_service(&app, req).await;
        assert!(resp.status().is_success());
        let body = test::read_body(resp).await;
        // The fallback route uses HttpResponse::Ok (builder), which returns an empty body
        assert_eq!(body, "");

        // TEST 4: Verify fallback works when headers are wrong
        let req = test::TestRequest::get()
            .uri("/")
            .insert_header(("x-guarded", "wrong-password"))
            .to_request();

        let resp = test::call_service(&app, req).await;
        assert!(resp.status().is_success());
        let body = test::read_body(resp).await;
        assert_eq!(body, ""); // Should fall through to the default route
    }
}
