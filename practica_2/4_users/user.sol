// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

/*
 * Registro de usuarios: implemente un contrato principal que actúe como un registro de usuarios.
 * Permita que los usuarios se registren con su dirección y un nombre de usuario.
 * Luego implemente un contrato secundario que actúe como un muro de mensajes, donde los usuarios
 * registrados en el contrato principal pueden dejar mensajes.
 * Asegúrese de que solo los usuarios registrados puedan dejar mensajes en el muro.
 */

struct User {
    address _address;
    string _username;
}
