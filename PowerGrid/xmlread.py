'''
This file contains functions to extract data from XML files
'''
# XML library
import xml.etree.ElementTree as ET

# To find path for files
from pathlib import Path

# Power System Classes (Terminals, ConnectivityNodes and ConductingEquipments)
import psclasses as psc
import ceclasses as cec

ns = {'cim': 'http://iec.ch/TC57/2013/CIM-schema-cim16#',
      'entsoe': 'http://entsoe.eu/CIM/SchemaExtension/3/1#',
      'rdf': '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'}


def read_file(file):
    '''
    Creating an XML tree from file and accessing the root.
    '''
    # Finding directory
    filestr = 'Files/' + file
    script_location = Path(__file__).absolute().parent
    Xfile = script_location / filestr
    # Creating an XML tree from file.
    tree = ET.parse(Xfile)

    # Accesssing root in XML tree.
    root = tree.getroot()

    # Returning the root
    return(root)


def unique_equipment(root):
    unieq = []
    for equipment in root:
        if (ns['cim'] in equipment.tag):
            eq = equipment.tag.replace("{" + ns['cim'] + "}", "")
            if eq not in unieq:
                unieq.append(eq)
    return(unieq)


def find_connected_equipment(root, eqlist):
    equipment = []
    for id in eqlist:
        for child in root:
            tg = child.tag.replace("{" + ns['cim'] + "}", "")
            attrID = child.attrib.get(ns['rdf'] + 'ID')

            if id == attrID and tg not in equipment:
                equipment.append(tg)
    return(equipment)


def find_connected_equipment_CN(root, eqlist):
    equipment = []
    for id in eqlist:
        for child in root:
            tg = child.tag.replace("{" + ns['cim'] + "}", "")
            attrID = child.attrib.get(ns['rdf'] + 'ID')

            if id == attrID and tg not in equipment:
                equipment.append(tg)
    return(equipment)


# --------------------------------------------------------------------------- #
# ------------------------ TE: TERMINALS ------------------------------------ #
# --------------------------------------------------------------------------- #
def terminal_data(root):
    '''
    Searches for "cim:Terminal" which is the main block,
    and "cim:PowerTransformerEnd"
    '''
    terminals = []
    for terminal in root.findall('cim:Terminal', ns):
        id = terminal.attrib.get(ns['rdf'] + 'ID')

        name = terminal.find('{' + ns['cim'] + '}' +
                             'IdentifiedObject.name').text

        ce = terminal.find('cim:Terminal.ConductingEquipment', ns)
        ce_id = ce.attrib.get(ns['rdf'] + 'resource')
        ce_id = ce_id[1:]

        cn = terminal.find('cim:Terminal.ConnectivityNode', ns)
        cn_id = cn.attrib.get(ns['rdf'] + 'resource')
        cn_id = cn_id[1:]

        types = 'Te'

        for connode in root.findall('cim:ConnectivityNode', ns):
            cnid = connode.attrib.get(ns['rdf'] + 'ID')
            cnname = connode.find('{' + ns['cim'] + '}' +
                                  'IdentifiedObject.name').text
            if cnid == cn_id:
                cn_name = cnname
                break
            else:
                pass

        term = psc.Terminal(id, name, ce_id, cn_id, cn_name, Type=types)
        terminals.append(term)
    return(terminals)


# --------------------------------------------------------------------------- #
# ------------------------ CN: CONNECTIVITY NODES --------------------------- #
# --------------------------------------------------------------------------- #
def connectivity_node_data(root):
    connectivitynodes = []
    for cn in root.findall('cim:ConnectivityNode', ns):

        id = cn.attrib.get(ns['rdf'] + 'ID')

        name = cn.find('{' + ns['cim'] + '}' + 'IdentifiedObject.name').text

        cnc = cn.find('cim:ConnectivityNode.ConnectivityNodeContainer', ns)
        cid = cnc.attrib.get(ns['rdf'] + 'resource')
        cid = cid[1:]

        types = 'CN'

        for voltlevel in root.findall('cim:VoltageLevel', ns):
            vlid = voltlevel.attrib.get(ns['rdf'] + 'ID')
            if vlid == cid:
                v_n = voltlevel.find('{' + ns['cim'] + '}' +
                                     'cim:IdentifiedObject.name')

        conode = psc.ConnectivityNode(id, name, cid, v_n, Type=types)
        connectivitynodes.append(conode)
    return(connectivitynodes)


# --------------------------------------------------------------------------- #
# ------------------------ CE: CONDUCTION EQUIPMENT ------------------------- #
# --------------------------------------------------------------------------- #
def busbar_data(root):
    busbars = []
    for bbs in root.findall('cim:BusbarSection', ns):

        id = bbs.attrib.get(ns['rdf'] + 'ID')

        name = bbs.find('{' + ns['cim'] + '}' + 'IdentifiedObject.name').text

        ec = bbs.find('cim:Equipment.EquipmentContainer', ns)
        ecid = ec.attrib.get(ns['rdf'] + 'resource')
        ecid = ecid[1:]

        types = 'CE'
        CE_type = 'BusBar'

        busbarcon = cec.BusBar(id, name, CE_type, ecid, Type=types)
        busbars.append(busbarcon)
    return(busbars)


