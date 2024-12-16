<div align="center">
    <h1>Ejercitación 4</h1>
    <h4>Brownie</h4>
</div>

Migrar todos los contratos desarrollados en la [Ejercitación #2](../practica_2) a [brownie](https://github.com/eth-brownie/brownie), y para cada uno de ellos hacer lo siguiente:

1. Generar los scripts de deploy parametrizados según la network y realizar deploy en al menos 1 testnet que no sea local.
1. Generar los scripts de verificación en etherscan y ejecutarlos.
1. Realizar los tests necesarios para alcanzar un coverage de al menos 70%.

## Bitácora

### Ballot

El único problema interesante de notar fue que en `brownie` estaba desactualizada la url de la API de Etherscan, por lo que tuve que modificarla (según explica [este link de SO](https://ethereum.stackexchange.com/a/161122)):

```bash
$ brownie networks modify sepolia explorer=https://api-sepolia.etherscan.io/api
```

El script produjo el siguiente contrato: `0x8Fa6C51A46da988598c3dd38367f13165f0C59e0`.
