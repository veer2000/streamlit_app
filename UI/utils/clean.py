from bs4 import BeautifulSoup

def clean_html_for_quill(html):
    try:
        soup = BeautifulSoup(html, "html.parser")

        # Remove unwanted tags
        for tag in soup(["meta", "head", "script"]):
            tag.decompose()

        # Remove only problematic attributes, KEEP styling essentials
        allowed_styles = ["background-color", "font-weight", "text-decoration"]

        for tag in soup.find_all(True):
            if tag.has_attr("style"):
                styles = tag["style"].split(";")
                filtered_styles = []

                for style in styles:
                    if any(prop in style for prop in allowed_styles):
                        filtered_styles.append(style)

                if filtered_styles:
                    tag["style"] = ";".join(filtered_styles)
                else:
                    del tag["style"]

            # Remove classes (Outlook junk)
            if tag.has_attr("class"):
                del tag["class"]

        # Extract body only
        body = soup.find("body")
        return str(body) if body else str(soup)
    except Exception as e:
        raise e