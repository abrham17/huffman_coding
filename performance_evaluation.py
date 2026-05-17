"""
Performance Evaluation Module for Huffman Coding System
Uses FileOperations for all I/O + compression logic
"""

import time
import json
import csv
import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from typing import List, Dict
from file_operations import compress_file, decompress_file, verify_compression, read_text_file


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "data", "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "output")
REPORTS_DIR = os.path.join(BASE_DIR, "data", "reports")


class PerformanceEvaluator:
    """Evaluate Huffman compression performance using real file operations"""

    # -----------------------------
    # CORE EVALUATION (FILE BASED)
    # -----------------------------
    def evaluate_file(self, input_path: str, description: str) -> dict:
        print(f"\n--- Testing: {description} ---")

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        os.makedirs(REPORTS_DIR, exist_ok=True)

        # compressed file uses .zip inside the output folder
        compressed_name = os.path.basename(input_path) + ".zip"
        compressed_path = os.path.join(OUTPUT_DIR, compressed_name)

        # restored file inside the output folder
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        decompressed_path = os.path.join(OUTPUT_DIR, base_name + "_restored.txt")

        # ---------------- Compression
        start_time = time.time()
        compression_ratio, space_savings = compress_file(
            input_path, compressed_path
        )
        compression_time = time.time() - start_time

        # ---------------- Decompression
        start_time = time.time()
        decompress_file(
            compressed_path,
            decompressed_path
        )
        decompression_time = time.time() - start_time

        # ---------------- Verification
        is_correct = verify_compression(
            input_path,
            compressed_path,
            decompressed_path
        )

        # ---------------- File sizes (real disk size in bytes)
        original_size = len(read_text_file(input_path).encode('utf-8'))
        compressed_size = os.path.getsize(compressed_path)

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
        print(f"Original size: {original_size:,} bytes")
        print(f"Compressed size: {compressed_size:,} bytes")
        print(f"Compression ratio: {compression_ratio:.2f}")
        print(f"Space savings: {space_savings:.1f}%")
        print(f"Compression time: {compression_time:.4f}s")
        print(f"Decompression time: {decompression_time:.4f}s")
        print(f"Verification: {'✓ PASSED' if is_correct else '✗ FAILED'}")

        return result

    # -----------------------------
    # RUN TESTS ON REAL FILES
    # -----------------------------
    def run_comprehensive_tests(self) -> List[dict]:
        print("=" * 60)
        print("HUFFMAN PERFORMANCE BENCHMARK")
        print("=" * 60)

        # Test files as assigned
        test_files = [
            (os.path.join(INPUT_DIR, "alice29.txt"), "Natural Language (Alice29)"),
            (os.path.join(INPUT_DIR, "bible.txt"), "Large Document (Bible)"),
            (os.path.join(INPUT_DIR, "repetitive_stats.txt"), "Highly Skewed (Stats)"),
            (os.path.join(INPUT_DIR, "alphabet.txt"), "Uniform Character (Alphabet)"),
            (os.path.join(INPUT_DIR, "random.txt"), "High Entropy (Random)"),
        ]

        results = []
        
        for file_path, description in test_files:
            if os.path.exists(file_path):
                result = self.evaluate_file(file_path, description)
                results.append(result)
            else:
                print(f"\nWarning: Test file '{file_path}' not found, skipping...")

        if results:
            self.generate_summary(results)
            self.save_json(results)
            self.save_csv(results)
            self.generate_charts(results)

        return results

    # -----------------------------
    # GENERATE CHARTS
    # -----------------------------
    def generate_charts(self, results: List[dict]):
        labels = [
            r["description"].replace(" ", "\n", 1).replace("(", "\n(").replace(")","") 
            for r in results
        ]
        savings = [r["space_savings"] for r in results]
        ratios = [r["compression_ratio"] for r in results]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        
        # Plot 1: Space Savings Percentage (How much smaller it got)
        bars1 = ax1.bar(labels, savings, color=['#4CAF50', '#2E86C1', '#9B59B6', '#E67E22', '#E74C3C'])
        ax1.set_ylabel('Space Savings (%)')
        ax1.set_title('Compression Efficiency (Higher is Better)')
        ax1.set_ylim(0, 100)
        ax1.bar_label(bars1, fmt='%.1f%%', padding=3)

        # Plot 2: Compression Ratio (How many times smaller)
        bars2 = ax2.bar(labels, ratios, color='skyblue')
        ax2.set_ylabel('Compression Ratio (Original / Compressed)')
        ax2.set_title('Compression Ratio (Higher is Better)')
        ax2.bar_label(bars2, fmt='%.2fx', padding=3)

        plt.suptitle("Huffman Coding Performance Analysis", fontsize=14, fontweight='bold')
        fig.tight_layout()
        chart_path = os.path.join(REPORTS_DIR, "performance_chart.png")
        plt.savefig(chart_path)
        print(f"Saved Chart → {chart_path}")

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

        os.makedirs(REPORTS_DIR, exist_ok=True)
        filename = os.path.join(REPORTS_DIR, filename)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print(f"\nSaved JSON → {filename}")

    # -----------------------------
    # SAVE AS CSV
    # -----------------------------
    def save_csv(self, results: List[dict], filename: str = "huffman_results.csv"):
        if not results:
            return

        os.makedirs(REPORTS_DIR, exist_ok=True)
        filename = os.path.join(REPORTS_DIR, filename)

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