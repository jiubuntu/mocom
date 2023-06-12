import click
from parse import NAVER

@click.command()
@click.option('--keyword', prompt='keyword', help='keyword for search')
def cli( keyword ):
    gNAVER = NAVER()
    gNAVER.parse( keyword )

if __name__ == '__main__':
    cli()