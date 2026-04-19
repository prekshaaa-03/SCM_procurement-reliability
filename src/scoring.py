def compute_score(supplier_stats, suppliers):
    # ---------------- MERGE RATINGS ---------------- #
    supplier_stats = supplier_stats.merge(
        suppliers[['supplier_id', 'rating']],
        on='supplier_id',
        how='left'
    )

    # ---------------- HANDLE MISSING VALUES ---------------- #
    supplier_stats['rating'] = supplier_stats['rating'].fillna(0)
    supplier_stats['avg_cost'] = supplier_stats['avg_cost'].fillna(0)
    supplier_stats['avg_delay'] = supplier_stats['avg_delay'].fillna(0)

    # Avoid division issues
    supplier_stats['avg_cost'] = supplier_stats['avg_cost'].replace(0, 1)

    # ---------------- NORMALIZATION ---------------- #
    supplier_stats['norm_cost'] = 1 / (1 + supplier_stats['avg_cost'])
    supplier_stats['norm_delay'] = 1 / (1 + supplier_stats['avg_delay'])

    # ---------------- FINAL SCORE ---------------- #
    supplier_stats['score'] = (
        0.4 * supplier_stats['on_time_rate'] +
        0.2 * supplier_stats['norm_delay'] +
        0.2 * supplier_stats['norm_cost'] +
        0.2 * (supplier_stats['rating'] / 5)
    )

    return supplier_stats


def classify_risk(supplier_stats):

    def classify(delay):
        if delay is None:
            return "⚪ Unknown"

        if delay <= 2:
            return "🟢 Low Risk"
        elif delay <= 5:
            return "🟡 Medium Risk"
        else:
            return "🔴 High Risk"

    supplier_stats['risk'] = supplier_stats['avg_delay'].apply(classify)

    return supplier_stats