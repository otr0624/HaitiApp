import click
import xml.etree.ElementTree as et
from pathlib import Path
from database import db
from hca.patients.patient_model import (
    Diagnosis,
    DiagnosisSchema
)


def register(app):

    @app.cli.group()
    def ict():
        """Load and manipulate ICD-10 data"""
        pass

    @ict.command()
    @click.argument('filename')
    def load(filename):
        """ Load ICD-10 data downloaded from https://www.cms.gov/Medicare/Coding/ICD10 """

        # Verify the file exists
        p = Path(filename)
        if not p.exists():
            print(f'File not found: {filename}')
            return

        # Load the ICT-10 XML file
        print(f'Loading ICT-10 date from {p.resolve()}')
        tree = et.parse(filename)
        root_node = tree.getroot()
        
        # ICT schema is nested tree of <diag> elements.
        # We'll flatten into SQL table, but keep track of
        # depth from section as we recurse through nodes
        depth = 0

        for section_node in root_node.findall('chapter/section'):

            #   <section id="C15-C26">
            #       <desc>Malignant neoplasms of digestive organs (C15-C26)</desc>
            #       <diag>
            #           ...
            #       </diag>
            section_name = section_node.attrib['id']
            section_desc = section_node.find('.desc').text
            print(f'{section_name} : {section_desc}')

            # Build and load a Diagnosis record for each child <diag> node
            for diag_node in section_node.findall('.diag'):
                load_diag_node(section_name, section_desc, depth, diag_node)

            # Batch up db.add() and commit at the end of every section
            db.session.commit()

    def load_diag_node(section_name, section_desc, depth, diag_node):

        # Load current diagnosis node
        d = Diagnosis()
        d.depth = depth

        d.icd_section_name = section_name
        d.icd_section_desc = section_desc

        # <diag>
        #     <name>J01</name>
        #     <desc>Acute sinusitis</desc>
        #     <diag>
        #         <name>J01.0</name>
        #         <desc>Acute maxillary sinusitis</desc>
        #         <diag>
        #             <name>J01.00</name>
        #             <desc>Acute maxillary sinusitis, unspecified</desc>
        #         </diag>
        #     </diag>
        # </diag>

        d.icd_diagnosis_name = diag_node.find('.name').text
        d.icd_diagnosis_desc = diag_node.find('.desc').text

        db.session.add(d)

        print(DiagnosisSchema().dump(d))

        # Recursively load child nodes
        for child_diag_node in diag_node.findall('.diag'):
            load_diag_node(
                section_name,
                section_desc,
                depth + 1,
                child_diag_node)
