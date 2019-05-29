from read_transport import Reader
from Blocker import Host
from utils import Regex as lex

from consolemenu import *
from consolemenu.items import *

def main():
    host = Host()
    parser = host.argument_handler(host.get_host_file())
    args = parser.parse_args()

    if args.menu:
        mainMenu = ConsoleMenu("SpiderWeb", "Sniffer/Blocker")
        menu_item = MenuItem("Menu Item")
        function_item = FunctionItem("Call a python function", input, ["enter input"])
        selection_menu = SelectionMenu(["item1", "item2", "item3"])
        submenu_item = SubmenuItem("Submenu item", selection_menu, mainMenu)
        mainMenu.append_item(menu_item)
        mainMenu.append_item(function_item)
        mainMenu.append_item(submenu_item)
        mainMenu.show()

    elif args.list:
        content = host.list_hosts_file()
        lex.output_highlight('# Search result:')
        result = host.check_exist(*args.check)
        lex.output_highlight(*result)
    elif args.insert:
        lex.output_highlight('# Insert mapping:')
        for each in args.insert:
            arg = each.split(':')
            result = host.append_host(*arg)
            if result[0]:
                lex.output_highlight('inserted ' + each)
            else:
                lex.output_highlight('failed to insert ' + each)
    elif args.remove:
        lex.output_highlight('# Remove mapping:')
        for each in args.remove:
            result = host.remove(each)
            if result[0]:
                lex.output_highlight('removed ' + each)
            else:
                lex.output_highlight('not found ' + each)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()

