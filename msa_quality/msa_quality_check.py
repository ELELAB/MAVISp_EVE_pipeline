import os
import pandas as pd
import glob
import sys

# ============================
# Paths
# ============================
pfam_file = "mavisp_unique_pfam.csv"  # PFAM output (must have 'protein' column)
msa_base_dir = "/data/databases/EVE/local_MSA"
output_file = "/data/user/shared_projects/mavisp_EVE_protocol/mavisp_data/28082025_onlyEVE/edeni95/msa_quality_report.csv"

# Ensure output directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# ============================
# Read PFAM input
# ============================
pfam_df = pd.read_csv(pfam_file)
pfam_df_unique = pfam_df.drop_duplicates(subset=["protein"])

# Map protein → Uniprot if available
protein_to_uniprot = dict(zip(pfam_df["protein"], pfam_df.get("uniprot_ac", ["NA"]*len(pfam_df))))

# ============================
# Classification function
# ============================
def classify_msa(len_cov, seqlen, num_seqs):
    Lcov = len_cov
    L = seqlen
    N = num_seqs

    if Lcov >= 0.8 * L and 10 * L <= N <= 100000:
        return "strict"
    elif Lcov >= 0.7 * L and N <= 200000:
        return "relaxed"
    else:
        return "none"

# ============================
# Command line option: run specific proteins
# ============================
if len(sys.argv) > 1:
    selected_proteins = sys.argv[1:]  # accept multiple proteins
else:
    selected_proteins = list(pfam_df_unique["protein"])

# ============================
# Collect available protein dirs
# ============================
available_proteins = {d for d in os.listdir(msa_base_dir) if os.path.isdir(os.path.join(msa_base_dir, d))}

output_data = []
missing_proteins = []
no_stats_proteins = []

# ============================
# Loop through selected proteins
# ============================
for protein in selected_proteins:
    if protein not in available_proteins:
        missing_proteins.append(protein)
        continue

    # Search recursively for stats files in this protein folder
    stat_files = glob.glob(os.path.join(msa_base_dir, protein, "**", "*_alignment_statistics.csv"), recursive=True)

    if not stat_files:
        no_stats_proteins.append(protein)
        continue

    # Use the first stats file found
    stats_file = stat_files[0]
    stats_df = pd.read_csv(stats_file)

    if stats_df.empty:
        no_stats_proteins.append(protein)
        continue

    # Extract required values
    len_cov = stats_df.iloc[0]["len_cov"]
    seqlen = stats_df.iloc[0]["seqlen"]
    num_seqs = stats_df.iloc[0]["num_seqs"]

    quality = classify_msa(len_cov, seqlen, num_seqs)

    output_data.append({
        "protein": protein,
        "uniprot": protein_to_uniprot.get(protein, "NA"),
        "num_seqs": num_seqs,
        "coverage": len_cov,
        "seqlen": seqlen,
        "quality": quality,
        "stats_file": stats_file
    })

# ============================
# Save output
# ============================
output_df = pd.DataFrame(output_data)
output_df.to_csv(output_file, index=False)

# ============================
# Summary
# ============================
print("="*60)
print(f"Proteins requested: {len(selected_proteins)}")
print(f"Proteins with valid stats: {len(output_df)}")
print(f"Proteins missing folder in {msa_base_dir}: {len(missing_proteins)}")
print(f"Proteins with folder but no stats file: {len(no_stats_proteins)}")

if missing_proteins:
    print("\nMissing folder proteins:", missing_proteins)
if no_stats_proteins:
    print("\nNo stats file found:", no_stats_proteins)

if not output_df.empty:
    print("\nQuality classification counts:")
    print(output_df["quality"].value_counts())
    print(f"\nReport saved to {output_file}")
else:
    print("\nNo data written — check protein names or folder structure.")
