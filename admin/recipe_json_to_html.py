import json
from pathlib import Path

project_root = Path(__file__).parent.parent
input_folder = project_root / "recipes_json"
output_dir = project_root / "recipes_html"
static_dir = project_root / "static"
output_dir.mkdir(exist_ok=True)

template = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{name} - FOOD by Chris</title>
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
      rel="stylesheet"
    />
    <style>
      body {{
        background: url("../static/images/background_home.jpg") no-repeat center center fixed;
        background-size: cover;
      }}
    </style>
  </head>
  <body class="bg-dark text-white">
    <div class="container mt-4 bg-dark rounded-5 border border-3 p-4">
      <h1 class="display-3 fw-bold mb-3">{name}</h1>

      <img src="{image}" alt="{name}" class="img-fluid rounded mb-4 border border-2 mx-auto d-block" style="max-width:400px;"/>

      <div class="mb-3">{tags_html}</div>

      <p class="lead">
        <strong>🔪 Prep time:</strong> {prep_time} min &nbsp;|&nbsp;
        <strong>👨‍🍳 Cook time:</strong> {cook_time} min
      </p>
    </div>
    <div class="container mt-4 bg-dark rounded-5 border border-3 p-4">
      <h2 class="mt-4">Ingredients</h2>
        <div class="table-responsive mb-4">
        <table class="table table-dark table-striped table-bordered border-light align-middle">
            <thead>
            <tr>
                <th scope="col">#️⃣ Quantity</th>
                <th scope="col">🍅 Ingredient</th>
            </tr>
            </thead>
            <tbody>
            {ingredients}
            </tbody>
        </table>
        </div>
    </div>
    <div class="container mt-4 bg-dark rounded-5 border border-3 p-4">
      <h2>Instructions</h2>
      <ol class="list-group list-group-numbered mb-4">
        {instructions}
      </ol>
    </div>
    <div class="container mt-4 bg-dark rounded-5 border border-3 p-4">
      <h2>Notes</h2>
      <ul class="list-group list-group-flush mb-4">
        {notes}
      </ul>

      <a href="../menu.html" class="btn btn-outline-light mt-3">Back to Menu</a>
    </div>
  </body>
</html>
"""

# Collect recipe metadata for index
recipes_index = []

# Iterate over JSON files
for json_file in input_folder.glob("*.json"):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    r = data if isinstance(data, dict) else data[0]

    # Build HTML
    ingredients_html = "\n      ".join(
        f"<tr><td>{i['qty']}</td><td>{i['name']}</td></tr>" for i in r["ingredients"]
    )
    instructions_html = "\n        ".join(
        f"<li class='list-group-item bg-dark text-white'>{step}</li>" for step in r["instructions"]
    )
    notes_html = "\n        ".join(
        f"<li class='list-group-item bg-dark text-white'>{n}</li>" for n in r.get("notes", [])
    )

    tag_styles = {
    "gluten_free": ("Gluten Free", "bg-danger"),
    "dairy_free": ("Dairy Free", "bg-warning text-dark"),
    "nut_free": ("Nut Free", "bg-success"),
    "low_fructose": ("Low Fructose", "bg-info text-dark"),
    "vegan": ("Vegan", "bg-primary"),
    "vegetarian": ("Vegetarian", "bg-secondary"),
    }
    
    tags_html = ""
    if "tags" in r and r["tags"]:
      tags_html = (
          "<div class='d-flex flex-wrap gap-2 mb-3'>"
          + " ".join(
              f"<span class='badge {tag_styles.get(t, (t, 'bg-light text-dark'))[1]}'>{tag_styles.get(t, (t, t))[0]}</span>"
              for t in r["tags"]
          )
          + "</div>"
      )

    html_content = template.format(
        name=r["name"],
        image=r.get("image", ""),
        prep_time=r.get("prep_time", 0),
        cook_time=r.get("cook_time", 0),
        ingredients=ingredients_html,
        instructions=instructions_html,
        notes=notes_html,
        tags_html=tags_html,
    )

    # Write HTML file
    output_path = output_dir / f"{r['id']}.html"
    output_path.write_text(html_content, encoding="utf-8")

    # Add entry to recipes_index
    recipes_index.append({
        "id": r["id"],
        "prep_time": r["prep_time"],
        "cook_time": r["cook_time"],
        "name": r["name"],
        "tags": r.get("tags", []),
        "html": f"recipes_html/{r['id']}.html",
        "image": r.get("image", "")
    })

# Write recipes_index.json
index_path = project_root / "recipes_json/index/recipes_index.json"
with open(index_path, "w", encoding="utf-8") as f:
    json.dump(recipes_index, f, indent=2)

print(f"Generated HTML for {len(recipes_index)} recipes and created recipes_index.json.")
