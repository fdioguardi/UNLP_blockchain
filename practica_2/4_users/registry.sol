// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

/*
 * Registro de usuarios: implemente un contrato principal que actúe como un registro de usuarios.
 * Permita que los usuarios se registren con su dirección y un nombre de usuario.
 * Luego implemente un contrato secundario que actúe como un muro de mensajes, donde los usuarios
 * registrados en el contrato principal pueden dejar mensajes.
 * Asegúrese de que solo los usuarios registrados puedan dejar mensajes en el muro.
 */

import {User} from "./user.sol";

contract UserRegistry {
    mapping(address => User) public users;

    event UserRegistered(address indexed _address, string _username);

    function register(string calldata username) public {
        require(bytes(username).length > 0, "Username cannot be empty");
        require(
            users[msg.sender]._address == address(0),
            "User is already registered"
        );

        users[msg.sender] = User({_address: msg.sender, _username: username});
    }

    function isUser(address _address) public view returns (bool) {
        return users[_address]._address != address(0);
    }
}
