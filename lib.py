from odbAccess import *
import sys

def console_log(*theBits):
    """
    Function that writes a message to standard output instead of the rpy file.
    """
    message = ''
    for bit in theBits:
        message += str(bit)
 
    print >> sys.__stdout__, message

def get_elements_and_nodes(odb):
    """
    Function for getting element and node numbers from the odb.
    """

    # The entries of the following three lists contain more information than necessary
    allNodesObjects          = odb.rootAssembly.nodeSets[' ALL NODES'].nodes[0]
    allElementsObjects       = odb.rootAssembly.elementSets[' ALL ELEMENTS'].elements[0]
    console_log('Objects acquired')

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
        entry       = [label] + coordinates

        allNodes.append(entry)
    console_log('Node array created')

    for element in allElementsObjects:
        connectivity = list(element.connectivity)
        label        = element.label
        entry        = [label] + connectivity

        allElements.append(entry)
    console_log('Element array created')

    # allNodes - Each entry is a list of 4 entries with the first one being the
    # node label and the last 3 being the initial nodal coordinates

    # allElements - Each entry is a list of 11 entries with the first one being
    # the element label and the last 10 being the node labels
    return allNodes, allElements

def get_stress_data(odb, number_of_elements):

    stress_data_from_odb_ = odb.steps['Step-1'].frames[-1].fieldOutputs['S']

    stress_data = []

    # accumulate relevant data from stress_data_from_odb_for_last_frame into
    # stress_data
    for num in range(number_of_elements):
        element_number = num + 1

        # each of the following four is a list of length 6
        stress_at_ip1 = stress_data_from_odb_.values[element_number + 0].data
        stress_at_ip2 = stress_data_from_odb_.values[element_number + 1].data
        stress_at_ip3 = stress_data_from_odb_.values[element_number + 2].data
        stress_at_ip4 = stress_data_from_odb_.values[element_number + 3].data

        # building the identifiers for each integration point
        # (works only because there are a single digit number of quadrature points)
        id_ip1 = element_number * 10 + 1
        id_ip2 = element_number * 10 + 2
        id_ip3 = element_number * 10 + 3
        id_ip4 = element_number * 10 + 4

        # building each individual entry for the stress_data array
        entry_ip1 = [id_ip1] + stress_at_ip1
        entry_ip2 = [id_ip2] + stress_at_ip2
        entry_ip3 = [id_ip3] + stress_at_ip3
        entry_ip4 = [id_ip4] + stress_at_ip4

        # append the entries to the stress_data array
        stress_data.append(entry_ip1)
        stress_data.append(entry_ip2)
        stress_data.append(entry_ip3)
        stress_data.append(entry_ip4)

    console_log ('Stress data acquired.')

    return stress_data

def get_displacement_data(odb, number_of_nodes):

    displacement_data = []

    displacement_data_from_odb_ = odb.steps['Step-1'].frames[-1].fieldOutputs['U']

    for num in range(number_of_nodes):
        node_number = num + 1

        # Get the displacements as an array of three floats
        displacements = displacement_data_from_odb_.values[node_number - 1].data

        # Generate the entry for the displacement_data array as one list with 4 entries
        entry = [node_number] + displacements

        # Append the entry to the displacement_data array
        displacement_data.append(entry)

    console_log ('Displacement data acquired')

    return displacement_data
