from lib import *

"""
part_instance = odb.rootAssembly.instances['PART-1-1']

1. Extract stresses at integration points
Every element has 4 integration points. So the stress values for the first
element are :
odb.steps['Step-1'].frames[-1].fieldOutputs['S'].values[0].data
odb.steps['Step-1'].frames[-1].fieldOutputs['S'].values[1].data
odb.steps['Step-1'].frames[-1].fieldOutputs['S'].values[2].data
odb.steps['Step-1'].frames[-1].fieldOutputs['S'].values[3].data
The values for the first integration point of the 2 element is :
odb.steps['Step-1'].frames[-1].fieldOutputs['S'].values[4].data (Gives an array
of 6 floats)

2. Extract displacements
displacement of node 1 at the end of the simulation (hence the -1)
= odb.steps['Step-1'].frames[-1].fieldOutputs['U'].values[0].data (Gives an
array of 3 floats)

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

odb_path = '/home/skunda/problems/cylinderCompression/fivePercentQuadTets/Job.odb'

odb = openOdb(odb_path)

allNodes, allElements = get_elements_and_nodes(odb)

number_of_elements = len(allElements) # Ne
number_of_nodes    = len(allNodes)    # Nn

stress_data = get_stress_data(odb, number_of_elements)

displacement_data = get_displacement_data(odb, number_of_nodes)
