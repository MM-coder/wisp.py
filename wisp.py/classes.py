class Server(object):

    '''
        Represents a user accesable Server object
    '''


    def __init__(self, server_owner: bool, identifier: str, name: str, description: str, limits: dict, databases: int):
        self.owner = server_owner
        self.identifier = identifier
        self.name = name
        self.description = description
        self.limits = limits

    def __repr__(self):
        '''
            Have a nice representation name for the class
        '''
        return self.name

    @property
    def id(self):
        '''
            Returns the server's ID 
        '''
        return self.identifier

    @property
    def ram(self):
        '''
            Returns the server's RAM 
        '''
        return self.limits['memory']

    @property
    def memory(self):
        '''
            Same as RAM
        '''
        return self.limits['memory']

    @property
    def swap(self):
        '''
            Returns the server's allocated SWAP
        '''
        return self.limits['swap']

    
    @property
    def cpu(self):
        '''
            Returns the server's CPU limit
        '''
        return self.limits['cpu']

class Query(object):

    '''
        Represents a server's QueryData
    '''

    def __init__(self, type: str, name: str, map: str, password: str, maxplayers: int):
        self.type = type
        self.name = name
        self.map = map
        self.password = password
        self.maxplayers = maxplayers

class Stats(object):

    '''
        Represents a server's statistics
    '''

    def __init__(self, state: str, memory: dict, cpu: dict, disk: dict, players: dict, **kwargs):
        self.state = state
        self.memory = memory
        self.cpu = cpu
        self.disk = disk
        self.players = players
        self.query = kwargs.get('query')

    @property
    def memory_usage(self):
        '''
            Returns current memory usage in MB
        '''
        return self.memory['current']

    @property
    def memory_limit(self):
        '''
            Returns memory limit in MB
        '''
        return self.memory['limit']

    @property
    def cpu_usage(self):
        '''
            Returns cpu usage in percent
        '''
        return self.cpu['current']

    @property
    def cpu_limit(self):
        '''
            Returns the cpu limit
            The value == 0 if it's unlimited
        '''
        return self.cpu['limit']

    @property
    def cpu_cores(self):
        '''
            Returns the cpu cores
            Can be [] if the machine is offline
        '''
        return self.cpu['cores']

    @property
    def disk_usage(self):
        '''
            Returns current disk usage in MB
        '''
        return self.disk['current']

    @property
    def disk_limit(self):
        '''
            Returns disk limit in MB
        '''
        return self.disk['limit']

    @property
    def current_players(self):
        '''
            Returns current player count
        '''
        return self.players['current']

    @property
    def players_limit(self):
        '''
            Returns players limit
        '''
        return self.players['limit']