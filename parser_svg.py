import sys
import os
from xml.dom import minidom

print(sys.argv[1])
doc = minidom.parse(sys.argv[1])

os.mkdir('./map_parsed')

for group in reversed(doc.getElementsByTagName('g')):
    layer_name: str = group.getAttribute('inkscape:label')
    with open(f'./map_parsed/Layer{layer_name}.vue', 'w') as file:
        file.write('<template>\n')
        file.write(f'  <!-- Content for layer {layer_name} -->\n')
        file.write(group.toprettyxml(indent='    ', newl='\n'))
        file.write('</template>\n')