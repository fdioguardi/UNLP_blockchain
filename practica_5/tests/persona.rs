use practica_5::persona::Persona;

#[test]
fn test_creacion_persona() {
    let persona = Persona::new("Alice", 30, Some("123 Calle Principal"));
    assert_eq!(persona.nombre, "Alice");
    assert_eq!(persona.edad, 30);
    assert_eq!(persona.direccion.as_deref(), Some("123 Calle Principal"));
}

#[test]
fn test_persona_sin_direccion() {
    let persona = Persona::new("Bob", 25, None);
    assert_eq!(persona.nombre, "Bob");
    assert_eq!(persona.edad, 25);
    assert!(persona.direccion.is_none());
}

#[test]
fn test_obtener_edad() {
    let persona = Persona::new("Charlie", 40, Some("456 Another St"));
    assert_eq!(persona.obtener_edad(), 40);
}

#[test]
fn test_actualizar_direccion() {
    let mut persona = Persona::new("Dana", 28, None);
    persona.actualizar_direccion(Some("789 New Ave"));
    assert_eq!(persona.direccion.as_deref(), Some("789 New Ave"));

    persona.actualizar_direccion(None);
    assert!(persona.direccion.is_none());
}

#[test]
fn test_imprimir() {
    let persona = Persona::new("Eve", 35, Some("1010 Hidden Rd"));
    persona.imprimir(); // Validate no errors on execution
}
