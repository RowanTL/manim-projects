use actix_web::{App, HttpServer, Result, web};
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
struct Vector3D {
    x: i64,
    y: i64,
    z: i64,
}

/// deserialize `Vector3D` from request's body
// #[post("/submit")]
async fn submit(vector: web::Json<Vector3D>) -> Result<String> {
    Ok(format!(
        "{}, {}, {}",
        vector.x + 1,
        vector.y + 1,
        vector.z + 1
    ))
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        // limit request size to 4096 kb
        let json_config = web::JsonConfig::default().limit(4096);

        App::new().service(
            web::resource("/submit")
                // change json extractor configuration
                .app_data(json_config)
                .route(web::post().to(submit)),
        )
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
    async fn test_json_extractor() {
        let json_config = web::JsonConfig::default().limit(4096);
        let app = test::init_service(
            App::new().service(
                web::resource("/submit")
                    // change json extractor configuration
                    .app_data(json_config)
                    .route(web::post().to(submit)),
            ),
        )
        .await;
        let request = test::TestRequest::post()
            .uri("/submit")
            .set_json(Vector3D { x: 1, y: 2, z: 3 })
            .to_request();
        let response: Bytes = test::call_and_read_body(&app, request).await;
        assert_eq!(response, Bytes::from("2, 3, 4"));
    }
}
