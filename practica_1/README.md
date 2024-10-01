<div align="center">
    <h1>Ejercitación 1</h1>
    <h4>Primeros conceptos</h4>
</div>

### Ejercicio 1

- Realice un script que genere una billetera y muestre 2 direcciones de recepción sobre la Testnet de Bitcoin.

  ```bash
  $ python create_wallet.py -h
  usage: create_wallet.py [-h] [--seed SEED]

  Generar una billetera en la Testnet de Bitcoin y mostrar direcciones de recepción.

  options:
    -h, --help   show this help message and exit
    --seed SEED  Frase semilla para restaurar la billetera (opcional)
  ```

- Anote la frase semilla generada.

  ```bash
  $ python create_wallet.py
  INFO: La frase semilla generada es:
              coach first stable current wisdom staff curious company field flat east glove

  INFO: Las direcciones de recepción son:
              tb1qde2whs4eyc8jdwusnmmlkw06a8rvmentwccplp (priv: cVJSYsX5WA72ynyyxpKLBrcaiPTaKwvG4CWAbHH4XDYK4q4cAUdp)
              tb1q5jpgclua0urc8qyfmseff9ap4qpw9fma4996u6 (priv: cUUno5iiR7vVPUCgSTaf5vddWqA8ZM6jarJpkTq1KiQX2t7a5cuY)

  INFO: La primer dirección de cambio es:
              tb1q4kuf834kjck090v53j3m7kfnae4qg2au4q4cts (priv: cUKEx3fujcovpCsUroc6vtKpE4a5JHY4tpKoBdZn2qkL183obqUR)
  ```

- Luego solicite a través de una faucet BTC Test para la primera dirección.

  Usé [Bitcoin Testnet Faucet](https://bitcoinfaucet.uo1.net/) para solicitar _₿ 0.000001_ (100 satoshis) a la dirección `tb1qde2whs4eyc8jdwusnmmlkw06a8rvmentwccplp`.

#### Bitácora

Al principio, creaba la wallet con el método `wallet()` de `Bitcoin`.

```python
>>> wallet: cryptos.Wallet = cryptos.Bitcoin(testnet=True).wallet(seed="seed_phrase")
>>> wallet.new_receiving_address()
'muxqc7c35vSLwSnAnc2jkEvWUuiz588fXk'
```

Sin embargo, al intentar conseguir bitcoins de la faucet, me topaba con el siguiente error:

> "muxqc7c35vSLwSnAnc2jkEvWUuiz588fXk" is not a valid bitcoin testnet address

Después de renegar un rato, vi que todas las direcciones de las transacciones de la faucet empezaban con `tb1`. Ahí me encontré con [este repo](https://github.com/citizen010/bitcoin-prefixes-address-list) que muestra para cada formato de clave, el prefijo de dirección correspondiente.

Revisando la librería, efectivamente usa por defecto en el método `wallet()` el formato `P2PKH` que empieza con `m` o `n`. Todo se solucionó al cambiar el método de generación de la `wallet()`.

```python
>>> wallet: cryptos.Wallet = cryptos.Bitcoin(testnet=True).p2wpkh_wallet(seed=seed_phrase)
>>> wallet.new_receiving_address()
'tb1qde2whs4eyc8jdwusnmmlkw06a8rvmentwccplp'
```

Con esta dirección, pude [solicitar los satoshis a la faucet sin problemas](https://blockexplorer.one/bitcoin/testnet/address/tb1qde2whs4eyc8jdwusnmmlkw06a8rvmentwccplp).

> Transaction of 0.00001 coins to tb1qde2whs4eyc8jdwusnmmlkw06a8rvmentwccplp has been placed into the sending queue. Don't forget to send the testnet coins back when you're done with them.

### Ejercicio 2

- Una vez recibido BTC Test sobre la primera dirección, realice otro script que restaure una billetera desde las palabras generadas en el punto anterior.

  ```bash
  $ python transfer.py -h
  usage: transfer.py [-h] --from-priv FROM_PRIV --to-addr TO_ADDR [--change CHANGE] --amount AMOUNT [--fee-rate FEE_RATE] --seed SEED

  Realizar una transferencia entre dos direcciones en la Testnet de Bitcoin.

  options:
    -h, --help            show this help message and exit
    --from-priv FROM_PRIV
                          Clave privada de la dirección de origen
    --to-addr TO_ADDR     Dirección de destino
    --change CHANGE       Dirección de cambio
    --amount AMOUNT       Cantidad de Bitcoin a transferir
    --fee-rate FEE_RATE   Tasa de comisión
    --seed SEED           Frase semilla de la billetera
  ```

- Luego envíe 20 satoshis desde la primera dirección (que tiene BTC Test) a la segunda dirección.

#### Bitácora

Acá tuve problemas con 2 cosas:

- Obtener la clave privada de la dirección de origen.

  Estaba intentando no usar la clave privada directamente, sino obtenerla a partir de la dirección y la frase semilla. Cuando no pude intenté lo contrario, usar solo la privada y recuperar la dirección de origen. Esto último sí es más factible, pero sigue siendo un problema. Por defecto la librería sigue usando el prefijo incorrecto a la hora de devolver direcciones, o sea que no me daba el formato de address correcto. Para no hardcodear el prefijo ni asumir que siempre la transacción se envía de la primera dirección o algo así, pido ambas cosas por parámetro.

- Mandar la transacción (`TODO`)

  Sigue en `TODO` porque me comieron tiempo errores tontos de tipos (value era float y no int...). Igualmente, ahora tengo un rango de errores que va desde el timeout, fondos insuficientes, y el infame:

    > aiorpcx.jsonrpc.ProtocolError: (-32600, 'ill-formed response error object: sendrawtransaction RPC error: {"code":-26,"message":"dust"}')
