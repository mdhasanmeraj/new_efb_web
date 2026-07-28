import os
import re

def optimize_images_in_templates():
    template_files = []
    for root, dirs, files in os.walk('.'):
        if 'node_modules' in root or '.git' in root or 'venv' in root or '.gemini' in root:
            continue
        for f in files:
            if f.endswith('.html'):
                template_files.append(os.path.join(root, f))

    img_tag_pattern = re.compile(r'<img\s+([^>]+)>', re.IGNORECASE)

    updated_files = 0
    for fpath in template_files:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        def process_img_tag(match):
            attrs = match.group(1)
            # Check if hero image (in hero section)
            is_hero = 'hero' in attrs.lower() or 'banner' in fpath.lower() or 'image1' in attrs.lower()
            
            new_attrs = attrs
            if 'loading=' not in attrs.lower():
                if not is_hero:
                    new_attrs += ' loading="lazy"'
                else:
                    new_attrs += ' loading="eager"'
            
            if 'decoding=' not in attrs.lower():
                new_attrs += ' decoding="async"'

            return f"<img {new_attrs}>"

        new_content = img_tag_pattern.sub(process_img_tag, content)

        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated_files += 1
            print(f"Updated <img> attributes in: {fpath}")

    print(f"Image optimization completed across {updated_files} template files.")

if __name__ == '__main__':
    optimize_images_in_templates()
