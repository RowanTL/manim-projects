use actix_web::{App, Error, FromRequest, HttpRequest, HttpServer, dev::Payload, error, get, web};
use std::pin::Pin;

struct Vector3D {
    x: i64,
    y: i64,
    z: i64,
}

const VECTOR3DSIZE: usize = 24; // 8 bytes (i64) * 3 fields

impl FromRequest for Vector3D {
    type Error = Error;
    type Future = Pin<Box<dyn Future<Output = Result<Self, Error>>>>;

    fn from_request(req: &HttpRequest, payload: &mut Payload) -> Self::Future {
        let payload_future = web::Bytes::from_request(req, payload);

        Box::pin(async move {
            let bytes = payload_future.await?;

            if bytes.len() != VECTOR3DSIZE {
                return Err(error::ErrorBadRequest(format!(
                    "Invalid payload size: expected 24 bytes, got {}",
                    bytes.len()
                )));
            }

            let x = i64::from_be_bytes(bytes[0..8].try_into().unwrap());
            let y = i64::from_be_bytes(bytes[8..16].try_into().unwrap());
            let z = i64::from_be_bytes(bytes[16..24].try_into().unwrap());

            Ok(Vector3D { x, y, z })
        })
    }
}

#[get("/")]
async fn index(vec: Vector3D) -> String {
    format!("{}, {}, {}", vec.x, vec.y, vec.z)
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
    use super::*;
    use actix_web::{App, body::to_bytes, test};
    use bytes::Bytes;

    #[actix_web::test]
    async fn test_custom_extractor_ok() {
        let app = test::init_service(App::new().service(index)).await;
        let x = 1i64;
        let y = 2i64;
        let z = 3i64;

        let mut payload = Vec::new();
        payload.extend_from_slice(&x.to_be_bytes());
        payload.extend_from_slice(&y.to_be_bytes());
        payload.extend_from_slice(&z.to_be_bytes());
        let payload = Bytes::from(payload);

        let req = test::TestRequest::get()
            .uri("/")
            .set_payload(payload)
            .to_request();
        let resp = test::call_service(&app, req).await;

        assert!(resp.status().is_success());
        let body = to_bytes(resp.into_body()).await.unwrap();
        assert_eq!(body, "1, 2, 3");
    }

    #[actix_web::test]
    async fn test_custom_extractor_bad_request() {
        let app = test::init_service(App::new().service(index)).await;

        let payload = Bytes::from("invalid payload");

        let req = test::TestRequest::get()
            .uri("/")
            .set_payload(payload)
            .to_request();
        let resp = test::call_service(&app, req).await;

        assert_eq!(resp.status(), 400);
    }
}
