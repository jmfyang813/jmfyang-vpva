import requests
from datetime import datetime
import pytz
import time
import json

# ------------------------------
# CONFIG
# ------------------------------
posts = {
    "DIGITAL SERIES OF THE YEAR": {
        "GHOSTING": "ZmVlZGJhY2s6MTI5NzU5MjkzOTA2MDc5OA",
        "LOVE AT FIRST SPIKE": "ZmVlZGJhY2s6MTI5NzU5NTU3OTA2MDUzNA",
        "GOLDEN SCENERY OF TOMORROW": "ZmVlZGJhY2s6MTI5NzU5NjkzNTcyNzA2NQ",
        "HOW TO SPOT A RED FLAG": "ZmVlZGJhY2s6MTI5NzU5MTIzNTcyNzYzNQ",
        "BAD GENIUS": "ZmVlZGJhY2s6MTI5NzU4ODc1MjM5NDU1MA",
        "ALIBI": "ZmVlZGJhY2s6MTI5NzU5ODY4NTcyNjg5MA",
    },
    "FANDOM OF THE YEAR": {
        "JMFYANG": "ZmVlZGJhY2s6MTIyNzg3NDA5MjgxODU3MA",
        "DUSTBIA": "ZmVlZGJhY2s6MTIyNzg3MDgyMjgxODg5Nw",
        "CAPEATH": "ZmVlZGJhY2s6MTIyNzg0NjY1OTQ4Nzk4MA",
        "WILLCA": "ZmVlZGJhY2s6MTIyNzg0Mjg0OTQ4ODM2MQ",
        "KIMPAU": "ZmVlZGJhY2s6MTIyNzgzOTUzNjE1NTM1OQ",
        "ASHDRES": "ZmVlZGJhY2s6MTIyNzgzNjE3NjE1NTY5NQ",
    },
    "LOVETEAM OF THE YEAR": {
        "JMFYANG": "ZmVlZGJhY2s6MTIyNzc4MTIzNjE2MTE4OQ",
        "RABGEL": "ZmVlZGJhY2s6MTIyNzc5MDMyMjgyNjk0Nw",
        "DUSTBIA": "ZmVlZGJhY2s6MTIyNzc4Nzc3NjE2MDUzNQ",
        "ASHDRES": "ZmVlZGJhY2s6MTIyNzc4NTY3OTQ5NDA3OA",
        "KIMPAU": "ZmVlZGJhY2s6MTIyNzc4Mjg4OTQ5NDM1Nw",
        "WILLCA": "ZmVlZGJhY2s6MTIyNzc3OTQyOTQ5NDcwMw",
    },
    "MUSIC VIDEO OF THE YEAR": {
        "WHEREVER YOU ARE": "ZmVlZGJhY2s6OTE1MDA3OTQxMjM5MzY3",
        "MINAMAHAL": "ZmVlZGJhY2s6OTE1MDA1MjQ0NTcyOTcw",
        "HANGGANG DITO NA LANG BA TAYO?": "ZmVlZGJhY2s6OTE1MDAyMTkxMjM5OTQy",
        "WHAT IF TAYO?": "ZmVlZGJhY2s6OTE0OTk4NjcxMjQwMjk0",
        "NAIILANG": "ZmVlZGJhY2s6OTE0OTk1NzUxMjQwNTg2",
        "AYA": "ZmVlZGJhY2s6OTE0OTkyNzE0NTc0MjIz",
    },
}

fb_dtsg = "NAftSGxIH9AA8B7cF4KEPlkV91fVtVk8BBF6PCwammW74JUDqwbQUFw:16:1756974490"
lsd = "Uq25aBYrQLNcHbwzY-RgZy"
jazoest = "25363"

headers = {
    "accept": "*/*",
    "content-type": "application/x-www-form-urlencoded",
    "x-asbd-id": "359341",
    "x-fb-lsd": lsd
}

graphql_url = "https://www.facebook.com/api/graphql/"
PH_TZ = pytz.timezone("Asia/Manila")

