class PSEquipment():
    '''
    A class containing 3 main types of equipment. Terminals,
    Connectivity Nodes and Conducting Equipment.
    Conducting Equipment is
    '''
    def __init__(self):
        pass


class Terminal(PSEquipment):
    '''
    A subclass to PSEquipment that creates Terminal variables.
    '''
    def __init__(self, ID, ConductingEquipmentID, ConnectivityNodeID,
                 Name=None, ConnectionStatus=True, Processed=False):
        super().__init__()
        self.ID = ID
        self.CE = ConductingEquipmentID
        self.CN = ConnectivityNodeID
        self.Name = Name
        self.ConStatus = ConnectionStatus
        self.Processed = Processed

    def __repr__(self):
        return(f'(ID = {self.ID}, CE = {self.CE}, CN ={self.CN}, \
               Processed = {self.Processed}) \n')


class ConnectivityNode(PSEquipment):
    '''
    A subclass to PSEquipment that creates ConnectivityNode variables.
    '''

    def __init__(self, ID, ConnectivityNodeContainerID, Name=None,
                 Processed=False):
        super().__init__()
        self.ID = ID
        self.CID = ConnectivityNodeContainerID
        self.Name = Name
        self.Processed = Processed

    def __repr__(self):
        return(f'(ID = {self.ID}, Container ID = {self.CID}, \
               Processed = {self.Processed})) \n')


class ConductingEquipment(PSEquipment):
    '''
    A subclass to PSEquipment that creates ConductingEquipment variables.
    There are multiple of subclasses to this subclass.
    '''
    def __init__(self):
        pass


class ConnectivityNodeGroup():
    # FIXME: Should this be included?
    pass
