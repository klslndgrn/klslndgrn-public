import psclasses as psc


class BusBar(psc.ConductingEquipment):
    '''
    BusBar class.
    '''
    def __init__(self, ID, Name, CE_Type, EquipmentContainerID,
                 Type='NotSpecified', BaseVolt=0, Processed=False):
        super().__init__()

        self.ID = ID
        self.Name = Name
        self.Type = Type
        self.CE_Type = CE_Type
        self.CID = EquipmentContainerID
        self.Processed = Processed

        self.BaseVolt = BaseVolt

    def __repr__(self):
        return(f'(ID = {self.ID}, Processed = {self.Processed})) \n')


class Transformer(psc.ConductingEquipment):
    '''
    Transformer class.
    '''
    def __init__(self, ID, Name, CE_Type, EquipmentContainerID,
                 TermID1, TermID2, V_hv, V_lv, S_n,
                 Type='NotSpecified', Processed=False):
        super().__init__()

        self.ID = ID
        self.Name = Name
        self.Type = Type
        self.CE_Type = CE_Type
        self.CID = EquipmentContainerID
        self.Processed = Processed

        self.T_ID1 = TermID1
        self.T_ID2 = TermID2
        self.V_hv = V_hv
        self.V_lv = V_lv
        self.S_n = S_n

    def __repr__(self):
        return(f'(2-WAY-TRAFO:ID = {self.ID}, Voltage Levels = {self.V_hv}/ \
               {self.V_lv} kV, S_n = {self.S_n}, \
               Processed = {self.Processed})) \n')


class Transformer3Way(psc.ConductingEquipment):
    '''
    3-Way Transformer class.
    '''
    def __init__(self, ID, Name, CE_Type, EquipmentContainerID,
                 TermID1, TermID2, TermID3, V_hv, V_mv, V_lv, S_n,
                 Type='NotSpecified', Processed=False):
        super().__init__()

        self.ID = ID
        self.Name = Name
        self.Type = Type
        self.CE_Type = CE_Type
        self.CID = EquipmentContainerID
        self.Processed = Processed

        self.T_ID1 = TermID1
        self.T_ID2 = TermID2
        self.T_ID3 = TermID3
        self.V_hv = V_hv
        self.V_mv = V_mv
        self.V_lv = V_lv
        self.S_n = S_n

    def __repr__(self):
        return(f'(3-WAY-TRAFO: ID = {self.ID}, Voltage Levels = {self.V_hv}/ \
              {self.V_mv}/{self.V_lv} kV, S_n = {self.S_n}, \
              Processed = {self.Processed})) \n')


class Breaker(psc.ConductingEquipment):
    '''
    Breaker/Switch class.
    '''
    def __init__(self, ID, Name, CE_Type, EquipmentContainerID,
                 OpenState=False, Type='NotSpecified', Processed=False):
        super().__init__()

        self.ID = ID
        self.Name = Name
        self.Type = Type
        self.CE_Type = CE_Type
        self.CID = EquipmentContainerID
        self.Processed = Processed

        self.OpenState = OpenState

    def __repr__(self):
        return(f'(ID = {self.ID}, OpenState = {self.OpenState}, \
                Processed = {self.Processed})) \n')


class Shunt(psc.ConductingEquipment):
    '''
    Shunt capacitor class.
    '''
    def __init__(self, ID, Name, CE_Type, EquipmentContainerID,
                 P_shunt=0, Q_shunt=0,
                 Type='NotSpecified', Processed=False):
        super().__init__()

        self.ID = ID
        self.Name = Name
        self.Type = Type
        self.CE_Type = CE_Type
        self.CID = EquipmentContainerID
        self.Processed = Processed

        self.P_shunt = P_shunt
        self.Q_shunt = Q_shunt

    def __repr__(self):
        return(f'(ID = {self.ID}, Processed = {self.Processed})) \n')


class Load(psc.ConductingEquipment):
    '''
    Load class.
    '''
    def __init__(self, ID, Name, CE_Type, EquipmentContainerID,
                 P_Load=0, Q_Load=0,
                 Type='NotSpecified', Processed=False):
        super().__init__()

        self.ID = ID
        self.Name = Name
        self.Type = Type
        self.CE_Type = CE_Type
        self.CID = EquipmentContainerID
        self.Processed = Processed

        self.P_Load = P_Load
        self.Q_Load = Q_Load

    def __repr__(self):
        return(f'(ID = {self.ID}, P = {self.P_Load} kV, Q = {self.Q_Load} \
                kVAr, Processed = {self.Processed})) \n')


class Line(psc.ConductingEquipment):
    def __init__(self, ID, Name, CE_Type, EquipmentContainerID,
                 FromID, ToID, Length,
                 Type='NotSpecified', Processed=False):
        super().__init__()

        self.ID = ID
        self.Name = Name
        self.Type = Type
        self.CE_Type = CE_Type
        self.CID = EquipmentContainerID
        self.Processed = Processed

        self.FromID = FromID
        self.ToID = ToID
        self.Length = Length

    def __repr__(self):
        return(f'(ID = {self.ID}, Length = {self.Length}, \
               Processed = {self.Processed})) \n')


class Generator(psc.ConductingEquipment):
    def __init__(self, ID, Name, CE_Type, EquipmentContainerID,
                 GeneratorID, P_Gen=0, Q_Gen=0, PF=1,
                 Type='NotSpecified', Processed=False):
        super().__init__()

        self.ID = ID
        self.Name = Name
        self.Type = Type
        self.CE_Type = CE_Type
        self.CID = EquipmentContainerID
        self.Processed = Processed

        self.GenID = GeneratorID
        self.P_Gen = P_Gen
        self.Q_Gen = Q_Gen
        self.PF = PF

    def __repr__(self):
        return(f'(ID = {self.ID}, P = {self.P_Gen} kV, Q = {self.Q_Gen} kVAr, \
               Processed = {self.Processed})) \n')

# -------------------------------------------------------------------- #
# ------------------------ UNFINISHED CLASSES ------------------------ #
# -------------------------------------------------------------------- #
