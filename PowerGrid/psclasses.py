class PSEquipment():
    '''
    A class containing 3 main types of equipment. Terminals,
    Connectivity Nodes and Conducting Equipment.
    Conducting Equipment is
    '''
    def __init__(self, ID, Name, Type='NotSpecified', Processed=False):

        self.ID = ID
        self.Name = Name
        self.Type = Type
        self.Processed = Processed

    def __repr__(self):
        return(f'({self.Name}, Type = {self.Type}) \n')


class Terminal(PSEquipment):
    '''
    A subclass to PSEquipment that creates Terminal variables.
    '''
    def __init__(self, ID, Name, ConductingEquipmentID, ConnectivityNodeID,
                 Type='NotSpecified', ConnectionStatus=True, Processed=False):
        super().__init__()

        self.ID = ID
        self.Name = Name
        self.Type = Type
        self.Processed = Processed

        self.CE = ConductingEquipmentID
        self.CN = ConnectivityNodeID
        self.ConStatus = ConnectionStatus

    # def __repr__(self):
    #     return(f'({self.Name}, Type = {self.Type}) \n')
        # return(f'(ID = {self.ID}, CE = {self.CE}, CN ={self.CN}, \
        #        Processed = {self.Processed}) \n')


class ConnectivityNode(PSEquipment):
    '''
    A subclass to PSEquipment that creates ConnectivityNode variables.
    '''
    def __init__(self, ID, Name, ConnectivityNodeContainerID,
                 Type='NotSpecified', Processed=False):
        super().__init__()

        self.ID = ID
        self.Name = Name
        self.Type = Type
        self.Processed = Processed

        self.CID = ConnectivityNodeContainerID

    # def __repr__(self):
    #     return(f'({self.Name}, Type = {self.Type}) \n')
        # return(f'(ID = {self.ID}, Container ID = {self.CID}, \
        #        Processed = {self.Processed})) \n')


class ConductingEquipment(PSEquipment):
    '''
    A subclass to PSEquipment that creates ConductingEquipment variables.
    There are multiple of subclasses to this subclass.
    '''
    def __init__(self, ID, Name, CE_Type, Type='NotSpecified',
                 Processed=False):

        self.ID = ID
        self.Name = Name
        self.Type = Type
        self.Processed = Processed

        self.CE_Type = CE_Type

    # def __repr__(self):
    #     return(f'({self.Name}, Type = {self.Type}) \n')


class ConnectivityNodeGroup():
    # FIXME: Should this be included?
    pass
