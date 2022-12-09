import click

@click.command
@click.argument('message1')
@click.argument('message2')
@click.option('--count', default=1, help='Number of messages')
def test(message1, message2, count):
   for _ in range(count):
       print(f'{message1=} - {message2=}')

if __name__ == "__main__":
   test()
