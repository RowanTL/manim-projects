use actix_web::{App, HttpServer, get, web};

#[get("/string")]
async fn string_response() -> String {
    String::from("This is a body")
}

#[get("/static_str")]
async fn static_str_response() -> &'static str {
    "This is a body"
}

#[get("/static_str")]
async fn vec_u8_response() -> Vec<u8> {
    vec![1, 2, 3, 4, 5]
}

// #[get("/cow")]
// async fn cow_response() -> Cow<'_, str> {
//     let cow_str = Cow::Owned("moo?");
//     cow_str
// }

#[get("/bytes")]
async fn bytes_response() -> web::Bytes {
    web::Bytes::from("123")
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .service(string_response)
            .service(static_str_response)
            .service(vec_u8_response)
            .service(bytes_response)
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}

// Thank you gemini
#[cfg(test)]
mod tests {
    use super::*;
    use actix_web::{App, test};

    #[actix_web::test]
    async fn test_string_response() {
        let app = test::init_service(App::new().service(string_response)).await;
        let req = test::TestRequest::get().uri("/string").to_request();
        let resp = test::call_service(&app, req).await;
        assert!(resp.status().is_success());
        let body = test::read_body(resp).await;
        assert_eq!(body, web::Bytes::from_static(b"This is a body"));
    }

    #[actix_web::test]
    async fn test_static_str_response() {
        let app = test::init_service(App::new().service(static_str_response)).await;
        let req = test::TestRequest::get().uri("/static_str").to_request();
        let resp = test::call_service(&app, req).await;
        assert!(resp.status().is_success());
        let body = test::read_body(resp).await;
        assert_eq!(body, web::Bytes::from_static(b"This is a body"));
    }

    #[actix_web::test]
    async fn test_vec_u8_response() {
        let app = test::init_service(App::new().service(vec_u8_response)).await;
        let req = test::TestRequest::get().uri("/vec_u8").to_request();
        let resp = test::call_service(&app, req).await;
        assert!(resp.status().is_success());
        let body = test::read_body(resp).await;
        assert_eq!(body, web::Bytes::from(vec![1, 2, 3, 4, 5]));
    }

    #[actix_web::test]
    async fn test_bytes_response() {
        let app = test::init_service(App::new().service(bytes_response)).await;
        let req = test::TestRequest::get().uri("/bytes").to_request();
        let resp = test::call_service(&app, req).await;
        assert!(resp.status().is_success());
        let body = test::read_body(resp).await;
        assert_eq!(body, web::Bytes::from_static(b"123"));
    }
}
