pub struct Persona {
    pub nombre: String,
    pub edad: u8,
    pub direccion: Option<String>,
}

impl Persona {
    pub fn new(nombre: &str, edad: u8, direccion: Option<&str>) -> Persona {
        Persona {
            nombre: nombre.to_string(),
            edad,
            direccion: direccion.map(|d| d.to_string()),
        }
    }

    pub fn imprimir(&self) {
        println!(
            "Nombre: {}, Edad: {}, Dirección: {}",
            self.nombre,
            self.edad,
            self.direccion.as_deref().unwrap_or("No especificada")
        );
    }

    pub fn obtener_edad(&self) -> u8 {
        self.edad
    }

    pub fn actualizar_direccion(&mut self, nueva_direccion: Option<&str>) {
        self.direccion = nueva_direccion.map(|d| d.to_string());
    }
}

pub fn main() {
    let mut persona = Persona::new("Juan", 25, Some("Calle 123"));
    persona.imprimir();
    persona.actualizar_direccion(Some("Calle 456"));
    persona.imprimir();
}
