# ============================================================
#   EXPLORATORY DATA ANALYSIS (EDA) - Netflix Titles Dataset
# ============================================================
# Topics Covered:
#   1. Load & Understand the Dataset
#   2. Clean Missing Values & Outliers
#   3. Summary Statistics
#   4. Univariate Analysis & Charts
#   5. Bivariate Analysis & Relationships
#   6. Hypothesis Testing & p-values
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings

warnings.filterwarnings("ignore")

# ── Style ────────────────────────────────────────────────────
plt.rcParams["figure.figsize"] = (10, 5)
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.labelsize"] = 12
sns.set_theme(style="whitegrid", palette="Set2")

# ============================================================
# SECTION 1 ── LOAD & UNDERSTAND THE DATASET
# ============================================================
print("\n" + "=" * 60)
print("  SECTION 1: LOAD & UNDERSTAND THE DATASET")
print("=" * 60)

# Download dataset automatically (no manual download needed)
url = (
    "https://raw.githubusercontent.com/DataScienceRoadMapDSRM/"
    "Datasets/main/netflix_titles.csv"
)

try:
    df = pd.read_csv(url)
    print(f"\n✅ Dataset loaded successfully from URL.")
except Exception:
    # Fallback: generate a representative synthetic dataset
    print("\n⚠️  URL unreachable. Generating synthetic Netflix-like dataset…")
    np.random.seed(42)
    n = 1000
    types    = np.random.choice(["Movie", "TV Show"], n, p=[0.7, 0.3])
    years    = np.random.randint(2000, 2022, n)
    ratings  = np.random.choice(
        ["TV-MA", "TV-14", "TV-PG", "PG-13", "R", "G", "NR"],
        n, p=[0.35, 0.25, 0.15, 0.10, 0.08, 0.04, 0.03],
    )
    durations = np.where(
        types == "Movie",
        np.random.randint(60, 180, n),
        np.random.randint(1, 10, n),
    )
    countries = np.random.choice(
        ["United States", "India", "United Kingdom", "Canada", "Japan"],
        n, p=[0.45, 0.20, 0.15, 0.10, 0.10],
    )
    genres = np.random.choice(
        ["Dramas", "Comedies", "Documentaries", "Action & Adventure",
         "Thrillers", "Horror Movies", "International TV Shows"],
        n,
    )
    # Inject ~10 % missing values in key columns
    mask = np.random.random(n) < 0.10
    df = pd.DataFrame({
        "type": types, "release_year": years, "rating": ratings,
        "duration": [f"{d} min" if t == "Movie" else f"{d} Seasons"
                     for d, t in zip(durations, types)],
        "country": np.where(mask, None, countries).astype(object),
        "listed_in": genres,
        "director": np.where(np.random.random(n) < 0.20, None, "Some Director").astype(object),
        "cast":     np.where(np.random.random(n) < 0.05, None, "Some Cast").astype(object),
    })
    print("✅ Synthetic dataset created.")

print(f"\n📐 Shape  : {df.shape[0]} rows × {df.shape[1]} columns")
print(f"\n📋 Columns:\n{list(df.columns)}")
print(f"\n🔎 First 5 rows:\n{df.head()}")
print(f"\n🗂️  Data Types:\n{df.dtypes}")

# ============================================================
# SECTION 2 ── CLEAN MISSING VALUES & OUTLIERS
# ============================================================
print("\n" + "=" * 60)
print("  SECTION 2: CLEAN MISSING VALUES & OUTLIERS")
print("=" * 60)

# --- 2a. Missing values ---
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_df = pd.DataFrame({"Missing Count": missing, "Missing %": missing_pct})
missing_df = missing_df[missing_df["Missing Count"] > 0].sort_values("Missing %", ascending=False)
print(f"\n🔍 Missing Values:\n{missing_df}")

# Visualise missing values
fig, ax = plt.subplots()
missing_df["Missing %"].plot(kind="bar", color="#E50914", ax=ax)
ax.set_title("Missing Values per Column (%)")
ax.set_ylabel("Missing %")
ax.set_xlabel("Column")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("plot_01_missing_values.png", dpi=150)
plt.show()
plt.close()
print("📊 Saved → plot_01_missing_values.png")

# --- 2b. Handle missing values ---
for col in ["director", "cast", "country", "rating", "date_added"]:
    if col in df.columns:
        df[col] = df[col].fillna("Unknown")

print("\n✅ Missing values filled with 'Unknown'.")
print(f"   Remaining nulls: {df.isnull().sum().sum()}")

