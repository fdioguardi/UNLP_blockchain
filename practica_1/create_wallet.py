import argparse
import os
import cryptos
import logging

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


def create_wallet(seed_phrase=None) -> cryptos.Wallet:
    """
    Crea o restaura una billetera de Bitcoin en la Testnet.

    Args:
        seed_phrase (str, optional): Frase semilla para restaurar la billetera.

    Returns:
        cryptos.Wallet: Billetera de Bitcoin en la Testnet.
    """
    if seed_phrase:
        logger.debug(f"Restaurando billetera con frase semilla: {seed_phrase}")
    else:
        logger.debug("Creando nueva frase semilla")
        seed_phrase = cryptos.entropy_to_words(os.urandom(16))
        logger.info(f"""La frase semilla generada es:
            {seed_phrase}
        """)

    wallet: cryptos.Wallet = cryptos.Bitcoin(testnet=True).p2wpkh_wallet(
        seed=seed_phrase
    )

    logger.info(
        f"La billetera fue creada exitosamente con la frase semilla: {seed_phrase}"
    )

    first = wallet.new_receiving_address()
    change = wallet.new_change_address()
    second = wallet.new_receiving_address()

    logger.info(f"""Las direcciones de recepción son:
            {first} (priv: {wallet.privkey(first)})
            {second} (priv: {wallet.privkey(second)})
    """)
    logger.info(f"""La primer dirección de cambio es:
            {change} (priv: {wallet.privkey(change)})
    """)

    return wallet


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generar una billetera en la Testnet de Bitcoin y mostrar direcciones de recepción."
    )

    parser.add_argument(
        "--seed", type=str, help="Frase semilla para restaurar la billetera (opcional)"
    )

    args: argparse.Namespace = parser.parse_args()

    create_wallet(seed_phrase=args.seed)


if __name__ == "__main__":
    main()
