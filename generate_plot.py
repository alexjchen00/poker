import pandas as pd
import matplotlib.pyplot as plt

# 1) Load data ---------------------------------------------------------------
df = pd.read_csv("poker_ev_per_hand.csv")  # path inside your repo

# 2) Add combo-counts and weight EV by deal frequency ------------------------
def combos(hand):
    """Return # of distinct combos for a starting hand."""
    if hand.endswith("s"):          # suited
        return 4
    if hand[0] == hand[1]:          # pair
        return 6
    return 12                       # offsuit

TOTAL_COMBOS = 1326  # 52 choose 2
df["Combos"]      = df["Hand"].apply(combos)
df["WeightedEV"]  = df["EV"] * df["Combos"] / TOTAL_COMBOS  # BB per *random* deal

# 3) Sort strongest → weakest and build cumulative sum ----------------------
df = df.sort_values("EV", ascending=False).reset_index(drop=True)
df["CumWeightedEV"] = df["WeightedEV"].cumsum()

# 4) Plot --------------------------------------------------------------------
plt.figure(figsize=(9,6))
plt.plot(range(1, len(df)+1), df["CumWeightedEV"], lw=2)

plt.xlabel("(starting from AA → 72o)")
plt.ylabel("Cumulative EV (bb per hand)")

plt.title(
    "Cumulative EV per hand in BB\n"
    "for all 169 Poker hands\n"
    "(weighted by deal frequency)"
)

plt.axhline(0, color="gray", ls="--", lw=1)
plt.xlim(0, 169)
plt.grid(alpha=0.3, ls="--")
plt.tight_layout()
plt.savefig("cumulative_EV_weighted_labels.png", dpi=300)
plt.show()
