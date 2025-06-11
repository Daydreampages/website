import os
import shutil
from bs4 import BeautifulSoup, Tag

# Paths
template_path = "main_template.html"
output_path = "merged-listings.html"
full_dir = "./full"
subpages_dir = "./subpages"

# Ensure subpages directory exists
os.makedirs(subpages_dir, exist_ok=True)

def get_category(filename):
    if "shower" in filename.lower():
        return "baby-shower-products"
    return "wedding-invite-products"

def transform_product_block(product_div, filename):
    title = product_div.find(class_="title")
    price = product_div.find(class_="price")
    img = product_div.find("img")
    nav_links = product_div.find("nav", class_="listing-navigation")

    cube = Tag(name="div", attrs={"class": "product-cube"})

    if img:
        img_tag = Tag(name="img", attrs={
            "class": "product-image",
            "src": img.get("src"),
            "alt": img.get("alt", "")
        })
        cube.append(img_tag)

    header = Tag(name="div", attrs={"class": "product-header"})

    if title:
        title_tag = Tag(name="h2", attrs={"class": "product-title"})
        title_tag.string = title.get_text(strip=True)
        header.append(title_tag)

    if price:
        price_tag = Tag(name="div", attrs={"class": "product-price"})
        price_tag.string = f"${price.get_text(strip=True)}"
        header.append(price_tag)

    cube.append(header)

    # Create "View Details" button
    details_link = Tag(name="a", attrs={
        "class": "view-details-button",
        "href": f"subpages/{filename}"
    })
    details_link.string = "View Details"
    cube.append(details_link)

    # --- Fix subpage content ---
    # Clone the original product div for subpage
    subpage_product = product_div
    sub_details_div = subpage_product.find("div", class_="description")

    # Fix version-switching links
    if nav_links:
        for a in nav_links.find_all("a"):
            href = a.get("href", "")
            if href.startswith("/"):
                # Convert to relative path if needed
                a["href"] = href.lstrip("/")

        # Add "Back to Home"
        back_link = Tag(name="a", attrs={"href": "../merged-listings.html", "class": "back-link"})
        back_link.string = "← Back to Home"
        nav_links.insert(0, back_link)

        # Put nav_links at end of description (if not already there)
        if sub_details_div:
            sub_details_div.append(nav_links)

    return cube

def main():
    with open(template_path, encoding="utf-8") as f:
        template_soup = BeautifulSoup(f, "html.parser")

    # Clear out both category containers
    for container_id in ["wedding-invite-products", "baby-shower-products"]:
        container = template_soup.find(id=container_id)
        if container:
            container.clear()

    for filename in os.listdir(full_dir):
        if filename.endswith(".html"):
            filepath = os.path.join(full_dir, filename)

            # Copy file to subpages
            shutil.copy(filepath, os.path.join(subpages_dir, filename))

            with open(filepath, encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")
                product = soup.find("div", class_="product")
                if product:
                    category_id = get_category(filename)
                    container = template_soup.find(id=category_id)
                    if container:
                        transformed = transform_product_block(product, filename)
                        container.append(transformed)
                    else:
                        print(f"⚠️ No container for category: {category_id}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(str(template_soup))

    print(f"✅ Merged listings saved to {output_path}")
    print(f"📁 Full listings copied to: {subpages_dir}")

if __name__ == "__main__":
    main()
