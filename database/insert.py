import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
import sys
from pathlib import Path
import json

engine = db.create_engine('postgresql://username:password@localhost/graphdb')
if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()
    if len(sys.argv) > 1:
        path = sys.argv[1]
        print(sys.argv)
        for item in Path(path).rglob('*.json'):
            print(item)
            try:
                content = open(item,'r').read()
                data = json.loads(content)
                library = data.get('library','')
                name = data.get('name','')

                graph = ComputeGraph()
                graph.model_name = name
                graph.library = library
                graph.model = data

                session.add(graph)
                session.commit()
                # TODO: schema validation
            except:
                print(f'not processing{item}')
