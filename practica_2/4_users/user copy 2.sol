// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

/*
 * Registro de usuarios: implemente un contrato principal que actúe como un registro de usuarios.
 * Permita que los usuarios se registren con su dirección y un nombre de usuario.
 * Luego implemente un contrato secundario que actúe como un muro de mensajes, donde los usuarios
 * registrados en el contrato principal pueden dejar mensajes.
 * Asegúrese de que solo los usuarios registrados puedan dejar mensajes en el muro.
 */

import {UserRegistry} from "./registry.sol";

struct Message {
    address from;
    string content;
    uint256 timestamp;
}

contract MessageBoard {
    UserRegistry public registry;
    Message[] public messages;

    constructor(address _userRegistry) {
        registry = UserRegistry(_userRegistry);
    }

    function postMessage(string calldata message) public {
        require(registry.isUser(msg.sender), "User is not registered");
        require(bytes(message).length > 0, "Message content cannot be empty");

        messages.push(
            Message({
                from: msg.sender,
                content: message,
                timestamp: block.timestamp
            })
        );
    }
}
