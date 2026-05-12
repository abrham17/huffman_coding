import os
from typing import Tuple
from huffman_coding import HuffmanCoding
import argparse

class FileOperations:
    """Handle file I/O operations for Huffman compression"""
    
    def __init__(self):
        self.huffman = HuffmanCoding()
    
    def read_text_file(self, file_path: str) -> str:
        """Read text file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise Exception(f"Error reading file {file_path}: {str(e)}")
    
    def write_text_file(self, file_path: str, content: str):
        """Write text content to file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
        except Exception as e:
            raise Exception(f"Error writing file {file_path}: {str(e)}")
    
    def compress_file(self, input_path: str, output_path: str) -> Tuple[float, float]:
        """Compress a text file and save compressed data"""
        # Read original file
        original_text = self.read_text_file(input_path)
        
        # Compress the text
        compressed_data = self.huffman.compress(original_text)
        
        # Save compressed data
        with open(output_path, 'wb') as file:
            file.write(compressed_data)
        
        # Calculate metrics
        compression_ratio = self.huffman.calculate_compression_ratio(original_text, compressed_data)
        space_savings = self.huffman.calculate_space_savings(original_text, compressed_data)
        
        return compression_ratio, space_savings
    
    def decompress_file(self, input_path: str, output_path: str) -> str:
        """Decompress a file and save original text"""
        # Read compressed data
        with open(input_path, 'rb') as file:
            compressed_data = file.read()
        
        # Decompress
        original_text = self.huffman.decompress(compressed_data)
        
        # Save decompressed text
        self.write_text_file(output_path, original_text)
        
        return original_text
    
    def get_file_size(self, file_path: str) -> int:
        """Get file size in bytes"""
        return os.path.getsize(file_path)
    
    def compare_file_sizes(self, original_path: str, compressed_path: str) -> Tuple[int, int, float]:
        """Compare original and compressed file sizes"""
        original_size = self.get_file_size(original_path)
        compressed_size = self.get_file_size(compressed_path)
        size_ratio = original_size / compressed_size if compressed_size > 0 else 0
        return original_size, compressed_size, size_ratio
    
    def verify_compression(self, original_path: str, compressed_path: str, decompressed_path: str) -> bool:
        """Verify that decompressed file matches original"""
        try:
            # Read original
            original_text = self.read_text_file(original_path)
            
            # Decompress to the specified path
            self.decompress_file(compressed_path, decompressed_path)
            
            # Read decompressed
            decompressed_text = self.read_text_file(decompressed_path)
            
            # Compare
            return original_text == decompressed_text
        except Exception as e:
            print(f"Verification error: {str(e)}")
            return False


# Command-line interface functions
def compress_file(input_file, output_file=None, show_stats=True):
    """Compress a file using Huffman coding"""
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        return False
    
    if output_file is None:
        output_file = input_file + '.zip'
    
    try:
        file_ops = FileOperations()
        compression_ratio, space_savings = file_ops.compress_file(input_file, output_file)
        
        if show_stats:
            original_size = os.path.getsize(input_file)
            compressed_size = os.path.getsize(output_file)
            
            print(f"  Successfully compressed '{input_file}'")
            print(f"  Original size: {original_size:,} bytes")
            print(f"  Compressed size: {compressed_size:,} bytes")
            print(f"  Compression ratio: {compression_ratio:.2f}")
            print(f"  Space savings: {space_savings:.1f}%")
            print(f"  Output file: '{output_file}'")
        
        return True
        
    except Exception as e:
        print(f"Error compressing file: {str(e)}")
        return False


def decompress_file(input_file, output_file=None, verify=True):
    """Decompress a Huffman-compressed file"""
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        return False
    
    if output_file is None:
        if input_file.endswith('.zip'):
            output_file = input_file[:-4]
        else:
            output_file = input_file + '_decompressed.txt'
    
    try:
        file_ops = FileOperations()
        file_ops.decompress_file(input_file, output_file)
        
        if verify:
            is_correct = file_ops.verify_compression(
                output_file, input_file, output_file + '_temp'
            )
            os.remove(output_file + '_temp')  # Clean up temp file
            
            if is_correct:
                print(f"  Successfully decompressed '{input_file}'")
                print(f"  Output file: '{output_file}'")
                print(f"  Verification: PASSED")
            else:
                print(f"  Decompression failed verification")
                return False
        else:
            print(f"  Successfully decompressed '{input_file}'")
            print(f"  Output file: '{output_file}'")
        
        return True
        
    except Exception as e:
        print(f"Error decompressing file: {str(e)}")
        return False


def show_frequency_analysis(input_file):
    """Show frequency analysis of a text file"""
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        return
    
    try:
        file_ops = FileOperations()
        text = file_ops.read_text_file(input_file)
        
        print(f"Frequency Analysis for '{input_file}'")
        print("=" * 50)
        
        frequency = file_ops.huffman.frequency_analysis(text)
        total_chars = len(text)
        
        # Sort by frequency
        sorted_freq = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
        
        print(f"Total characters: {total_chars:,}")
        print(f"Unique characters: {len(sorted_freq)}")
        print(f"Character diversity: {(len(sorted_freq) / total_chars) * 100:.2f}%")
        
        print("\nCharacter frequency distribution:")
        print("-" * 30)
        
        for i, (char, freq) in enumerate(sorted_freq[:20]):  # Show top 20
            percentage = (freq / total_chars) * 100
            display_char = repr(char) if char.isspace() else char
            print(f"{i+1:2d}. '{display_char}': {freq:6d} ({percentage:5.2f}%)")
        
        if len(sorted_freq) > 20:
            print(f"... and {len(sorted_freq) - 20} more characters")
        
    except Exception as e:
        print(f"Error analyzing file: {str(e)}")


def main():
    """Main function with command-line interface"""
    parser = argparse.ArgumentParser(
        description="Huffman Coding Lossless Text Compression System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python file_operations.py compress document.txt
  python file_operations.py compress document.txt -o compressed.zip
  python file_operations.py decompress compressed.zip
  python file_operations.py decompress compressed.zip -o restored.txt
  python file_operations.py analyze document.txt
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Compress command
    compress_parser = subparsers.add_parser('compress', help='Compress a text file')
    compress_parser.add_argument('input', help='Input text file to compress')
    compress_parser.add_argument('-o', '--output', help='Output compressed file')
    compress_parser.add_argument('--no-stats', action='store_true', 
                               help='Don\'t show compression statistics')
    
    # Decompress command
    decompress_parser = subparsers.add_parser('decompress', help='Decompress a file')
    decompress_parser.add_argument('input', help='Input compressed file')
    decompress_parser.add_argument('-o', '--output', help='Output text file')
    decompress_parser.add_argument('--no-verify', action='store_true',
                                  help='Skip verification after decompression')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze character frequency')
    analyze_parser.add_argument('input', help='Input text file to analyze')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Run performance tests')
    
    args = parser.parse_args()
    
    if args.command == 'compress':
        compress_file(args.input, args.output, not args.no_stats)
    
    elif args.command == 'decompress':
        decompress_file(args.input, args.output, not args.no_verify)
    
    elif args.command == 'analyze':
        show_frequency_analysis(args.input)
    
    elif args.command == 'test':
        evaluator = PerformanceEvaluator()
        evaluator.run_comprehensive_tests()
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
