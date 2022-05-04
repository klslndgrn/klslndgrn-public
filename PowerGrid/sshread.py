import eqread as eqr

# --------------------------------------------------------------------------- #
# ------------------------ Needed for XML extraction ------------------------ #
# --------------------------------------------------------------------------- #
ns = {'cim': 'http://iec.ch/TC57/2013/CIM-schema-cim16#',
      'entsoe': 'http://entsoe.eu/CIM/SchemaExtension/3/1#',
      'rdf': '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'}


# --------------------------------------------------------------------------- #
# ------------------------ Updating equipment file -------------------------- #
# --------------------------------------------------------------------------- #
def update_data_lists(eq_file, ssh_file):
    # Accessing root of XML file ------------------- #
    root_ssh = eqr.read_file(ssh_file)

    # Updating breakers ---------------------------- #
    eq_file = updating_breakers(eq_file, root_ssh)

    # Updating loads
    eq_file = updating_loads(eq_file, root_ssh)

    # Updating generators
    eq_file = updating_generators(eq_file, root_ssh)

    # Updating terminals
    eq_file = updating_terminals(eq_file, root_ssh)

    # Creating data from root ---------------------- #
    grid_data = eq_file
    return(grid_data)


# BREAKERS ----------------------------------------- #
def updating_breakers(eq_file, root):
    for eq in eq_file:
        if eq.Type == 'CE' and eq.CE_Type == 'Breaker':
            for breaker in root.findall('cim:Breaker', ns):
                idf = breaker.attrib.get(ns['rdf'] + 'about')
                id = idf[1:]

                openstate = breaker.find('{' + ns['cim'] + '}' +
                                         'Switch.open').text.capitalize()

                if eq.ID == id:
                    eq.OpenState = openstate
                    # print(f'Breaker status updated: {openstate}')
                    break
                else:
                    pass
        else:
            pass
    return(eq_file)


def updating_loads(eq_file, root):
    for eq in eq_file:
        if eq.Type == 'CE' and eq.CE_Type == 'Load':
            for load in root.findall('cim:EnergyConsumer', ns):
                idf = load.attrib.get(ns['rdf'] + 'about')
                id = idf[1:]

                pl = load.find('{' + ns['cim'] + '}' +
                               'EnergyConsumer.p').text
                pload = int(float(pl))

                ql = load.find('{' + ns['cim'] + '}' +
                               'EnergyConsumer.q').text
                qload = int(float(ql))

                if eq.ID == id:
                    eq.P_Load = pload
                    eq.Q_Load = qload
                    # print(f'Load updates: P = {pload}, Q = {qload}')
                    break
                else:
                    pass
        else:
            pass
    return(eq_file)


def updating_generators(eq_file, root):
    for eq in eq_file:
        if eq.Type == 'CE' and eq.CE_Type == 'Generator':
            for gen in root.findall('cim:SynchronousMachine', ns):
                idf = gen.attrib.get(ns['rdf'] + 'about')
                id = idf[1:]

                pg = gen.find('{' + ns['cim'] + '}' +
                              'RotatingMachine.p').text
                pgen = int(float(pg))*(-1)

                qg = gen.find('{' + ns['cim'] + '}' +
                              'RotatingMachine.q').text
                qgen = int(float(qg))*(-1)

                if eq.ID == id:
                    eq.P_Gen = pgen
                    eq.Q_Gen = qgen
                    # print(f'Generator updates: P = {pgen}, Q = {qgen}')
                    break
                else:
                    pass
        else:
            pass
    return(eq_file)


def updating_terminals(eq_file, root):
    for eq in eq_file:
        if eq.Type == 'Te':
            for term in root.findall('cim:Terminal', ns):
                idf = term.attrib.get(ns['rdf'] + 'about')
                id = idf[1:]

                in_serv = term.find('{' + ns['cim'] + '}' +
                                    'ACDCTerminal.connected').text.capitalize()

                if eq.ID == id:  # If terminal ID = SSH Terminal ID
                    cn_id = eq.CN  # Set Terminal CN connection ID = cn_id
                    ce_id = eq.CE  # Set Terminal CE connection ID = ce_id
                    for equip in eq_file:
                        if equip.ID == cn_id:
                            equip.InService = in_serv
                            # print(f'{equip.Name}, {equip.InService}')
                        if equip.ID == ce_id and equip.CE_Type == 'BusBar':
                            equip.InService = in_serv
                            # print(f'{equip.Name}, {equip.InService}')
                else:
                    pass
        else:
            pass
    return(eq_file)
