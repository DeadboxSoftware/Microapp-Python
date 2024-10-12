import argparse
import sys
import asyncio

parser = argparse.ArgumentParser(add_help=False)

class MyAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if option_string:
            attr = True if values else False
            setattr(namespace, self.dest, attr)
        if hasattr(namespace, 'command'):
            current_values = getattr(namespace, 'command')
            try:
                current_values.extend(values)
            except AttributeError:
                current_values = values
            finally:
                setattr(namespace, 'command', current_values)
        else:
            setattr(namespace, 'command', values)

# https://stackoverflow.com/a/31347222
parser.add_argument('command', nargs='+', action=MyAction)
parser.add_argument('-h', dest='help', action='store_true', required=False)
parser.add_argument('--email', type=str, dest='email', required=False)
parser.add_argument('--user', type=str, dest='user', required=False)
parser.add_argument('--password', type=str, dest='password', required=False)

def print_help():
    print("""""")


if len(sys.argv) == 1:
    print("testing")
    print_help()
elif len(sys.argv) > 1 and sys.argv[1] == '-h':
    print_help()
else:
    args = parser.parse_args()
    command = args.command[0]
    if command == 'migrate':
        from modules.bash import run_bash_command
        run_bash_command("alembic upgrade head")
        print("migrate")
    elif command == "seed":
        print("seed")
    elif command == "newuser":
        from database import get_db
        from controllers.user import create_user
        if args.email and args.password:
            print("CREATING USER")
            async def handle_new_user():
                async for db in get_db():
                    result = await create_user(
                        db, 
                        email=args.email, 
                        password=args.password
                    )
                    print(result)
            asyncio.run(handle_new_user())