# ------------------------------
# HELPER FUNCTIONS
# ------------------------------
def fetch_graphql(doc_id, variables, friendly_name):
    """Sends a GraphQL POST request and returns JSON response."""
    data = {
        "fb_dtsg": fb_dtsg,
        "jazoest": jazoest,
        "fb_api_caller_class": "RelayModern",
        "fb_api_req_friendly_name": friendly_name,
        "variables": str(variables).replace("'", '"'),
        "doc_id": doc_id,
        "server_timestamps": "true"
    }
    try:
        response = requests.post(graphql_url, headers=headers, data=data, cookies={})
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching {friendly_name}: {e}")
        return {}

def generate_html_report(all_categories_data):
    """Generate HTML report from ranking data."""
    current_time = datetime.now(PH_TZ).strftime("%Y-%m-%d %H:%M:%S")
    
    html = """<html>
<head>
    <title>Facebook Post Rankings</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            padding: 20px;
        }
        h1 {
            color: #333;
        }
        h2 {
            color: #555;
            margin-top: 30px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        th, td {
            padding: 10px;
            text-align: left;
            border: 1px solid #ddd;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .timestamp {
            color: #666;
            font-size: 14px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <h1>Facebook Post Rankings</h1>
    <p class="timestamp">Data generated at {current_time}</p>
"""
    
    for category, post_data in all_categories_data.items():
        html += f"    <h2>{category}</h2>\n"
        html += """        <table>
            <tr>
                <th>Rank</th>
                <th>Post Name</th>
                <th>Reactions</th>
                <th>Shares</th>
                <th>Total (Reactions + Shares)</th>
            </tr>
"""
        
        for rank, (post_name, reactions, shares, total) in enumerate(post_data, 1):
            html += f"            <tr>\n                <td>{rank}</td>\n                <td>{post_name}</td>\n                <td>{reactions}</td>\n                <td>{shares}</td>\n                <td>{total}</td>\n            </tr>\n"
        
        html += "        </table>\n"
    
    html += """    </body>
</html>"""
    
    return html.format(current_time=current_time)

# ------------------------------
# MAIN EXECUTION
# ------------------------------
def fetch_and_generate():
    """Fetch all post data and generate HTML report."""
    all_categories_data = {}
    
    for category, posts_dict in posts.items():
        print(f"\n📊 Fetching {category}...")
        
        post_data = []
        
        for post_name, post_id in posts_dict.items():
            # Fetch reactions
            reactions_data = fetch_graphql(
                "24051433444544934",
                {"feedbackTargetID": post_id, "scale": 1},
                "CometUFIReactionsDialogQuery"
            )
            reaction_count = 0
            try:
                reactions_summary = reactions_data.get("data", {}).get("node", {}).get("top_reactions", {}).get("summary", [])
                reaction_count = next(
                    (r['reaction_count'] for r in reactions_summary 
                     if r['reaction']['id'] == '613557422527858'), 0
                )
            except:
                pass
            
            # Fetch shares
            shares_data = fetch_graphql(
                "9843821265734688",
                {"feedbackTargetID": post_id},
                "CometUFISharesCountTooltipContentQuery"
            )
            total_shares = 0
            try:
                total_shares = shares_data.get("data", {}).get("feedback", {}).get("reshares", {}).get("count", 0)
            except:
                pass
            
            total = reaction_count + total_shares
            post_data.append((post_name, reaction_count, total_shares, total))
            print(f"  ✓ {post_name}: {reaction_count} reactions, {total_shares} shares")
            time.sleep(1)  # Rate limiting
        
        # Sort by total descending
        sorted_posts = sorted(post_data, key=lambda x: x[3], reverse=True)
        all_categories_data[category] = sorted_posts
    
    # Generate and save HTML
    html_content = generate_html_report(all_categories_data)
    with open("ranking_data.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("\n✅ HTML report generated: ranking_data.html")

if __name__ == "__main__":
    fetch_and_generate()