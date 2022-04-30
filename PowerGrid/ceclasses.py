import psclasses as psc


class BusBar(psc.ConductingEquipment):
    # TODO: Is more data needed?
    '''
    BusBar class.
    '''
    def __init__(self, ID, EquipmentContainerID, Name=None, BaseVolt=0,
                 Processed=False):
        super().__init__()
        self.ID = ID
        self.CID = EquipmentContainerID
        self.Name = Name
        self.BaseVolt = BaseVolt
        self.Processed = Processed

    def __repr__(self):
        return(f'(ID = {self.ID}, Processed = {self.Processed})) \n')


class Transformer(psc.ConductingEquipment):
    # TODO: Is more data needed?
    '''
    Transformer class.
    '''
    def __init__(self, ID, EquipmentContainerID, TermID1, TermID2, V_hv, V_lv,
                 S_n, Name=None, Processed=False):
        super().__init__()
        self.ID = ID
        # self.EndID = EndID
        self.CID = EquipmentContainerID
        self.T_ID1 = TermID1
        self.T_ID2 = TermID2
        self.V_hv = V_hv
        self.V_lv = V_lv
        self.S_n = S_n
        self.Name = Name
        self.Processed = Processed

    def __repr__(self):
        return(f'(2-WAY-TRAFO:ID = {self.ID}, Voltage Levels = {self.V_hv}/ \
               {self.V_lv} kV, S_n = {self.S_n}, \
               Processed = {self.Processed})) \n')


class Transformer3Way(psc.ConductingEquipment):
    # TODO: Is more data needed?
    def __init__(self, ID, EquipmentContainerID, TermID1, TermID2, TermID3,
                 V_hv, V_mv, V_lv, S_n, Name=None, Processed=False):
        super().__init__()
        self.ID = ID
        # self.EndID = EndID
        self.CID = EquipmentContainerID
        self.T_ID1 = TermID1
        self.T_ID2 = TermID2
        self.T_ID3 = TermID3
        self.V_hv = V_hv
        self.V_mv = V_mv
        self.V_lv = V_lv
        self.S_n = S_n
        self.Name = Name
        self.Processed = Processed

    def __repr__(self):
        return(f'(3-WAY-TRAFO: ID = {self.ID}, Voltage Levels = {self.V_hv}/ \
              {self.V_mv}/{self.V_lv} kV, S_n = {self.S_n}, \
              Processed = {self.Processed})) \n')


class Breaker(psc.ConductingEquipment):
    # TODO: Is more data needed?
    def __init__(self, ID, EquipmentContainerID, OpenState=False,
                 Name=None, Processed=False):
        super().__init__()
        self.ID = ID
        self.CID = EquipmentContainerID
        self.OpenState = OpenState
        self.Name = Name
        self.Processed = Processed

    def __repr__(self):
        return(f'(ID = {self.ID}, OpenState = {self.OpenState}, \
                Processed = {self.Processed})) \n')


class Shunt(psc.ConductingEquipment):
    # TODO: Is more data needed?
    def __init__(self, ID, EquipmentContainerID, Name=None, Processed=False):
        super().__init__()
        self.ID = ID
        self.CID = EquipmentContainerID
        self.Name = Name
        self.Processed = Processed

    def __repr__(self):
        return(f'(ID = {self.ID}, Processed = {self.Processed})) \n')


class Load(psc.ConductingEquipment):
    def __init__(self, ID, EquipmentContainerID, P_Load=0, Q_Load=0,
                 Name=None, Processed=False):
        super().__init__()
        self.ID = ID
        self.CID = EquipmentContainerID
        self.P_Load = P_Load
        self.Q_Load = Q_Load
        self.Name = Name
        self.Processed = Processed

    def __repr__(self):
        return(f'(ID = {self.ID}, P = {self.P_Load} kV, Q = {self.Q_Load} \
                kVAr, Processed = {self.Processed})) \n')


class Line(psc.ConductingEquipment):
    # FIXME:    ACLineSegment
    #           FROM, TO, LENGTH
    def __init__(self, ID, EquipmentContainerID, FromID, ToID, Length=None,
                 Name=None, Processed=False):
        super().__init__()
        self.ID = ID
        self.CID = EquipmentContainerID
        self.FromID = FromID
        self.ToID = ToID
        self.Length = Length
        self.Name = Name
        self.Processed = Processed

    def __repr__(self):
        return(f'(ID = {self.ID}, Length = {self.Length}, \
               Processed = {self.Processed})) \n')


class Generator(psc.ConductingEquipment):
    # FIXME: SyncronousMachine <-> GeneratingUnit
    def __init__(self, ID, EquipmentContainerID, GeneratorID, P_Gen=0, Q_Gen=0,
                 PF=1, Name=None, Processed=False):
        super().__init__()
        self.ID = ID
        self.CID = EquipmentContainerID
        self.GenID = GeneratorID
        self.P_Gen = P_Gen
        self.Q_Gen = Q_Gen
        self.PF = PF
        self.Name = Name
        self.Processed = Processed

    def __repr__(self):
        return(f'(ID = {self.ID}, P = {self.P_Gen} kV, Q = {self.Q_Gen} kVAr, \
               Processed = {self.Processed})) \n')

# -------------------------------------------------------------------- #
# ------------------------ UNFINISHED CLASSES ------------------------ #
# -------------------------------------------------------------------- #
