import os
import subprocess

def run_all_cnf_with_main(cnf_dir="data/uf20-91", main_script="main.py"):
    """
    Searches for all .cnf files in the specified directory and runs main.py on each.
    """
    if not os.path.exists(cnf_dir):
        print(f"Directory not found: {cnf_dir}")
        return

    cnf_files = [f for f in os.listdir(cnf_dir) if f.endswith(".cnf")]
    cnf_files.sort()  # Optional: ensure consistent order

    for cnf_file in cnf_files:
        full_path = os.path.join(cnf_dir, cnf_file)
        print(f"Running: {full_path}")
        subprocess.run(["python", main_script, "--cnf", full_path], check=False)

if __name__ == "__main__":
    run_all_cnf_with_main()
