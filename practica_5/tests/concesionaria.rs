#[cfg(test)]
mod tests {

    use practica_5::concesionaria::*;

    #[test]
    fn test_calcular_precio() {
        let auto_bmw = Auto::new("BMW", "Serie 3", 2010, 20000.0, Color::Blanco);
        let auto_viejo = Auto::new("Ford", "Focus", 1999, 15000.0, Color::Negro);
        let auto_primario = Auto::new("Fiat", "Uno", 2013, 17000.0, Color::Rojo);

        assert_eq!(auto_bmw.calcular_precio(), 20000.0 * 0.9 * 1.15);
        assert_eq!(auto_viejo.calcular_precio(), 15000.0 * 0.9 * 0.95);
        assert_eq!(auto_primario.calcular_precio(), 17000.0 * 1.25);
    }

    #[test]
    fn test_agregar_auto() {
        let mut concesionario = Concesionaria::new("Concesionario A", "Calle 123", 3);
        let auto1 = Auto::new("Toyota", "Corolla", 2020, 18000.0, Color::Blanco);

        assert!(concesionario.agregar_auto(auto1));
        assert_eq!(concesionario.get_autos().len(), 1);

        let auto2 = Auto::new("BMW", "X5", 2021, 60000.0, Color::Negro);
        let auto3 = Auto::new("Mazda", "CX-5", 2019, 30000.0, Color::Rojo);
        let auto4 = Auto::new("Audi", "Q7", 2018, 50000.0, Color::Azul);

        assert!(concesionario.agregar_auto(auto2));
        assert!(concesionario.agregar_auto(auto3));
        assert!(!concesionario.agregar_auto(auto4)); // supera la capacidad máxima
        assert_eq!(concesionario.get_autos().len(), 3);
    }

    #[test]
    fn test_eliminar_auto() {
        let mut concesionario = Concesionaria::new("Concesionario A", "Calle 123", 3);
        let auto1 = Auto::new("Toyota", "Corolla", 2020, 18000.0, Color::Blanco);
        concesionario.agregar_auto(auto1.clone());

        let auto2 = Auto::new("BMW", "X5", 2021, 60000.0, Color::Negro);
        concesionario.agregar_auto(auto2);

        assert!(concesionario.eliminar_auto(&auto1));
        assert_eq!(concesionario.get_autos().len(), 1);
    }

    #[test]
    fn test_buscar_auto() {
        let mut concesionario = Concesionaria::new("Concesionario A", "Calle 123", 3);
        let auto1 = Auto::new("Toyota", "Corolla", 2020, 18000.0, Color::Blanco);
        concesionario.agregar_auto(auto1.clone());

        assert_eq!(concesionario.buscar_auto(&auto1), Some(&auto1));
        assert_eq!(
            concesionario.buscar_auto(&Auto::new("Honda", "Civic", 2019, 16000.0, Color::Rojo)),
            None
        );
    }

    #[test]
    fn coverage_test() {
        let mut concesionario = Concesionaria::new("Concesionario B", "Calle 456", 2);
        let auto = Auto::new("Toyota", "Camry", 2015, 22000.0, Color::Verde);

        assert_eq!(concesionario.get_autos().len(), 0);
        assert!(concesionario.agregar_auto(auto.clone()));
        assert_eq!(concesionario.buscar_auto(&auto), Some(&auto));
        assert!(concesionario.eliminar_auto(&auto));
        assert_eq!(concesionario.buscar_auto(&auto), None);
    }
}
