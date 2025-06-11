import os
from bs4 import BeautifulSoup

# Paths
full_dir = "./full"
subpages_dir = "./subpages"

# Ensure subpages folder exists
os.makedirs(subpages_dir, exist_ok=True)

def add_navigation_buttons(soup, category_folder, base_filename):
    nav_div = soup.new_tag("nav", **{"class": "nav-buttons"})

    back_home = soup.new_tag("a", href="../merged-listings.html", **{"class": "btn"})
    back_home.string = "Back Home"
    nav_div.append(back_home)

    lite_href = f"../{category_folder}/lite/{base_filename}-lite.html"
    lite_btn = soup.new_tag("a", href=lite_href, **{"class": "btn"})
    lite_btn.string = "Lite"
    nav_div.append(lite_btn)

    gallery_href = f"../{category_folder}/gallery/{base_filename}-gallery.html"
    gallery_btn = soup.new_tag("a", href=gallery_href, **{"class": "btn"})
    gallery_btn.string = "Gallery"
    nav_div.append(gallery_btn)

    # If no <body> tag, create one and wrap the entire content inside
    if not soup.body:
        new_body = soup.new_tag("body")
        for element in list(soup.contents):
            new_body.append(element.extract())
        soup.append(new_body)

    # Insert nav at the top of the body
    soup.body.insert(0, nav_div)


def get_category_folder(filename):
    """Determine category folder by filename keywords."""
    if "shower" in filename.lower():
        return "baby_shower"
    return "invite_wedding"

def main():
    for filename in os.listdir(full_dir):
        if not filename.endswith(".html"):
            continue

        full_path = os.path.join(full_dir, filename)
        with open(full_path, encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        category_folder = get_category_folder(filename)
        base_filename = filename[:-5]  # Remove .html extension

        # Add navigation buttons
        add_navigation_buttons(soup, category_folder, base_filename)

        # Write modified HTML to subpages folder
        subpage_path = os.path.join(subpages_dir, filename)
        with open(subpage_path, "w", encoding="utf-8") as out_f:
            out_f.write(str(soup))

        print(f"Generated subpage: {subpage_path}")

if __name__ == "__main__":
    main()
