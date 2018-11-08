from configparser import SafeConfigParser


class Configuration(SafeConfigParser):
    """Clase encargada de administrar las configuraciones"""

    def __init__(self, master=None):
        SafeConfigParser.__init__(self, master)
        self.read('config.ini')

    # Cambia un valor de configuracion
    def add_config(self, section, key, value):
        if not self.has_section(section):
            print('La seccion no existe')
            self.add_section(section)

        self.set(section, key, value)

    # Retorna un valor de configuracion
    def get_config(self, section, key):
        if not self.has_section(section):
            return False

        return self.get(section, key)

    # Obtiene listado de hosts
    def get_hosts_list(self):
        hosts = []
        for key, value in self.items('hosts'):
            hosts.append(value)

        return hosts