class PSEquipment():
    '''
    A class containing 3 main types of equipment. Terminals, Connectivity Nodes
    and Conducting Equipment. Conducting Equipment in turn have subclasses
    containing data for each equipment.
    '''
    GridData = []

    def __init__(self, ID, Name, Type='NotSpecified', Processed=False):

        self.ID = ID
        self.Name = Name
        self.Type = Type
        self.Processed = Processed

    def __repr__(self):
        return(f'({self.Name}, {self.Type}, {self.Processed}) \n')


class Terminal(PSEquipment):
    '''
    A subclass to PSEquipment that creates Terminal variables.
    '''
    def __init__(self, ID, Name, ConductingEquipmentID, ConnectivityNodeID,
                 ConnectivityNodeName, Type,
                 ConnectionStatus=True, Processed=False):
        super().__init__(ID, Name, Type, Processed)

        self.CE = ConductingEquipmentID
        self.CN = ConnectivityNodeID
        self.CN_Name = ConnectivityNodeName
        self.ConStatus = ConnectionStatus


class ConnectivityNode(PSEquipment):
    '''
    A subclass to PSEquipment that creates ConnectivityNode variables.
    '''
    def __init__(self, ID, Name, ConnectivityNodeContainerID,
                 BaseVolt, Type, InService=True, Processed=False):
        super().__init__(ID, Name, Type, Processed)

        self.CID = ConnectivityNodeContainerID
        self.BaseVolt = BaseVolt
        self.InService = InService


class ConductingEquipment(PSEquipment):
    '''
    A subclass to PSEquipment that creates ConductingEquipment variables.
    There are multiple of subclasses to this subclass.
    '''
    def __init__(self, ID, Name, CE_Type, Type,
                 Processed=False):
        super().__init__(ID, Name, Type, Processed)

        self.CE_Type = CE_Type

    def __repr__(self):
        return(f'({self.Name}, {self.Type}, {self.CE_Type}, {self.Processed})\
               \n')
