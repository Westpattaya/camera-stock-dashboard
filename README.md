# 📷 Camera Stock Dashboard

A simple inventory dashboard for tracking camera sales, stock levels, and restocks.  
No installation needed — just open the HTML file in your browser.

---

## How to use

### Quick start (easiest)

1. Download `camera_dashboard_v3.html`
2. Double-click to open it in your browser
3. Click **"↑ Update data"** and select your `Update log.csv`
4. Done — the dashboard will show your data

### With restock history

If you have a `restock_log.csv` file too, drag and drop it onto the upload area, or load it via the button.

---

## Files

| File | What it is |
|---|---|
| `camera_dashboard_v3.html` | The dashboard — this is all you need |
| `Update log.csv` | Order data (sales log) |
| `restock_log.csv` | Restock history |
| `start.sh` | (Mac only) Auto-starts a local server and loads both CSVs automatically |

---

## CSV format

Your `Update log.csv` must have these columns:

```
Order_ID, date_time, total_count_product_a, total_count_product_b, total_count_product_c, total_items
```

Example:
```
1, 23/4/2026 09:15, 1, 0, 0, 1
2, 23/4/2026 09:35, 0, 1, 1, 2
```

Date format can be `DD/MM/YYYY HH:MM` or `MM/DD/YYYY H:MM` — both work.

---

## Features

- **KPIs** — Total orders, revenue, items sold, restocks, stock alerts
- **Sales chart** — Daily sales per product over time
- **Revenue share** — Donut chart by product
- **Live inventory** — Current stock = Initial + Restocked − Sold
- **Restock log** — Add, edit, delete restock events
- **Order heatmap** — Busiest hours of the day
- **Filters** — By date range and product
- **Export** — Download filtered orders as CSV

---

## Product settings

Click the **⚙️** icon in the inventory table to change:
- Product names
- Prices (฿)
- Starting stock
- Low stock alert threshold

Settings are saved in your browser automatically.

---

## Sharing restock data

After logging restocks, click **"↓ Save restock log"** to download `restock_log.csv`.  
Share this file alongside the HTML so others have the same restock history.

---

## Mac: Auto-load with local server

If you're on Mac and want the CSVs to load automatically (no manual upload):

```bash
bash start.sh
```

Then open `http://localhost:8080/camera_dashboard_v3.html`

> Requires Python 3 — comes pre-installed on most Macs.
