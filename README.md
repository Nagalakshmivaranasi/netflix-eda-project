# 📊 Netflix Titles — Exploratory Data Analysis (EDA)



## 📁 Project Structure

```
netflix_eda_project/
│
├── netflix_eda.py        ← Main EDA script (run this)
├── requirements.txt      ← All Python libraries needed
├── README.md             ← This file
└── outputs/              ← All charts saved here after running
```

---

## 🚀 How to Run in VS Code (Step by Step)

### Step 1 — Open the folder in VS Code
```
File → Open Folder → select "netflix_eda_project"
```

### Step 2 — Open the terminal in VS Code
```
Terminal → New Terminal   (or press Ctrl + ` )
```

### Step 3 — Install all required libraries
```bash
pip install -r requirements.txt
```

### Step 4 — Run the script
```bash
python netflix_eda.py
```

---

## 📈 Output Charts Generated

| File | Description |
|------|-------------|
| `plot_01_missing_values.png` | Bar chart of missing values per column |
| `plot_02_outliers.png`       | Box plots before & after outlier removal |
| `plot_03_univariate.png`     | 4-panel univariate analysis charts |
| `plot_04_bivariate.png`      | Bivariate relationship charts |
| `plot_05_correlation.png`    | Correlation heatmap (numeric columns) |
| `plot_06_hypothesis.png`     | Hypothesis test distribution plot |

All charts are saved in the **same folder** as the script.

---

## 📚 Topics Covered

1. **Load & Understand** — Shape, columns, data types, first look
2. **Clean Data** — Missing values, outlier detection using IQR
3. **Summary Statistics** — describe(), value counts, ranges
4. **Univariate Analysis** — Pie, bar, line, histogram charts
5. **Bivariate Analysis** — Stacked bar, line by type, heatmap
6. **Hypothesis Testing** — t-test & Chi-square with p-values

---

## 💡 Optional: Use Real Netflix Dataset

Download from Kaggle → [Netflix Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows)

Then replace line ~37 in `netflix_eda.py`:
```python
# Replace this:
df = pd.read_csv(url)

# With this:
df = pd.read_csv("netflix_titles.csv")
```
And place `netflix_titles.csv` in the same folder as the script.
