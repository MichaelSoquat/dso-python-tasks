import argparse
from PyPDF2 import PdfFileReader, PdfFileWriter

parser = argparse.ArgumentParser(description="Metadata analysis")
parser.add_argument('-f', required=True, type=str, help="Path to pdf")
parser.add_argument('-d', type=str, help="Path to folder with more pdf")
parser.add_argument('-n', type=str, help="Name for new file")

args = parser.parse_args()