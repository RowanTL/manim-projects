use actix_web::{App, HttpServer, Result, get, web};

/// extract path info from "/users/{user_id}/{friend}" url
/// {user_id} - deserializes to a u32
/// {friend} - deserializes to a String
#[get("/users/{user_id}/{friend}")]
async fn index(path: web::Path<(u32, String)>) -> Result<String> {
    // This is not a std rust Result return type!
    let (user_id, friend) = path.into_inner();
    Ok(format!("Welcome {}, user_id {}!", friend, user_id))
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
    async fn test_path_extractor() {
        let app = test::init_service(App::new().service(index)).await;
        let request = test::TestRequest::get().uri("/users/1/jerry").to_request();
        let response = test::call_service(&app, request).await;
        let res_body = response.into_body();
        assert_eq!(
            res_body.try_into_bytes().unwrap(),
            Bytes::from("Welcome jerry, user_id 1!")
        );
    }
}
