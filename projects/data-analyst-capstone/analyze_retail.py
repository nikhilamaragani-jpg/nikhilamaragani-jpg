from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

DATA_DIR.mkdir(exist_ok=True, parents=True)
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

rng = np.random.default_rng(42)

regions = ["North", "South", "East", "West", "Central"]
channels = ["Online", "Retail", "Marketplace"]
categories = ["Electronics", "Home", "Fashion", "Beauty", "Sports"]
segments = ["New", "Regular", "VIP"]

category_base_price = {
    "Electronics": 140,
    "Home": 75,
    "Fashion": 55,
    "Beauty": 48,
    "Sports": 68,
}

category_margin = {
    "Electronics": 0.22,
    "Home": 0.27,
    "Fashion": 0.32,
    "Beauty": 0.29,
    "Sports": 0.25,
}

records = []
for order_id in range(1, 1601):
    order_date = pd.Timestamp("2024-01-01") + pd.Timedelta(days=rng.integers(0, 365))
    region = rng.choice(regions)
    channel = rng.choice(channels)
    category = rng.choice(categories)
    customer_segment = rng.choice(segments, p=[0.45, 0.40, 0.15])

    quantity = int(rng.integers(1, 8))
    price = category_base_price[category] * rng.uniform(0.8, 1.5)
    discount = rng.uniform(0.05, 0.28) if channel == "Online" else rng.uniform(0.02, 0.18)
    revenue = round(quantity * price * (1 - discount), 2)
    profit_margin = category_margin[category] + (0.04 if customer_segment == "VIP" else 0)
    profit = round(revenue * profit_margin, 2)

    order_status = rng.choice(["Completed", "Returned"], p=[0.92, 0.08])
    region_factor = {"North": 1.15, "South": 0.96, "East": 0.88, "West": 1.2, "Central": 1.03}[region]
    channel_factor = {"Online": 1.2, "Retail": 0.95, "Marketplace": 1.1}[channel]
    demand_factor = 1 + (rng.random() * 0.35)
    revenue = round(revenue * region_factor * channel_factor * demand_factor, 2)
    profit = round(revenue * (profit_margin + 0.03 if channel == "Online" else profit_margin), 2)

    records.append(
        {
            "order_id": f"ORD-{order_id:05d}",
            "order_date": order_date,
            "customer_id": f"CUST-{rng.integers(1, 500):04d}",
            "region": region,
            "sales_channel": channel,
            "category": category,
            "customer_segment": customer_segment,
            "quantity": quantity,
            "unit_price": round(price, 2),
            "discount_pct": round(discount, 4),
            "revenue": revenue,
            "profit": profit,
            "order_status": order_status,
        }
    )

sales_df = pd.DataFrame(records)
sales_df["month"] = sales_df["order_date"].dt.to_period("M").astype(str)

sales_df.to_csv(DATA_DIR / "retail_sales_data.csv", index=False)

monthly_summary = (
    sales_df.groupby("month")
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique"),
    )
    .reset_index()
)
monthly_summary["month"] = pd.to_datetime(monthly_summary["month"])

region_summary = (
    sales_df.groupby("region")
    .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), orders=("order_id", "nunique"))
    .reset_index()
)

category_summary = (
    sales_df.groupby("category")
    .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), quantity=("quantity", "sum"))
    .reset_index()
)

channel_summary = (
    sales_df.groupby("sales_channel")
    .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), orders=("order_id", "nunique"))
    .reset_index()
)

monthly_summary.to_csv(OUTPUT_DIR / "monthly_summary.csv", index=False)
region_summary.to_csv(OUTPUT_DIR / "region_summary.csv", index=False)
category_summary.to_csv(OUTPUT_DIR / "category_summary.csv", index=False)
channel_summary.to_csv(OUTPUT_DIR / "channel_summary.csv", index=False)

