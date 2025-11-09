import os, re, json, subprocess
from flask import Flask, render_template, request, jsonify


app = Flask(__name__, template_folder='.', static_folder="../static")

RECIPES_DIR = "/app/recipes_json"
IMAGES_DIR = "/app/static/images"

TEMPLATE = "webui.html"

def get_next_prefix():
    if not os.path.exists(RECIPES_DIR):
        return "000"
    nums = []
    for f in os.listdir(RECIPES_DIR):
        m = re.match(r"(\d{3})_.*\.json$", f)
        if m:
            nums.append(int(m.group(1)))
    return f"{max(nums)+1:03d}" if nums else "000"

@app.route("/")
def index():
    return render_template(TEMPLATE, next_prefix=get_next_prefix())

@app.route("/generate", methods=["POST"])
def generate():
    data = request.form.to_dict()
    image_file = request.files.get("image")
    recipe_id = data["id"]

    # ensure folder exists
    os.makedirs(RECIPES_DIR, exist_ok=True)

    # prefix collision check
    prefix = recipe_id.split("_")[0]
    existing_files = [
        f for f in os.listdir(RECIPES_DIR)
        if f.startswith(prefix + "_") and f.endswith(".json")
    ]
    if existing_files:
        return jsonify({
            "error": f"A recipe with prefix {prefix} already exists: {existing_files[0]}, refresh to gain a new ID."
        }), 400

    recipe = {
        "id": recipe_id,
        "name": data["name"],
        "tags": request.form.getlist("tags"),
        "prep_time": int(data.get("prep_time") or 0),
        "cook_time": int(data.get("cook_time") or 0),
        "ingredients": [
            {"qty": qty.strip(), "name": name.strip()}
            for line in data["ingredients"].splitlines() if "," in line
            for qty, name in [line.split(",", 1)]
        ],
        "instructions": [i.strip() for i in data["instructions"].splitlines() if i.strip()],
        "notes": [n.strip() for n in data["notes"].splitlines() if n.strip()],
        "image": f"../static/images/{recipe_id}.jpg" if image_file else ""
    }

    with open(os.path.join(RECIPES_DIR, f"{recipe_id}.json"), "w", encoding="utf-8") as f:
        json.dump(recipe, f, ensure_ascii=False, indent=2)

    if image_file:
        os.makedirs(IMAGES_DIR, exist_ok=True)
        image_path = os.path.join(IMAGES_DIR, f"{recipe_id}.jpg")
        image_file.save(image_path)

    return jsonify(recipe)

@app.route("/generate_html", methods=["POST"])
def generate_html():
    import subprocess
    result = subprocess.run(["python3.12", "recipe_json_to_html.py"], capture_output=True, text=True)
    return result.stdout or result.stderr

@app.route("/sync", methods=["POST"])
def sync_to_github():
    try:
        repo_dir = "/app" 
        commands = [
            ["git", "-C", repo_dir, "add", "."],
            ["git", "-C", repo_dir, "commit", "-m", "Auto-sync from admin panel"],
            ["git", "-C", repo_dir, "push", "origin", "master"]
        ]
        for cmd in commands:
            subprocess.run(cmd, check=True)
        return jsonify({"status": "success", "message": "Synced to GitHub"})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5469, debug=True)
    print("Recipes directory:", RECIPES_DIR)
    print("Next prefix:", get_next_prefix())
