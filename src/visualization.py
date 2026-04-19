import matplotlib.pyplot as plt


# ---------------- COMMON STYLE ---------------- #
def style_ax(ax, title, xlabel="", ylabel=""):
    ax.set_title(title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    ax.grid(alpha=0.2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


# ---------------- 1. SUPPLIER SCORES ---------------- #
def plot_scores(supplier_stats):
    if supplier_stats.empty:
        return plt.figure()

    data = supplier_stats.sort_values(by='score', ascending=False).head(20)

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.bar(
        data['supplier_id'].astype(str),
        data['score']
    )

    style_ax(ax, "Top 20 Supplier Scores", "Supplier ID", "Score")
    ax.tick_params(axis='x', rotation=45)

    return fig


# ---------------- 2. DELAY DISTRIBUTION ---------------- #
def plot_delay_distribution(supplier_stats):
    if supplier_stats.empty:
        return plt.figure()

    fig, ax = plt.subplots()

    ax.hist(supplier_stats['avg_delay'], bins=10)

    style_ax(ax, "Delay Distribution", "Average Delay", "Frequency")

    return fig


# ---------------- 3. TOP SUPPLIERS ---------------- #
def plot_top_suppliers(supplier_stats):
    if supplier_stats.empty:
        return plt.figure()

    top = supplier_stats.sort_values(by='score', ascending=False).head(10)

    fig, ax = plt.subplots()

    ax.barh(
        top['supplier_id'].astype(str),
        top['score']
    )

    ax.invert_yaxis()

    style_ax(ax, "Top 10 Suppliers", "Score", "Supplier ID")

    return fig


# ---------------- 4. RISK DISTRIBUTION ---------------- #
def plot_risk_distribution(supplier_stats):
    if supplier_stats.empty:
        return plt.figure()

    fig, ax = plt.subplots()

    risk_counts = supplier_stats['risk'].value_counts()

    ax.bar(
        risk_counts.index,
        risk_counts.values
    )

    style_ax(ax, "Risk Distribution", "Risk Level", "Number of Suppliers")

    return fig


# ---------------- 5. COST VS DELAY ---------------- #
def plot_cost_vs_delay(supplier_stats):
    if supplier_stats.empty:
        return plt.figure()

    fig, ax = plt.subplots()

    ax.scatter(
        supplier_stats['avg_cost'],
        supplier_stats['avg_delay'],
        alpha=0.7
    )

    style_ax(ax, "Cost vs Delay", "Average Cost", "Average Delay")

    return fig