# --- 2c. Extract numeric duration ---
if "duration" in df.columns:
    movies = df[df["type"] == "Movie"].copy()
    movies["duration_mins"] = (
        movies["duration"].str.extract(r"(\d+)").astype(float)
    )

    # Outlier detection using IQR
    Q1, Q3 = movies["duration_mins"].quantile([0.25, 0.75])
    IQR = Q3 - Q1
    lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    outliers = movies[(movies["duration_mins"] < lower) | (movies["duration_mins"] > upper)]
    print(f"\n📌 Movie duration outliers: {len(outliers)} rows "
          f"(outside [{lower:.0f}, {upper:.0f}] mins)")

    fig, axes = plt.subplots(1, 2)
    movies["duration_mins"].plot(kind="box", ax=axes[0], color="#E50914")
    axes[0].set_title("Before Outlier Removal")
    movies_clean = movies[
        (movies["duration_mins"] >= lower) & (movies["duration_mins"] <= upper)
    ]
    movies_clean["duration_mins"].plot(kind="box", ax=axes[1], color="#221F1F")
    axes[1].set_title("After Outlier Removal")
    plt.suptitle("Movie Duration (mins) – Outlier Treatment")
    plt.tight_layout()
    plt.savefig("plot_02_outliers.png", dpi=150)
    plt.close()
    print("📊 Saved → plot_02_outliers.png")

# ============================================================
# SECTION 3 ── SUMMARY STATISTICS
# ============================================================
print("\n" + "=" * 60)
print("  SECTION 3: SUMMARY STATISTICS")
print("=" * 60)

print("\n📊 Numerical summary:")
print(df.describe(include="all").T.to_string())

if "duration" in df.columns and "movies_clean" in dir():
    print(f"\n🎬 Movie Duration Stats (mins):")
    print(movies_clean["duration_mins"].describe().round(2))

print(f"\n📺 Content Type distribution:")
print(df["type"].value_counts())

if "release_year" in df.columns:
    print(f"\n📅 Release Year range: {df['release_year'].min()} – {df['release_year'].max()}")

# ============================================================
# SECTION 4 ── UNIVARIATE ANALYSIS & CHARTS
# ============================================================
print("\n" + "=" * 60)
print("  SECTION 4: UNIVARIATE ANALYSIS & CHARTS")
print("=" * 60)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Univariate Analysis – Netflix Titles", fontsize=16, fontweight="bold")

# 4a. Content type (Movies vs TV Shows)
type_counts = df["type"].value_counts()
axes[0, 0].pie(
    type_counts, labels=type_counts.index,
    autopct="%1.1f%%", colors=["#E50914", "#221F1F"],
    startangle=140, wedgeprops={"edgecolor": "white"},
)
axes[0, 0].set_title("Movies vs TV Shows")

# 4b. Top 10 Ratings
rating_counts = df["rating"].value_counts().head(10)
rating_counts.plot(kind="bar", ax=axes[0, 1], color="#E50914", edgecolor="white")
axes[0, 1].set_title("Top 10 Content Ratings")
axes[0, 1].set_xlabel("Rating")
axes[0, 1].set_ylabel("Count")
axes[0, 1].tick_params(axis="x", rotation=45)

# 4c. Content added by release year
if "release_year" in df.columns:
    df["release_year"].value_counts().sort_index().plot(
        kind="line", ax=axes[1, 0], color="#E50914", linewidth=2
    )
    axes[1, 0].set_title("Titles Added by Release Year")
    axes[1, 0].set_xlabel("Year")
    axes[1, 0].set_ylabel("Count")

# 4d. Movie duration histogram
if "movies_clean" in dir():
    axes[1, 1].hist(
        movies_clean["duration_mins"], bins=30, color="#E50914",
        edgecolor="white", alpha=0.85,
    )
    axes[1, 1].axvline(movies_clean["duration_mins"].mean(), color="black",
                       linestyle="--", linewidth=1.5, label="Mean")
    axes[1, 1].axvline(movies_clean["duration_mins"].median(), color="grey",
                       linestyle=":", linewidth=1.5, label="Median")
    axes[1, 1].set_title("Movie Duration Distribution")
    axes[1, 1].set_xlabel("Duration (mins)")
    axes[1, 1].legend()

plt.tight_layout()
plt.savefig("plot_03_univariate.png", dpi=150)
plt.show()
plt.close()
print("📊 Saved → plot_03_univariate.png")

# ============================================================
# SECTION 5 ── BIVARIATE ANALYSIS & RELATIONSHIPS
# ============================================================
print("\n" + "=" * 60)
print("  SECTION 5: BIVARIATE ANALYSIS & RELATIONSHIPS")
print("=" * 60)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Bivariate Analysis – Netflix Titles", fontsize=15, fontweight="bold")

# 5a. Content type vs Rating (stacked bar)
if "rating" in df.columns:
    top_ratings = df["rating"].value_counts().head(6).index
    cross = (
        df[df["rating"].isin(top_ratings)]
        .groupby(["rating", "type"])
        .size()
        .unstack(fill_value=0)
    )
    cross.plot(kind="bar", stacked=True, ax=axes[0],
               color=["#E50914", "#221F1F"], edgecolor="white")
    axes[0].set_title("Rating vs Content Type")
    axes[0].set_xlabel("Rating")
    axes[0].set_ylabel("Count")
    axes[0].tick_params(axis="x", rotation=45)
    axes[0].legend(title="Type")

