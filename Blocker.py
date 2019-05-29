from utils import Platform


class Host:
    def __init__(self):
        platform = Platform()
        self.platform = platform

        if platform.is_linux() or platform.is_mac():
            self.hostsFile = "/etc/hosts"
        elif platform.is_windows():
            self.hostsFile = r'c:\windows\system32\drivers\etc\hosts'
        else:
            self.hostsFile = '/etc/hosts'

    def list_hosts_file(self):
        with open(self.hostsFile, 'r') as f:
            return [line.strip() for line in f]

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

    def _split_row(self, host_names):
        return self.platform.is_windows() and len(host_names) >= 9

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

    def _get_file_lines(self):
        with open(self.hostsFile, 'r') as input:
            lines = input.readlines()
            return lines
