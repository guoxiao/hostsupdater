#!/usr/bin/python
import dns.resolver
from multiprocessing.dummy import Pool as ThreadPool

class HostsUpdater():
    """
    HostsUpdater: Read a hosts file and query to make a new one
    """
    names = []
    name_ip = []
    nameservers = ['8.8.8.8']
    THREADS = 10
    def __init__(self, infilename, outfilename):
        self.infilename = infilename
        self.outfilename = outfilename
        self.my_resolver = dns.resolver.Resolver()
        self.my_resolver.nameservers = self.nameservers

    def read(self):
        with open(self.infilename, 'r') as infile:
            for line in infile:
                line = line.strip()
                if line == "" or line[0] == '#':
                    pass
                else:
                    self.names.append(line.split("\t")[1])

    def query(self):
        pool = ThreadPool(self.THREADS)
        self.name_ip = pool.map(self.queryone, self.names)
        pool.close()
        pool.join()
        print(self.name_ip)

    def queryone(self, name):
        try:
            print(name)
            answer = self.my_resolver.query(name, 'A', tcp=True)
            ipaddr = answer[0].address
            print(ipaddr)
            return (ipaddr, name)
        except dns.exception.DNSException:
            return None

    def output(self):
        with open(self.outfilename, 'w') as outfile:
            for item in self.name_ip:
                if item is None:
                    pass
                else:
                    line = "%s\t%s\n" % item
                    print(line)
                    outfile.write(line)
    def run(self):
        self.read()
        self.query()
        self.output()


if __name__ == '__main__':
    hostupdater = HostsUpdater('hosts','hosts.out')
    hostupdater.run()