# 5b. Release year vs Count by type
if "release_year" in df.columns:
    pivot = (
        df[df["release_year"] >= 2000]
        .groupby(["release_year", "type"])
        .size()
        .unstack(fill_value=0)
    )
    pivot.plot(kind="line", ax=axes[1], color=["#E50914", "#221F1F"], linewidth=2)
    axes[1].set_title("Movies vs TV Shows Over the Years")
    axes[1].set_xlabel("Release Year")
    axes[1].set_ylabel("Count")
    axes[1].legend(title="Type")

plt.tight_layout()
plt.savefig("plot_04_bivariate.png", dpi=150)
plt.show()
plt.close()
print("📊 Saved → plot_04_bivariate.png")

# Correlation (numeric columns only)
num_cols = df.select_dtypes(include="number").columns.tolist()
if len(num_cols) >= 2:
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(df[num_cols].corr(), annot=True, fmt=".2f",
                cmap="Reds", ax=ax, linewidths=0.5)
    ax.set_title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig("plot_05_correlation.png", dpi=150)
    plt.close()
    print("📊 Saved → plot_05_correlation.png")

# ============================================================
# SECTION 6 ── HYPOTHESIS TESTING & p-VALUES
# ============================================================
print("\n" + "=" * 60)
print("  SECTION 6: HYPOTHESIS TESTING & p-VALUES")
print("=" * 60)

if "movies_clean" in dir():
    # ── Test 1: Are movies from the 2010s longer than those from the 2000s? ──
    pre_2010  = movies_clean[movies_clean["release_year"] < 2010]["duration_mins"].dropna()
    post_2010 = movies_clean[movies_clean["release_year"] >= 2010]["duration_mins"].dropna()

    t_stat, p_val = stats.ttest_ind(pre_2010, post_2010, equal_var=False)
    print("\n📌 Test 1 – Are 2010s movies longer than 2000s movies?")
    print(f"   H0: Mean duration (pre-2010) == Mean duration (post-2010)")
    print(f"   H1: Mean duration differs between the two groups")
    print(f"   Mean pre-2010  : {pre_2010.mean():.2f} mins (n={len(pre_2010)})")
    print(f"   Mean post-2010 : {post_2010.mean():.2f} mins (n={len(post_2010)})")
    print(f"   t-statistic    : {t_stat:.4f}")
    print(f"   p-value        : {p_val:.4f}")
    if p_val < 0.05:
        print("   ✅ Result: Reject H0 — significant difference in duration.")
    else:
        print("   ❌ Result: Fail to reject H0 — no significant difference.")

    # ── Test 2: Are Movies & TV Shows equally distributed across ratings? ──
    if "rating" in df.columns:
        top_r = df["rating"].value_counts().head(5).index
        contingency = pd.crosstab(
            df[df["rating"].isin(top_r)]["type"],
            df[df["rating"].isin(top_r)]["rating"],
        )
        chi2, p_chi, dof, expected = stats.chi2_contingency(contingency)
        print("\n📌 Test 2 – Are content types distributed evenly across ratings?")
        print(f"   H0: Content type and rating are independent")
        print(f"   H1: Content type and rating are NOT independent")
        print(f"   Chi-Square statistic : {chi2:.4f}")
        print(f"   p-value              : {p_chi:.4f}")
        print(f"   Degrees of freedom   : {dof}")
        if p_chi < 0.05:
            print("   ✅ Result: Reject H0 — type and rating are dependent.")
        else:
            print("   ❌ Result: Fail to reject H0 — type and rating are independent.")

    # ── Plot: Duration by era ──
    fig, ax = plt.subplots()
    ax.hist(pre_2010, bins=25, alpha=0.7, color="#E50914", label="Pre-2010")
    ax.hist(post_2010, bins=25, alpha=0.7, color="#221F1F", label="Post-2010")
    ax.axvline(pre_2010.mean(), color="red", linestyle="--", linewidth=1.5)
    ax.axvline(post_2010.mean(), color="black", linestyle="--", linewidth=1.5)
    ax.set_title("Movie Duration: Pre-2010 vs Post-2010 (Hypothesis Test 1)")
    ax.set_xlabel("Duration (mins)")
    ax.set_ylabel("Frequency")
    ax.legend()
    plt.tight_layout()
    plt.savefig("plot_06_hypothesis.png", dpi=150)
    plt.close()
    print("\n📊 Saved → plot_06_hypothesis.png")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("  ✅ EDA COMPLETE — GENERATED FILES")
print("=" * 60)
charts = [
    "plot_01_missing_values.png  → Missing value bar chart",
    "plot_02_outliers.png        → Outlier box plots (before/after)",
    "plot_03_univariate.png      → 4-panel univariate charts",
    "plot_04_bivariate.png       → Bivariate relationship charts",
    "plot_05_correlation.png     → Correlation heatmap (if applicable)",
    "plot_06_hypothesis.png      → Hypothesis test distribution",
]
for c in charts:
    print(f"   📈 {c}")