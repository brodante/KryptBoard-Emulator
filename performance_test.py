# performance_test.py
# This script measures the performance of the KryptBoard encryption function
# and generates graphs for the research paper.

import timeit
import os
import matplotlib.pyplot as plt
from Crypto.Random import get_random_bytes

# We import the exact encryption function from your project
from crypto_aead import aead_encrypt

def run_benchmarks():
    """
    Runs the performance tests and generates the graphs.
    """
    print("🚀 Starting KryptBoard performance benchmarks...")
    
    # --- Setup ---
    # A single, consistent 32-byte key for all tests
    key = get_random_bytes(32)
    
    # --- Benchmark 1: Performance Overhead (for Figure 2a) ---
    print("\n[1] Running overhead test for a 500-byte message...")
    overhead_msg_size = 500
    overhead_msg = os.urandom(overhead_msg_size)
    num_runs_overhead = 10000

    # Use a lambda to wrap the function call for timeit
    overhead_stmt = lambda: aead_encrypt(overhead_msg, key)
    
    total_time = timeit.timeit(overhead_stmt, number=num_runs_overhead)
    
    # Calculate average time in milliseconds (ms)
    avg_time_ms = (total_time / num_runs_overhead) * 1000
    
    print(f"    -> Average encryption time: {avg_time_ms:.6f} ms over {num_runs_overhead} runs.")
    
    
    # --- Benchmark 2: Encryption Scaling (for Figure 2b) ---
    print("\n[2] Running scaling test for various message sizes...")
    message_sizes = [100, 500, 1000, 2000, 5000, 10000, 20000]
    scaling_results_ms = []
    num_runs_scaling = 1000 # Fewer runs needed as messages get larger

    for size in message_sizes:
        msg = os.urandom(size)
        scaling_stmt = lambda: aead_encrypt(msg, key)
        total_time = timeit.timeit(scaling_stmt, number=num_runs_scaling)
        avg_time_ms_scaling = (total_time / num_runs_scaling) * 1000
        scaling_results_ms.append(avg_time_ms_scaling)
        print(f"    -> Size: {size:<5} bytes | Avg Time: {avg_time_ms_scaling:.6f} ms")
        
    
    # --- Plotting ---
    print("\n[3] Generating graphs...")
    plt.style.use('seaborn-v0_8-whitegrid') # A clean, academic style

    # Plot for Figure 2a: Overhead
    fig1, ax1 = plt.subplots(figsize=(5, 4))
    ax1.bar(['Encryption Overhead'], [avg_time_ms], width=0.4, color='skyblue')
    ax1.set_ylabel('Time (milliseconds)')
    ax1.set_title('Performance Overhead for a 500-Byte Message')
    ax1.set_ylim(0, avg_time_ms * 1.2) # Give a little space on top
    # Add the value label on top of the bar
    for i in ax1.patches:
        ax1.text(i.get_x() + i.get_width()/2, i.get_height() * 1.02, 
                f"{i.get_height():.4f} ms", ha='center', va='bottom')
    
    fig1.tight_layout()
    fig1.savefig("overhead-graph.pdf")
    print("    -> Saved 'overhead-graph.pdf'")

    # Plot for Figure 2b: Scaling
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.plot(message_sizes, scaling_results_ms, marker='o', linestyle='-', color='royalblue')
    ax2.set_xlabel('Message Size (bytes)')
    ax2.set_ylabel('Average Encryption Time (milliseconds)')
    ax2.set_title('ChaCha20-Poly1305 Encryption Scaling')
    ax2.grid(True)
    
    fig2.tight_layout()
    fig2.savefig("scaling-graph.pdf")
    print("    -> Saved 'scaling-graph.pdf'")
    
    print("\n✅ Benchmarks complete. Graphs are ready for your paper.")


if __name__ == "__main__":
    run_benchmarks()