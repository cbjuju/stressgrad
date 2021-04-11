from odbAccess import *

################################################################################
#                           SUPPORT FUNCTIONS BEGIN                            #
################################################################################

def log(*theBits):
    """
    Function that writes a message to standard output instead of the rpy file.
    """
    message = ''
    for bit in theBits:
        message += str(bit)
 
    print >> sys.__stdout__, message

def get_elements_and_nodes(odbPath):
    """
    Function for getting element and node numbers from the odb.
    """
    # Open the odb file
    odb = openOdb(odbPath)

    # The entries of the following three lists contain more information than necessary
    allNodesObjects          = odb.rootAssembly.nodeSets[' ALL NODES'].nodes[0]
    allElementsObjects       = odb.rootAssembly.elementSets[' ALL ELEMENTS'].elements[0]
    log('Objects acquired')

    # The entries of the following three lists contain only information relevant to the repair
    allNodes          = []
    allElements       = []

    """
    Each entry of allNodes is a list with two elements in it : first the node label and
    second a list of the node coordinates.
    Each entry of allElements is also a list of two members : the first is the element
    number and the second is the element nodes. distortedElements is built the 
    same way as allElements.
    """

    for node in allNodesObjects:
        coordinates = list(node.coordinates)
        label       = node.label
        entry       = [label, coordinates]

        allNodes.append(entry)
    log('Node array created')

    for element in allElementsObjects:
        connectivity = list(element.connectivity)
        label        = element.label
        entry        = [label, connectivity]

        allElements.append(entry)
    log('All element array created')

    return allNodes, allElements

################################################################################
#                            SUPPORT FUNCTIONS END                             #
################################################################################

################################################################################
#                       ACTUAL POSTPROCESSING STARTING                         #
################################################################################

odb = openOdb('Job.odb')

allNodes, allElements = get_elements_and_nodes('Job.odb')

"""
part_instance = odb.rootAssembly.instances['PART-1-1']


1. Extract displacements
displacement of node 1 at the end of the simulation (hence the -1)
= odb.steps['Step-1'].frames[-1].fieldOutputs['U'].values[0].data (Gives an
array of 3 floats)

2. Extract stresses at integration points
Every element has 4 integration points. So the stress values for the first
element are :
odb.steps['Step-1'].frames[-1].fieldOutputs['S'].values[0].data
odb.steps['Step-1'].frames[-1].fieldOutputs['S'].values[1].data
odb.steps['Step-1'].frames[-1].fieldOutputs['S'].values[2].data
odb.steps['Step-1'].frames[-1].fieldOutputs['S'].values[3].data
The values for the first integration point of the 2 element is :
odb.steps['Step-1'].frames[-1].fieldOutputs['S'].values[4].data (Gives an array
of 6 floats)

3. Generate an array that contains the integration points and the stresses at
those points

Each entry of the list is also a list. The first member of each entry is an
identifier for the integration point whose stress is recorded. The identifier
is just the element number and the integration point smashed together. For
example, the stress at the 3rd integration point of the 1939th element will
have the identifier 19393. The next six entries are the components of the
stress tensor.  

This data is stored in an array called stress_data, which will have 4 * Ne
entries. Each entry has a length of 7, with the first entry being the
identifier and the remaining 6 being the stress components.
"""

number_of_elements = len(allElements) # Ne
number_of_nodes    = len(allNodes)    # Nn

stress_data_from_odb_for_last_frame = odb.steps['Step-1'].frames[-1].fieldOutputs['S']

stress_data = []

# Accumulate relevant data from stress_data_from_odb_for_last_frame into
# stress_data
for num in range(number_of_elements):
    element_number = num + 1

    # Each of the following four is a list of length 6
    stress_at_ip1 = stress_data_from_odb_for_last_frame.values[element_number + 0].data
    stress_at_ip2 = stress_data_from_odb_for_last_frame.values[element_number + 1].data
    stress_at_ip3 = stress_data_from_odb_for_last_frame.values[element_number + 2].data
    stress_at_ip4 = stress_data_from_odb_for_last_frame.values[element_number + 3].data

    # Building the identifiers for each integration point
    id_ip1 = element_number * 10 + 1
    id_ip2 = element_number * 10 + 2
    id_ip3 = element_number * 10 + 3
    id_ip4 = element_number * 10 + 4

    # Building each individual entry for the stress_data array
    entry_ip1 = [id_ip1] + stress_at_ip1
    entry_ip2 = [id_ip2] + stress_at_ip2
    entry_ip3 = [id_ip3] + stress_at_ip3
    entry_ip4 = [id_ip4] + stress_at_ip4

    # Append the entries to the stress_data array
    stress_data.append(entry_ip1)
    stress_data.append(entry_ip2)
    stress_data.append(entry_ip3)
    stress_data.append(entry_ip4)
