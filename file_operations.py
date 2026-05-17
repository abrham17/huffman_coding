import os
import argparse
from typing import Tuple
from huffman_coding import HuffmanCoding

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, 'data', 'input')
OUTPUT_DIR = os.path.join(BASE_DIR, 'data', 'output')

def ensure_parent_dir(file_path: str) -> None:
    parent_dir = os.path.dirname(file_path)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

def read_text_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_text_file(file_path: str, content: str):
    ensure_parent_dir(file_path)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def compress_file(input_path: str, output_path: str) -> Tuple[float, float]:
    huffman = HuffmanCoding()
    original_text = read_text_file(input_path)
    
    compressed_data = huffman.compress(original_text)
    
    ensure_parent_dir(output_path)
    with open(output_path, 'wb') as file:
        file.write(compressed_data)
    
    ratio = huffman.calculate_compression_ratio(original_text, compressed_data)
    savings = huffman.calculate_space_savings(original_text, compressed_data)
    return ratio, savings

def decompress_file(input_path: str, output_path: str) -> str:
    with open(input_path, 'rb') as file:
        compressed_data = file.read()
    
    huffman = HuffmanCoding()
    original_text = huffman.decompress(compressed_data)
    write_text_file(output_path, original_text)
    return original_text

def verify_compression(original_path: str, compressed_path: str, decompressed_path: str) -> bool:
    try:
        original_text = read_text_file(original_path)
        decompress_file(compressed_path, decompressed_path)
        decompressed_text = read_text_file(decompressed_path)
        return original_text == decompressed_text
    except Exception:
        return False

# Command-line interface
def main():
    parser = argparse.ArgumentParser(description="Huffman Compression System")
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    compress_parser = subparsers.add_parser('compress', help='Compress a file')
    compress_parser.add_argument('input', help='Input text file')
    compress_parser.add_argument('-o', '--output', help='Output compressed file')
    
    decompress_parser = subparsers.add_parser('decompress', help='Decompress a file')
    decompress_parser.add_argument('input', help='Input compressed file')
    decompress_parser.add_argument('-o', '--output', help='Output text file')
    
    analyze_parser = subparsers.add_parser('analyze', help='Analyze characters')
    analyze_parser.add_argument('input', help='Input text file')
    
    args = parser.parse_args()
    
    if args.command == 'compress':
        out_path = args.output or os.path.join(OUTPUT_DIR, os.path.basename(args.input) + '.zip')
        ratio, savings = compress_file(args.input, out_path)
        print(f"Compressed '{args.input}' to '{out_path}'")
        print(f"Ratio: {ratio:.2f} | Savings: {savings:.1f}%")
        
    elif args.command == 'decompress':
        out_path = args.output or os.path.join(OUTPUT_DIR, os.path.basename(args.input).replace('.zip', '') + '_restored.txt')
        decompress_file(args.input, out_path)
        print(f"Decompressed '{args.input}' to '{out_path}'")
        
    elif args.command == 'analyze':
        text = read_text_file(args.input)
        huffman = HuffmanCoding()
        freq = sorted(huffman.frequency_analysis(text).items(), key=lambda x: x[1], reverse=True)
        print(f"Total characters: {len(text)}")
        for char, count in freq[:20]:
            print(f"{repr(char)}: {count}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
