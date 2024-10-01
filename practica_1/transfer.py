import argparse
import logging
import cryptos

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)

COIN: cryptos.Bitcoin = cryptos.Bitcoin(testnet=True)


def transfer(
    wallet: cryptos.Wallet,
    from_priv: str,
    to_addr: str,
    change_addr: str,
    amount: int,
    fee_rate: float,
) -> None:
    from_addr: str = addr_from_priv(wallet, from_priv)
    logger.info(f"Enviando {amount} BTC desde {from_addr} hacia {to_addr}")

    breakpoint()
    COIN.send(
        privkey=from_priv,
        frm=from_addr,
        to=change_addr,
        value=amount,
        change_addr=to_addr,
        fee=int(amount * fee_rate),
    )


def addr_from_priv(wallet: cryptos.Wallet, privkey: str) -> str:
    return str(wallet.pubtoaddr(COIN.privtopub(privkey)))


def restore_wallet(seed_phrase: str) -> cryptos.Wallet:
    return COIN.p2wpkh_wallet(seed=seed_phrase)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Realizar una transferencia entre dos direcciones en la Testnet de Bitcoin."
    )

    parser.add_argument(
        "--from-priv",
        type=str,
        required=True,
        help="Clave privada de la dirección de origen",
    )
    parser.add_argument(
        "--to-addr", type=str, required=True, help="Dirección de destino"
    )
    parser.add_argument(
        "--change", type=str, required=False, help="Dirección de cambio"
    )
    parser.add_argument(
        "--amount", type=float, required=True, help="Cantidad de Bitcoin a transferir"
    )
    parser.add_argument(
        "--fee-rate", type=float, required=False, help="Tasa de comisión", default=0.1
    )

    parser.add_argument(
        "--seed", type=str, required=True, help="Frase semilla de la billetera"
    )

    args: argparse.Namespace = parser.parse_args()

    wallet: cryptos.Wallet = restore_wallet(args.seed)

    from_addr: str = addr_from_priv(wallet, args.from_priv)
    change_addr: str = args.change if args.change else str(wallet.new_change_address())

    logger.info(
        f"Iniciando transferencia de {args.amount} BTC desde {from_addr} hacia {args.to_addr}"
    )

    transfer(
        wallet,
        args.from_priv,
        args.to_addr,
        change_addr,
        args.amount,
        args.fee_rate,
    )

    for addr in [from_addr, args.to_addr, change_addr]:
        balance: int = COIN.balance(addr)
        logger.info(f"Saldo de {addr}: {balance} BTC")


if __name__ == "__main__":
    main()
