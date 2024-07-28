import subprocess
import argparse

def delete_meta_exif(input_file:str, output_file:str):
    try:
        command = f'exiftool -all= -o {output_file} {input_file}'
        subprocess.run(command, shell=True, check=True)
        print(f"Success! Output is: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error occured removing the meta data with Exiftool: {e}")

def linearize(input_file:str, output_file:str):
    try:
        command = f'qpdf --linearize --object-streams=disable {input_file} {output_file}'
        subprocess.run(command, shell=True, check=True)
        print(f"Success! Output: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error occured removing the meta data with QPDF: {e}")

def main():
    parser = argparse.ArgumentParser(description="Delete meta data")
    parser.add_argument('-i', '--input', 
                        required=True, 
                        help='Path: Input PDF')
    parser.add_argument('-o', '--output', 
                        required=True, 
                        help='Path: Output PDF')

    args = parser.parse_args()

    input_file = args.input
    output_file = args.output
    delete_meta_exif(input_file, output_file)
    linearize(input_file, output_file)


if __name__ == "__main__":
    main()