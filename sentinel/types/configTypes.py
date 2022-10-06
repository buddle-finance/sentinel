class BuddleConfig:
    def __init__(self, config: dict):
        self.defaults = Defaults(config.get("networkDefaults"))
        self.networks: list[Network] = [
            Network(network, self.defaults) for network in config.get("networks")
        ]


class Defaults:
    def __init__(self, defaults):
        if defaults is None:
            return

        self.privateKey: str = defaults.get("privateKey", "")
        self.processes: list[str] = defaults.get("processes", [])


class Network:
    def __init__(self, network: dict, defaults: Defaults):
        self.name: str = network.get("name")
        self.chainId: str = network.get("chainId")
        self.type: str = network.get("type")
        self.rpc: str = network.get("rpc")
        self.privateKey: str = network.get("privateKey", defaults.privateKey)
        self.srcContract: str = network.get("srcContract")
        self.destContract: str = network.get("destContract")
        self.bridgeContract: str = network.get("bridgeContract")
        self.processes: list[str] = network.get("processes", defaults.processes)
