from read_transport import Reader
from Blocker import Host
from utils import Regex as lex
from read_transport import Reader
# from consolemenu import *
# from consolemenu.items import *

def main():
    host = Host()
    parser = host.argument_handler(host.get_host_file())
    args = parser.parse_args()

    # if args.menu:
    #     mainMenu = ConsoleMenu("SpiderWeb", "Sniffer/Blocker")
    #     menu_item = MenuItem("Menu Item")
    #     function_item = FunctionItem("Call a python function", input, ["enter input"])
    #     selection_menu = SelectionMenu(["item1", "item2", "item3"])
    #     submenu_item = SubmenuItem("Submenu item", selection_menu, mainMenu)
    #     mainMenu.append_item(menu_item)
    #     mainMenu.append_item(function_item)
    #     mainMenu.append_item(submenu_item)
    #     mainMenu.show()

    # handles arguments
    # this arg lists all the entries in the host file
    if args.list:
        content = host.list_hosts_file()
        lex.output_highlight('# Search result:')
        result = host.host_exists(*args.check)
        lex.output_highlight(*result)
    # this arg inserts a given entry to the hosts file
    elif args.insert:
        lex.output_highlight('# Insert mapping:')
        for each in args.insert:
            # splts each arg by colon
            arg = each.split(':')
            result = host.append_host(*arg)
            if result:
                lex.output_highlight('inserted ' + each)
            else:
                lex.output_highlight('failed to insert ' + each)
    # removes arg from hosts file
    elif args.remove:
        lex.output_highlight('# Remove mapping:')
        for each in args.remove:
            result = host.remove(each)
            if result:
                lex.output_highlight('removed ' + each)
            else:
                lex.output_highlight('not found ' + each)
    # starts sniffing process
    elif args.sniff:
        sniffer = Reader()
        pkts = sniffer.packet_sniffer()
        lex.output_highlight("\n".join(sniffer.sorter(True)))

    else:
        # prints help
        parser.print_help()


if __name__ == '__main__':
    main()