kpis = {
    "Total Revenue": round(sales_df["revenue"].sum(), 2),
    "Total Profit": round(sales_df["profit"].sum(), 2),
    "Average Order Value": round(sales_df["revenue"].mean(), 2),
    "Total Orders": sales_df["order_id"].nunique(),
    "Profit Margin": round((sales_df["profit"].sum() / sales_df["revenue"].sum()) * 100, 2),
    "Returned Orders Rate": round((sales_df[sales_df["order_status"] == "Returned"].shape[0] / sales_df.shape[0]) * 100, 2),
}

summary_df = pd.DataFrame({"Metric": list(kpis.keys()), "Value": list(kpis.values())})
summary_df.to_csv(OUTPUT_DIR / "summary_metrics.csv", index=False)

sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

sns.lineplot(data=monthly_summary, x="month", y="revenue", ax=axes[0, 0], marker="o", color="#2563eb")
axes[0, 0].set_title("Monthly Revenue Trend")
axes[0, 0].set_xlabel("Month")
axes[0, 0].set_ylabel("Revenue")

sns.barplot(data=region_summary.sort_values("revenue", ascending=False), x="region", y="revenue", ax=axes[0, 1], palette="viridis")
axes[0, 1].set_title("Revenue by Region")
axes[0, 1].set_xlabel("Region")
axes[0, 1].set_ylabel("Revenue")

sns.barplot(data=category_summary.sort_values("revenue", ascending=False), x="category", y="revenue", ax=axes[1, 0], palette="magma")
axes[1, 0].set_title("Revenue by Category")
axes[1, 0].set_xlabel("Category")
axes[1, 0].set_ylabel("Revenue")

sns.barplot(data=channel_summary.sort_values("revenue", ascending=False), x="sales_channel", y="revenue", ax=axes[1, 1], palette="Set2")
axes[1, 1].set_title("Revenue by Sales Channel")
axes[1, 1].set_xlabel("Channel")
axes[1, 1].set_ylabel("Revenue")

plt.tight_layout()
fig.savefig(OUTPUT_DIR / "data_analyst_dashboard.png", dpi=300, bbox_inches="tight")
plt.close(fig)

best_region = region_summary.sort_values("revenue", ascending=False).iloc[0]
best_category = category_summary.sort_values("revenue", ascending=False).iloc[0]
best_channel = channel_summary.sort_values("revenue", ascending=False).iloc[0]

insights = [
    "# Retail Performance & Customer Insights",
    "",
    "## Executive summary",
    f"- Total revenue generated: ${kpis['Total Revenue']:,.2f}",
    f"- Total profit generated: ${kpis['Total Profit']:,.2f}",
    f"- Average order value: ${kpis['Average Order Value']:,.2f}",
    f"- Profit margin: {kpis['Profit Margin']:.2f}%",
    f"- Returned orders rate: {kpis['Returned Orders Rate']:.2f}%",
    "",
    "## Key findings",
    f"- The strongest revenue region is {best_region['region']} with ${best_region['revenue']:,.2f} in sales.",
    f"- The top-selling category is {best_category['category']} with ${best_category['revenue']:,.2f} in revenue.",
    f"- The highest-performing channel is {best_channel['sales_channel']} with ${best_channel['revenue']:,.2f} in revenue.",
    "- Online and marketplace channels produce higher transaction velocity and stronger conversion potential.",
    "- The business has room to improve retention, profitability in lower-performing areas, and discount strategy for slower categories.",
    "",
    "## Recommendations",
    "1. Increase retention campaigns targeted at repeat customers in the South and East regions.",
    "2. Push premium product bundles in the Electronics and Home categories to raise profit margins.",
    "3. Improve inventory allocation in the West and North regions to match demand concentration.",
    "4. Rebalance discounts so promotions drive conversion without eroding margin in low-volume categories.",
    "5. Build a recurring Power BI dashboard to share results with sales, marketing, and leadership teams.",
]

(OUTPUT_DIR / "insights_summary.md").write_text("\n".join(insights), encoding="utf-8")

print("Dataset created at:", DATA_DIR / "retail_sales_data.csv")
print("Dashboard saved at:", OUTPUT_DIR / "data_analyst_dashboard.png")
print("Summary saved at:", OUTPUT_DIR / "insights_summary.md")
print("Total revenue:", f"${kpis['Total Revenue']:,.2f}")
