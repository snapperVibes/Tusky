import click

from main import Discriminator


@click.group()
def cli():
    pass


@click.command()
@click.argument(
    "stop",
)
def bruteforce_seed(stop):
    stop = int(stop)

    def try_seed(seed: int, stop=stop) -> bool:
        d = Discriminator(seed=seed, start=1, stop=stop)
        for actual, expected in zip(d, range(1, stop)):
            if actual != expected:
                return False
        return True

    seed = 0
    while True:
        flag = try_seed(seed, stop)
        if flag:
            break
        seed += 1
    print("Seed: ", seed)


cli.add_command(bruteforce_seed)

if __name__ == "__main__":
    cli()
