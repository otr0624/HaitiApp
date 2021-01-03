import click
import xml.etree.ElementTree as et
from pathlib import Path


def register(app):

    @app.cli.group()
    def ict():
        """Load and manipulate ICD-10 data"""
        pass

    @ict.command()
    @click.argument('filename')
    def load(filename):
        """ Load ICD-10 data downloaded from https://www.cms.gov/Medicare/Coding/ICD10 """

        p = Path(filename)

        if not p.exists():
            print(f'File not found: {filename}')
            return

        print(f'Loading ICT-10 date from {p.resolve()}')
        tree = et.parse(filename)

        print(tree.getroot())
