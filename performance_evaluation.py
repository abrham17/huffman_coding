"""
Performance Evaluation Module for Huffman Coding System
Uses FileOperations for all I/O + compression logic
"""

import time
import json
import csv
import os
from datetime import datetime
from typing import List, Dict
from file_operations import FileOperations


class PerformanceEvaluator:
    """Evaluate Huffman compression performance using real file operations"""

    def __init__(self):
        self.file_ops = FileOperations()

    # -----------------------------
    # CORE EVALUATION (FILE BASED)
    # -----------------------------
    def evaluate_file(self, input_path: str, description: str) -> dict:
        print(f"\n--- Testing: {description} ---")

        # compressed file uses .zip
        compressed_path = input_path + ".zip"

        # restored file
        base_name = os.path.splitext(input_path)[0]
        decompressed_path = base_name + "_restored.txt"

        # ---------------- Compression
        start_time = time.time()
        compression_ratio, space_savings = self.file_ops.compress_file(
            input_path, compressed_path
        )
        compression_time = time.time() - start_time

        # ---------------- Decompression
        start_time = time.time()
        self.file_ops.decompress_file(
            compressed_path,
            decompressed_path
        )
        decompression_time = time.time() - start_time

        # ---------------- Verification
        is_correct = self.file_ops.verify_compression(
            input_path,
            compressed_path,
            decompressed_path
        )

        # ---------------- File sizes (real disk size)
        original_size = self.file_ops.get_file_size(input_path) * 8
        compressed_size = self.file_ops.get_file_size(compressed_path) * 8

        result = {
            "description": description,
            "original_size": original_size,
            "compressed_size": compressed_size,
            "compression_ratio": compression_ratio,
            "space_savings": space_savings,
            "compression_time": compression_time,
            "decompression_time": decompression_time,
            "is_correct": is_correct
        }

        # ---------------- PRINT RESULTS
        print(f"Original size: {original_size:,} bits")
        print(f"Compressed size: {compressed_size:,} bits")
        print(f"Compression ratio: {compression_ratio:.2f}")
        print(f"Space savings: {space_savings:.1f}%")
        print(f"Compression time: {compression_time:.4f}s")
        print(f"Decompression time: {decompression_time:.4f}s")
        print(f"Verification: {'✓ PASSED' if is_correct else '✗ FAILED'}")

        return result

    # -----------------------------
    # RUN TESTS ON REAL FILE
    # -----------------------------
    def run_comprehensive_tests(self) -> List[dict]:
        print("=" * 60)
        print("HUFFMAN PERFORMANCE BENCHMARK (FILE BASED)")
        print("=" * 60)

        file_path = input("Enter path to test file: ").strip()

        results = []

        result = self.evaluate_file(file_path, "Real File Benchmark")
        results.append(result)

        self.generate_summary(results)
        self.save_json(results)
        self.save_csv(results)

        return results

    # -----------------------------
    # SUMMARY REPORT
    # -----------------------------
    def generate_summary(self, results: List[dict]):
        print("\n" + "=" * 60)
        print("SUMMARY REPORT")
        print("=" * 60)

        avg_ratio = sum(r["compression_ratio"] for r in results) / len(results)
        avg_savings = sum(r["space_savings"] for r in results) / len(results)

        best = max(results, key=lambda x: x["space_savings"])
        worst = min(results, key=lambda x: x["space_savings"])

        print(f"Average compression ratio: {avg_ratio:.2f}")
        print(f"Average space savings: {avg_savings:.1f}%")
        print(f"\nBest case: {best['description']} ({best['space_savings']:.1f}%)")
        print(f"Worst case: {worst['description']} ({worst['space_savings']:.1f}%)")

    # -----------------------------
    # SAVE AS JSON
    # -----------------------------
    def save_json(self, results: List[dict], filename: str = "huffman_results.json"):
        data = {
            "timestamp": datetime.now().isoformat(),
            "results": results
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print(f"\nSaved JSON → {filename}")

    # -----------------------------
    # SAVE AS CSV
    # -----------------------------
    def save_csv(self, results: List[dict], filename: str = "huffman_results.csv"):
        if not results:
            return

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

        print(f"Saved CSV → {filename}")


# -----------------------------
# RUN DIRECTLY
# -----------------------------
if __name__ == "__main__":
    evaluator = PerformanceEvaluator()
    evaluator.run_comprehensive_tests()