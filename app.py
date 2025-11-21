

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------
# Dashboard Title and Context
# ---------------------------------------
st.title("Gordon–Loeb Model: Cybersecurity Investment")
st.markdown(
    """
    This dashboard implements the specific **Cost-Benefit Analysis** approach detailed in 
    *Integrating Cost-Benefit Analysis into the NIST Cybersecurity Framework via the Gordon-Loeb Model (2020)*.
    
    It uses the specific probability function: $s(z,v) = v / (1 + z/2)$.
    """
)

# ---------------------------------------
# Sidebar Inputs
# ---------------------------------------
st.sidebar.header("Input Parameters")

# Updated range to match the paper's example (up to $150M)
L_input = st.sidebar.slider(
    "Potential Loss (L) in Millions ($)",
    min_value=1.0,
    max_value=150.0,
    value=72.6,
    step=0.1,
    help="Financial loss if the asset is compromised (in Millions)."
)

v_input = st.sidebar.slider(
    "Vulnerability (v)",
    min_value=0.0,
    max_value=1.0,
    value=0.3,
    step=0.05,
    help="Probability of a breach occurring before investment."
)

# ---------------------------------------
# The Corrected Formula (from Page 6)
# ---------------------------------------
def calculate_optimal_investment(v, L):
    # Formula: z* = sqrt(2vL) - 2
    # Note: L is treated as the raw value. If L is passed in Millions, z is in Millions.
    
    # Calculate term under square root
    term = 2 * v * L
    
    # Prevent math error if term is negative (though v and L are positive)
    if term < 0:
        return 0.0
        
    z = np.sqrt(term) - 2
    
    # Investment cannot be negative
    return max(0.0, z)

# Calculate for user input
optimal_z = calculate_optimal_investment(v_input, L_input)

# ---------------------------------------
# Sidebar Output
# ---------------------------------------
st.sidebar.write("---")
st.sidebar.subheader("Model Output")
st.sidebar.metric("Optimal Investment (z*)", f"${optimal_z:,.2f} M")

# Determine NIST Tier based on the Example in Paper (Page 6/7)
# Tiers thresholds used in the paper: z=0.1, z=1, z=3, z=7
tier = "Tier 1 (Partial)"
if optimal_z >= 7.0:
    tier = "Tier 4 (Adaptive)"
elif optimal_z >= 3.0:
    tier = "Tier 3 (Repeatable)"
elif optimal_z >= 1.0:
    tier = "Tier 2 (Risk Informed)"

st.sidebar.info(f"Implied NIST Level: **{tier}**")

# ---------------------------------------
# Replication of Figure 1 (Page 7)
# ---------------------------------------
st.subheader("Optimal Investment vs. Potential Loss")
st.write(
    "This graph replicates **Figure 1** from the paper, showing how optimal investment ($z^*$) "
    "increases with Potential Loss ($L$). The dots represent the user's current selection."
)

# Generate data for the plot
L_range = np.linspace(0, 150, 300) # L from 0 to 150 Million

# Calculate curves for v=0.1, v=0.3, v=0.5 (The paper's examples)
z_v1 = [calculate_optimal_investment(0.1, l) for l in L_range]
z_v3 = [calculate_optimal_investment(0.3, l) for l in L_range]
z_v5 = [calculate_optimal_investment(0.5, l) for l in L_range]
z_user = [calculate_optimal_investment(v_input, l) for l in L_range]

fig, ax = plt.subplots(figsize=(10, 6))

# Plot reference lines from the paper
ax.plot(L_range, z_v5, label='v = 0.5 (High Vuln)', color='gray', linestyle='--', alpha=0.6)
ax.plot(L_range, z_v3, label='v = 0.3 (Med Vuln)', color='gray', linestyle=':', alpha=0.6)
ax.plot(L_range, z_v1, label='v = 0.1 (Low Vuln)', color='gray', linestyle='-.', alpha=0.6)

# Plot User's Dynamic Line
ax.plot(L_range, z_user, label=f'Current User Input (v={v_input})', color='blue', linewidth=2)

# Plot the specific user point
ax.scatter([L_input], [optimal_z], color='red', zorder=5, s=100, label="Your Selection")

# Add NIST Tier Threshold lines (Horizontal) as seen in Figure 1
ax.axhline(y=7, color='purple', linestyle='-', linewidth=0.8, alpha=0.5)
ax.text(5, 7.2, 'Tier 4 Threshold ($7M)', color='purple', fontsize=8)

ax.axhline(y=3, color='purple', linestyle='-', linewidth=0.8, alpha=0.5)
ax.text(5, 3.2, 'Tier 3 Threshold ($3M)', color='purple', fontsize=8)

ax.axhline(y=1, color='purple', linestyle='-', linewidth=0.8, alpha=0.5)
ax.text(5, 1.2, 'Tier 2 Threshold ($1M)', color='purple', fontsize=8)

ax.set_xlabel("Potential Loss (L) in Millions ($)")
ax.set_ylabel("Optimal Investment (z) in Millions ($)")
ax.set_title("Replication of Figure 1: Optimal Investment Levels")
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)

# ---------------------------------------
# Paper Explanation
# ---------------------------------------
st.markdown("### Explanation of the Calculation")
st.latex(r"z^* = \sqrt{2vL} - 2")
st.write(
    """
    This formula is derived by minimizing the total expected cost function:
    $$ E(z) = \\frac{vL}{(1 + z/2)} + z $$
    
    As noted in the paper:
    * **Low L or Low v**: Investment is 0 (Benefits don't outweigh costs).
    * **Diminishing Returns**: Investment increases with L, but at a decreasing rate.
    """
)
