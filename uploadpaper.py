import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from PyPDF2 import PdfReader

import os
import argparse
from database.tables import Paper

import configparser

def upload_pdf(filename, session, title=''):
    pdfcontent = None
    try: 
        with open(filename, 'rb') as pdf_file:
            content = pdf_file.read()
            pdfcontent = content
            reader = PdfReader(pdf_file)
            if title == '':
                title = reader.metadata.title
    except FileNotFoundError:
        print("File not found.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    title = title if title else filename
    print(title)
    paper = Paper()
    paper.paper_name = title
    paper.contents = pdfcontent

    session.add(paper)
    session.commit()




if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='paper uploader')
    parser.add_argument('--paper', help='The full path to the paper to be uploaded into the database')
    parser.add_argument('--title', help='Set the title of the paper', default='')
    args = parser.parse_args()
    #parser.print_help()


    print(args.paper)

    if args.paper and os.path.exists(args.paper):
        config = configparser.ConfigParser()
        config.read('database.ini')


        engine = db.create_engine(f'postgresql://{config["database"]["user"]}:{config["database"]["password"]}@{config["database"]["host"]}/graphdb')
        Session = sessionmaker(bind=engine)
        session = Session()

        upload_pdf(args.paper, session, title = args.title)
