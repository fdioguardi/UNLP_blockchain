#[derive(PartialEq, Clone, Debug)]
pub enum Color {
    Rojo,
    Verde,
    Azul,
    Amarillo,
    Blanco,
    Negro,
}

#[derive(PartialEq, Clone, Debug)]
pub struct Auto {
    marca: String,
    modelo: String,
    año: u16,
    precio_bruto: f64,
    color: Color,
}

pub struct Concesionaria {
    nombre: String,
    direccion: String,
    capacidad_max: usize,
    autos: Vec<Auto>,
}

impl Auto {
    pub fn new(marca: &str, modelo: &str, año: u16, precio_bruto: f64, color: Color) -> Self {
        Auto {
            marca: marca.to_string(),
            modelo: modelo.to_string(),
            año,
            precio_bruto,
            color,
        }
    }

    pub fn calcular_precio(&self) -> f64 {
        let mut precio = self.precio_bruto;

        match self.color {
            Color::Rojo | Color::Azul | Color::Amarillo => {
                precio *= 1.25;
            }
            _ => {
                precio *= 0.9;
            }
        }

        if self.marca.to_uppercase() == "BMW" {
            precio *= 1.15;
        }

        if self.año < 2000 {
            precio *= 0.95;
        }

        precio
    }
}

impl Concesionaria {
    pub fn new(nombre: &str, direccion: &str, capacidad_max: usize) -> Self {
        Concesionaria {
            nombre: nombre.to_string(),
            direccion: direccion.to_string(),
            capacidad_max,
            autos: Vec::new(),
        }
    }

    pub fn agregar_auto(&mut self, auto: Auto) -> bool {
        if self.autos.len() < self.capacidad_max {
            self.autos.push(auto);
            true
        } else {
            false
        }
    }

    pub fn eliminar_auto(&mut self, auto: &Auto) -> bool {
        if let Some(pos) = self.autos.iter().position(|a| a == auto) {
            self.autos.remove(pos);
            true
        } else {
            false
        }
    }

    pub fn buscar_auto(&self, auto: &Auto) -> Option<&Auto> {
        self.autos.iter().find(|&a| a == auto)
    }

    pub fn get_autos(&self) -> &Vec<Auto> {
        &self.autos
    }
}
