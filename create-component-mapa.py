import sys
from xml.dom import minidom

doc = minidom.parse("map-ufc.svg")

if doc.firstChild and doc.firstChild.nodeType == doc.firstChild.PROCESSING_INSTRUCTION_NODE:
    doc.removeChild(doc.firstChild)

svg = doc.documentElement

svg.setAttribute(':viewBox', 'viewBoxString')
svg.setAttribute('@wheel.prevent', 'handleWheel')
svg.setAttribute('@mousemove', 'handleMouseMove')
svg.setAttribute('@mousedown', 'handleMouseDown')
svg.setAttribute('class', 'map-svg')
svg.setAttribute('ref', 'svgElement')

with open('./src/components/MapSVG.vue', 'w') as file:
    file.write('<template>\n')
    file.write(doc.documentElement.toprettyxml(indent='    ', newl='\n'))
    file.write('</template>\n')