import os
import re

def remove_tailwind_cdn():
    template_files = []
    for root, dirs, files in os.walk('.'):
        if 'node_modules' in root or '.git' in root or 'venv' in root or '.gemini' in root:
            continue
        for f in files:
            if f.endswith('.html'):
                template_files.append(os.path.join(root, f))

    cdn_pattern = re.compile(r'<script\s+src=[\'"]https://cdn\.tailwindcss\.com[^\'"]*[\'"]\s*></script>', re.IGNORECASE)
    config_pattern = re.compile(r'<script\s+id=[\'"]tailwind-config[\'"]\s*>.*?</script>', re.DOTALL | re.IGNORECASE)

    cleaned_count = 0
    for fpath in template_files:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = cdn_pattern.sub('', content)
        new_content = config_pattern.sub('', new_content)

        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            cleaned_count += 1
            print(f"Removed Tailwind CDN from: {fpath}")

    print(f"Finished. Cleaned {cleaned_count} files.")

if __name__ == '__main__':
    remove_tailwind_cdn()
