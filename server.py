from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from concurrent.futures import ThreadPoolExecutor
import xml.etree.ElementTree as ET

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class NoteServer:
    def __init__(self, filename):
        self.filename = filename
        try:
            self.tree = ET.parse(filename)
            self.root = self.tree.getroot
        except FileNotFoundError:
            self.tree = ET.ElementTree(ET.Element("data"))
            self.root = self.tree.getroot()
        except ET.ParseError as e:
            print(f"Error parsing the database: {e}")
            self.tree = ET.ElementTree(ET.Element("data"))
            self.root = self.tree.getroot()

    def add_note(self, topic, note_name, text, timestamp):
        for t in self.root.findall('topic'):
            if t.get('name') == topic:
                ET.SubElement(t, 'note', name=note_name).extend([
                    ET.Element('text', text=text),
                    ET.Element('timestamp', timestamp=timestamp)
                ])
                try:
                    self.tree.write(self.filename)
                except Exception as e:
                    print(f"Error writing to file: {e}")
                    return False
                return
        ET.SubElement(self.root, 'topic', name=topic).extend([
            ET.Element('note', name=note_name).extend([
                ET.Element('text', text=text),
                ET.Element('timestamp', timestamp=timestamp)
            ])
        ])
        try:
            self.tree.write(self.filename)
        except Exception as e:
            print(f"Error writing to file: {e}")
            return False
        return

    def get_notes(self, topic):
        for t in self.root.findall('topic'):
            if t.get('name') == topic:
                notes = []
                for note in t.findall('note'):
                    name = note.get("name")
                    text = note.find("text").text.strip()
                    timestamp = note.find("timestamp").text.strip()
                    notes.append({"name": name, "text": text, "timestamp": timestamp})
                return notes
        return 'Topic not found'

server = SimpleXMLRPCServer(("localhost", 8000), requestHandler=RequestHandler, allow_none=True)
server.register_introspection_functions()

note_server = NoteServer('db.xml')
server.register_instance(note_server)
print("Server is online")
server.serve_forever()