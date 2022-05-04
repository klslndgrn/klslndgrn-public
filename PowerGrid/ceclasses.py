import psclasses as psc


class BusBar(psc.ConductingEquipment):
    '''
    BusBar class.
    '''
    def __init__(self, ID, Name, CE_Type, EquipmentContainerID,
                 Type='NotSpecified', BaseVolt=0, InService=True,
                 Processed=False):
        super().__init__(ID, Name, CE_Type, Type, Processed)

        self.CID = EquipmentContainerID
        self.BaseVolt = BaseVolt
        self.InService = InService


class Transformer(psc.ConductingEquipment):
    '''
    Transformer class.
    '''
    def __init__(self, ID, Name, CE_Type, EquipmentContainerID,
                 TermID1, TermID2, V_hv, V_lv, S_n,
                 Type='NotSpecified', Processed=False):
        super().__init__(ID, Name, CE_Type, Type, Processed)

        self.CID = EquipmentContainerID
        self.TermID1 = TermID1
        self.TermID2 = TermID2
        self.V_hv = V_hv
        self.V_lv = V_lv
        self.S_n = S_n


class Transformer3Way(psc.ConductingEquipment):
    '''
    3-Way Transformer class.
    '''
    def __init__(self, ID, Name, CE_Type, EquipmentContainerID,
                 TermID1, TermID2, TermID3, V_hv, V_mv, V_lv, S_n,
                 Type='NotSpecified', Processed=False):
        super().__init__(ID, Name, CE_Type, Type, Processed)

        self.CID = EquipmentContainerID
        self.T_ID1 = TermID1
        self.T_ID2 = TermID2
        self.T_ID3 = TermID3
        self.V_hv = V_hv
        self.V_mv = V_mv
        self.V_lv = V_lv
        self.S_n = S_n


class Breaker(psc.ConductingEquipment):
    '''
    Breaker/Switch class.
    '''
    def __init__(self, ID, Name, CE_Type, EquipmentContainerID,
                 ToID, FromID, OpenState=False,
                 Type='NotSpecified', Processed=False):
        super().__init__(ID, Name, CE_Type, Type, Processed)

        self.CID = EquipmentContainerID
        self.FromID = FromID
        self.ToID = ToID
        self.OpenState = OpenState


class Shunt(psc.ConductingEquipment):
    '''
    Shunt capacitor class.
    '''
    def __init__(self, ID, Name, CE_Type, EquipmentContainerID, TerminalID,
                 P_Shunt=0, Q_Shunt=0,
                 Type='NotSpecified', Processed=False):
        super().__init__(ID, Name, CE_Type, Type, Processed)

        self.TermID = TerminalID
        self.CID = EquipmentContainerID
        self.P_Shunt = P_Shunt
        self.Q_Shunt = Q_Shunt


class Load(psc.ConductingEquipment):
    '''
    Load class.
    '''
    def __init__(self, ID, Name, CE_Type, EquipmentContainerID, TerminalID,
                 P_Load=0, Q_Load=0,
                 Type='NotSpecified', Processed=False):
        super().__init__(ID, Name, CE_Type, Type, Processed)

        self.TermID = TerminalID
        self.CID = EquipmentContainerID
        self.P_Load = P_Load
        self.Q_Load = Q_Load


class Line(psc.ConductingEquipment):
    '''
    Line class.
    '''
    def __init__(self, ID, Name, CE_Type, EquipmentContainerID,
                 FromID, ToID, Length,
                 Type='NotSpecified', Processed=False):
        super().__init__(ID, Name, CE_Type, Type, Processed)

        self.CID = EquipmentContainerID
        self.FromID = FromID
        self.ToID = ToID
        self.Length = Length


class Generator(psc.ConductingEquipment):
    '''
    Generator/Motor class.
    '''
    def __init__(self, ID, Name, CE_Type, EquipmentContainerID, TerminalID,
                 GeneratorID, V_nom=0, S_nom=0, PF=1, P_Gen=0, Q_Gen=0,
                 Type='NotSpecified', Processed=False):
        super().__init__(ID, Name, CE_Type, Type, Processed)

        self.TermID = TerminalID
        self.CID = EquipmentContainerID
        self.GenID = GeneratorID
        self.Vn = V_nom
        self.Sn = S_nom
        self.PF = PF
        self.P_Gen = P_Gen
        self.Q_Gen = Q_Gen
