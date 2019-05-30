from utils import Host_OS, Regex
import argparse

class Host:
    def __init__(self):
        platform = Host_OS()
        self.platform = platform
        # this section sets the hosts file location according to the OS
        if platform.is_linux() or platform.is_mac():
            self.hostsFile = "/etc/hosts"
        elif platform.is_windows():
            self.hostsFile = r'c:\windows\system32\drivers\etc\hosts'
        else:
            self.hostsFile = '/etc/hosts'
    # lists all entries in hosts file
    def list_hosts_file(self):
        with open(self.hostsFile, 'r') as f:
            return [line.strip() for line in f]
    # checks if host exists
    def host_exists(self, hostname, ip=None):
        with open(self.hostsFile, 'r') as f:
            for line in list(f):
                segment = line.split()
                if line.startswith('#') or line == '\n':
                    continue
                if hostname in segment[1:] and (ip is None or ip == segment[0]):
                    return True
                else:
                    return False
    # windows specific host file confirguration
    def _split_row(self, host_names):
        return self.platform.is_windows() and len(host_names) >= 9
    # appends host to the end of the hosts file with a default of blocking
    def append_host(self, hostname, ip='127.0.0.1'):
        if self.host_exists(hostname, ip):
            return False, None

        done = False
        lines = self._get_file_lines()

        with open(self.hostsFile, 'w') as output:
            for line in lines:
                if line.startswith('#') or line == '\n':
                    output.write(line.strip() + '\n')
                else:
                    segment = line.split()
                    if ip == segment[0] and not self._split_row(segment[1:]) and not done:
                        segment.append(hostname)
                        done = True

                    output.write(segment[0])
                    output.write('\t')
                    output.write(' '.join(segment[1:]))
                    output.write('\n')
            if not done:
                output.write(ip)
                output.write('\t')
                output.write(hostname)
                output.write('\n')
        return True
    # removes host file if found
    def remove(self, hostname):
        if not self.host_exists(hostname):
            return False, None

        found = False

        lines = self._get_file_lines()
        with open(self.hostsFile, 'w') as output:
            for line in lines:
                segment = line.split()

                if line.startswith('#') or line == '\n':
                    output.write(line)
                elif len(segment) == 2 and hostname == segment[1]:
                    found = True
                    continue
                elif len(segment) >= 2 and hostname in segment[1:]:
                    found = True
                    segment.remove(hostname)
                    output.write(segment[0])
                    output.write('\t')
                    output.write(' '.join(segment[1:]))
                    output.write('\n')
                else:
                    output.write(line)
        return found
    # enables option to read hosts to be blocked from a file
    def _get_file_lines(self):
        with open(self.hostsFile, 'r') as input:
            lines = input.readlines()
            return lines
    # retrieves hosts file
    def get_host_file(self):
        return self.hostsFile

    #handles arguments
    @staticmethod
    def argument_handler(file_path):
        parser = argparse.ArgumentParser(description='block certain hosts in hosts file',
                                         epilog='hosts location: ' + file_path)
        group = parser.add_mutually_exclusive_group()
        group.add_argument("--menu", help="Opens menu")
        group.add_argument("--list", action="store_true", help="Shows content of hosts file")
        group.add_argument("--check", metavar='HOSTNAME', nargs='+',
                           help="Check if host exists")
        group.add_argument("--insert", metavar='HOSTNAME[:IP]', nargs='+',
                           help="Append hostname")
        group.add_argument("--remove", metavar='HOSTNAME', nargs='+',
                           help="Remove hostname")
        group.add_argument("--sniff", metavar='trcroute option' ,help="starts scan")

        return parser