def breaker_data(root):
    breakers = []
    for breaker in root.findall('cim:Breaker', ns):

        id = breaker.attrib.get(ns['rdf'] + 'ID')

        name = breaker.find('{' + ns['cim'] + '}' +
                            'IdentifiedObject.name').text

        openstate = breaker.find('{' + ns['cim'] + '}' +
                                 'Switch.normalOpen').text.capitalize()

        ec = breaker.find('cim:Equipment.EquipmentContainer', ns)
        ecid = ec.attrib.get(ns['rdf'] + 'resource')
        ecid = ecid[1:]

        types = 'CE'
        CE_type = 'Breaker'

        break_id = []
        for terminal in root.findall('cim:Terminal', ns):
            terminalID = terminal.attrib.get(ns['rdf'] + 'ID')

            br = terminal.find('cim:Terminal.ConductingEquipment', ns)
            brid = br.attrib.get(ns['rdf'] + 'resource')
            breakerid = brid[1:]

            if id == breakerid:
                break_id.append(terminalID)
            else:
                pass

        FromID = break_id[0]
        ToID = break_id[1]

        brkr = cec.Breaker(id, name, CE_type, ecid, FromID, ToID, openstate,
                           Type=types)
        breakers.append(brkr)
    return(breakers)


def shunt_data(root):
    shunts = []
    for shunt in root.findall('cim:LinearShuntCompensator', ns):

        id = shunt.attrib.get(ns['rdf'] + 'ID')

        name = shunt.find('{' + ns['cim'] + '}' + 'IdentifiedObject.name').text

        ec = shunt.find('cim:Equipment.EquipmentContainer', ns)
        ecid = ec.attrib.get(ns['rdf'] + 'resource')
        ecid = ecid[1:]

        types = 'CE'
        CE_type = 'Shunt'

        for terminal in root.findall('cim:Terminal', ns):
            terminalID = terminal.attrib.get(ns['rdf'] + 'ID')

            t = terminal.find('cim:Terminal.ConductingEquipment', ns)
            tid = t.attrib.get(ns['rdf'] + 'resource')
            TID = tid[1:]

            if id == TID:
                TermID = terminalID
                break
            else:
                pass

        shnts = cec.Shunt(id, name, CE_type, ecid, TermID, Type=types)
        shunts.append(shnts)
    return(shunts)


def transformer_data(root):
    transformers = []
    for transformer in root.findall('cim:PowerTransformer', ns):
        id = transformer.attrib.get(ns['rdf'] + 'ID')

        name = transformer.find('{' + ns['cim'] + '}' +
                                'IdentifiedObject.name').text

        ec = transformer.find('cim:Equipment.EquipmentContainer', ns)
        ecid = ec.attrib.get(ns['rdf'] + 'resource')
        ecid = ecid[1:]

        types = 'CE'
        CE_type = 'Transformer'

        trafodict = {}
        # Extracting data from "cim:PowerTransformerEnd"
        for trafoend in root.findall('cim:PowerTransformerEnd', ns):
            # tendid = trafoend.attrib.get(ns['rdf'] + 'ID')

            t = trafoend.find('cim:TransformerEnd.Terminal', ns)
            tid = t.attrib.get(ns['rdf'] + 'resource')
            termid = tid[1:]

            e = trafoend.find('cim:PowerTransformerEnd.PowerTransformer', ns)
            eid = e.attrib.get(ns['rdf'] + 'resource')
            eid = eid[1:]

            v_n = trafoend.find('{' + ns['cim'] + '}' +
                                'PowerTransformerEnd.ratedU').text

            S_n = trafoend.find('{' + ns['cim'] + '}' +
                                'PowerTransformerEnd.ratedS').text

            if id == eid:
                trafodict[termid] = v_n
            else:
                pass

        # Sort dictionary
        sorted_values = sorted(trafodict.values(), reverse=True)
        # Sort the values
        trafodict_sort = {}

        for i in sorted_values:
            for k in trafodict.keys():
                if trafodict[k] == i:
                    trafodict_sort[k] = trafodict[k]
                    break

        idz = list(trafodict_sort.keys())
        vlvl = list(trafodict_sort.values())

        # Create class
        if len(idz) == 2:
            TermID1 = idz[0]
            TermID2 = idz[1]
            V_hv = vlvl[0]
            V_lv = vlvl[1]
            trans = cec.Transformer(id, name, CE_type, ecid,
                                    TermID1, TermID2,
                                    V_hv, V_lv, S_n,
                                    Type=types)
            transformers.append(trans)
        if len(idz) == 3:
            TermID1 = idz[0]
            TermID2 = idz[1]
            TermID3 = idz[2]
            V_hv = vlvl[0]
            V_mv = vlvl[1]
            V_lv = vlvl[2]
            trans = cec.Transformer3Way(id, name, CE_type, ecid,
                                        TermID1, TermID2, TermID3,
                                        V_hv, V_mv, V_lv, S_n,
                                        Type=types)
            transformers.append(trans)
    return(transformers)


