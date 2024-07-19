import os
import csv
import argparse
from PyPDF2 import PdfReader

def extract_pdf_metadata(file_path):
    metadata = {
        'Author': 'undefined',
        'Creator': 'undefined',
        'Created': 'undefined',
        'Modified': 'undefined',
        'Subject': 'undefined',
        'Keywords': 'undefined',
        'Description': 'undefined',
        'Producer': 'undefined',
        'PDF Version': 'undefined'
    }
    try:
        pdf = PdfReader(file_path)
        meta = pdf.metadata

        metadata['Author'] = meta.get('/Author', 'undefined')
        metadata['Creator'] = meta.get('/Creator', 'undefined')
        metadata['Created'] = meta.get('/CreationDate', 'undefined')
        metadata['Modified'] = meta.get('/ModDate', 'undefined')
        metadata['Subject'] = meta.get('/Subject', 'undefined')
        metadata['Keywords'] = meta.get('/Keywords', 'undefined')
        metadata['Description'] = meta.get('/Description', 'undefined')
        metadata['Producer'] = meta.get('/Producer', 'undefined')   
        metadata['PDF Version'] = pdf.trailer.get('/Version', 'undefined')
    except Exception as e:
        print(f'Error extracting metadata from {file_path}: {e}')
    return metadata

def extract_one_file(file_path, csv_path):
    metadata = extract_pdf_metadata(file_path)
    with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Author', 'Creator', 'Created', 'Modified', 'Subject', 'Keywords', 'Description', 'Producer', 'PDF Version']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerow(metadata)
    print(f'Metadata saved to following path: {csv_path}')

def extract_dir(directory_path, csv_path):
    metadata_list = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                file_path = os.path.join(root, file)
                metadata = extract_pdf_metadata(file_path)
                metadata_list.append(metadata)

    with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Title', 'Author', 'Creator', 'Created', 'Modified', 'Subject', 'Keywords', 'Description', 'Producer', 'PDF Version']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for metadata in metadata_list:
            writer.writerow(metadata)
    print(f'Metadata saved to following path: {csv_path}')

def main():
    parser = argparse.ArgumentParser(description="Extract metadata from PDF")
    parser.add_argument('-f', '--file', help='Path to one PDF')
    parser.add_argument('-d', '--directory', help='Path to directory')
    parser.add_argument('-n', '--name', required=True, help='Output csv file name')

    args = parser.parse_args()

    if not args.file and not args.directory:
        parser.error("Please enter -f or -d")
    if args.file:
        extract_one_file(args.file, args.name)
    elif args.directory:
        print('dir')
        extract_dir(args.directory, args.name)

if __name__ == "__main__":
    main()
