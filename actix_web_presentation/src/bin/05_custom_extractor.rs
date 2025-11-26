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