def load_data(root):
    consumers = []
    for consumer in root.findall('cim:EnergyConsumer', ns):

        id = consumer.attrib.get(ns['rdf'] + 'ID')

        name = consumer.find('{' + ns['cim'] + '}' +
                             'IdentifiedObject.name').text

        ec = consumer.find('cim:Equipment.EquipmentContainer', ns)
        ecid = ec.attrib.get(ns['rdf'] + 'resource')
        ecid = ecid[1:]

        types = 'CE'
        CE_type = 'Load'

        for terminal in root.findall('cim:Terminal', ns):
            terminalID = terminal.attrib.get(ns['rdf'] + 'ID')

            t = terminal.find('cim:Terminal.ConductingEquipment', ns)
            tid = t.attrib.get(ns['rdf'] + 'resource')
            TID = tid[1:]

            if id == TID:
                TermID = terminalID
                break
            else:
                pass

        lds = cec.Load(id, name, CE_type, ecid, TermID, Type=types)
        consumers.append(lds)
    return(consumers)


def line_data(root):
    'Length = "cim:Conductor.length>45.000000"'
    lines = []
    for line in root.findall('cim:ACLineSegment', ns):

        id = line.attrib.get(ns['rdf'] + 'ID')

        name = line.find('{' + ns['cim'] + '}' + 'IdentifiedObject.name').text

        ec = line.find('cim:Equipment.EquipmentContainer', ns)
        ecid = ec.attrib.get(ns['rdf'] + 'resource')
        ecid = ecid[1:]

        types = 'CE'
        CE_type = 'Line'

        length = line.find('{' + ns['cim'] + '}' + 'Conductor.length').text
        ToFrom = []
        for terminal in root.findall('cim:Terminal', ns):
            termid = terminal.attrib.get(ns['rdf'] + 'ID')

            ce = terminal.find('cim:Terminal.ConductingEquipment', ns)
            ce_id = ce.attrib.get(ns['rdf'] + 'resource')
            ce_id = ce_id[1:]

            if id == ce_id:
                ToFrom.append(termid)

        FromID = ToFrom[0]
        ToID = ToFrom[1]
        lns = cec.Line(id, name, CE_type, ecid,
                       FromID, ToID, Length=length,
                       Type=types)
        lines.append(lns)
    return(lines)


def generator_data(root):
    generators = []
    for generator in root.findall('cim:SynchronousMachine', ns):

        id = generator.attrib.get(ns['rdf'] + 'ID')

        name = generator.find('{' + ns['cim'] + '}' +
                              'IdentifiedObject.name').text

        types = 'CE'
        CE_type = 'Generator'

        ec = generator.find('cim:Equipment.EquipmentContainer', ns)
        ecid = ec.attrib.get(ns['rdf'] + 'resource')
        ecid = ecid[1:]

        gen = generator.find('cim:RotatingMachine.GeneratingUnit', ns)
        genid = gen.attrib.get(ns['rdf'] + 'resource')
        genid = genid[1:]

        v_n = generator.find('{' + ns['cim'] + '}' +
                             'RotatingMachine.ratedU').text

        s_n = generator.find('{' + ns['cim'] + '}' +
                             'RotatingMachine.ratedS').text

        cosphi = generator.find('{' + ns['cim'] + '}' +
                                'RotatingMachine.ratedPowerFactor').text

        for terminal in root.findall('cim:Terminal', ns):
            terminalID = terminal.attrib.get(ns['rdf'] + 'ID')

            t = terminal.find('cim:Terminal.ConductingEquipment', ns)
            tid = t.attrib.get(ns['rdf'] + 'resource')
            TID = tid[1:]

            if id == TID:
                TermID = terminalID
                break
            else:
                pass

        lds = cec.Generator(id, name, CE_type, ecid, TermID, genid,
                            V_nom=v_n, S_nom=s_n, PF=cosphi,
                            Type=types)
        generators.append(lds)
    return(generators)


def conducting_equipment_data(root):
    CE = []
    CE_new = []
    CE.append(busbar_data(root))
    CE.append(breaker_data(root))
    CE.append(shunt_data(root))
    CE.append(transformer_data(root))
    CE.append(line_data(root))
    CE.append(load_data(root))
    CE.append(generator_data(root))

    for i in CE:
        for j in i:
            CE_new.append(j)
    return(CE_new)


# --------------------------------------------------------------------------- #
# ------------------------ ALL EQUIPMENT ------------------------------------ #
# --------------------------------------------------------------------------- #
def all_data(root):
    all = []
    all_new = []
    all.append(terminal_data(root))
    all.append(connectivity_node_data(root))
    all.append(conducting_equipment_data(root))

    for i in all:
        for j in i:
            all_new.append(j)
    return(all_new)
