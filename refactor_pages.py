import os
import re

def refactor_template(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Avoid processing small stub files unless they have html tags
    if len(content) < 300 and '<html' not in content:
        return

    # Extract head contents
    head_match = re.search(r'<head>(.*?)</head>', content, re.DOTALL | re.IGNORECASE)
    head_content = head_match.group(1) if head_match else ""

    # Extract body contents
    body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
    if body_match:
        body_content = body_match.group(1)
    else:
        # If no body, take everything after head, or the whole file
        if head_match:
            body_content = content[head_match.end():]
        else:
            body_content = content

    # 1. Gather Extra CSS (Styles, Tailwind Config, Non-Font Links)
    extra_css = []
    
    # Extract styles from head
    for match in re.finditer(r'<style[^>]*>.*?</style>', head_content, re.DOTALL | re.IGNORECASE):
        # Remove body style if it specifies fonts to enforce base.html fonts
        style_block = match.group(0)
        style_block = re.sub(r'body\s*{[^}]*font-family[^}]*}', '', style_block, flags=re.DOTALL | re.IGNORECASE)
        extra_css.append(style_block)
        
    # Extract Tailwind config or other scripts from head that look like CSS setups
    for match in re.finditer(r'<script[^>]*>.*?</script>', head_content, re.DOTALL | re.IGNORECASE):
        script_text = match.group(0)
        if 'tailwind.config' in script_text or 'tailwindcss.com' in script_text:
            extra_css.append(script_text)

    # Extract CSS Links (ignore Google Fonts as they are global)
    for match in re.finditer(r'<link[^>]*>', head_content, re.DOTALL | re.IGNORECASE):
        link_text = match.group(0)
        if 'fonts.googleapis.com' not in link_text and 'fonts.gstatic.com' not in link_text:
            extra_css.append(link_text)

    # 2. Gather Extra JS
    extra_js = []
    
    # Extract scripts from body
    # Instead of removing them, let's keep them in the body content or move them to extra_js
    # We will move them to extra_js to follow Django best practices
    body_scripts = []
    for match in re.finditer(r'<script[^>]*>.*?</script>', body_content, re.DOTALL | re.IGNORECASE):
        extra_js.append(match.group(0))
        body_scripts.append(match.group(0))
        
    for script in body_scripts:
        body_content = body_content.replace(script, '')

    # 3. Clean up the body content
    # Remove any existing {% extends ... %} and {% load static %} from the body content
    body_content = re.sub(r'{%\s*extends\s+[^%]+%}', '', body_content)
    body_content = re.sub(r'{%\s*load\s+static\s*%}', '', body_content)
    
    # Remove standalone navbar/footer includes if they are there, as they are in base.html
    body_content = re.sub(r'{%\s*include\s+[\'"]core/navbar\.html[\'"]\s*%}', '', body_content)
    body_content = re.sub(r'{%\s*include\s+[\'"]core/footer\.html[\'"]\s*%}', '', body_content)
    
    # 4. Fix static asset paths
    # Replace src="filename.ext" with src="{% static 'images/filename.ext' %}"
    # Ignore http, https, data:
    def replace_src(match):
        full = match.group(0)
        quote = match.group(1)
        path = match.group(2)
        if path.startswith('http') or path.startswith('data:') or path.startswith('{%'):
            return full
        # It's a local file
        filename = path.split('/')[-1]
        return f'src={quote}{{{"% static 'images/" + filename + "' %"}}}{quote}'
    
    body_content = re.sub(r'src=([\'"])(.*?\.([a-zA-Z0-9]+))[\'"]', replace_src, body_content)
    
    def replace_url(match):
        full = match.group(0)
        quote = match.group(2) if match.group(2) else ""
        path = match.group(3)
        if path.startswith('http') or path.startswith('data:') or path.startswith('{%'):
            return full
        filename = path.split('/')[-1]
        return f'url({quote}{{{"% static 'images/" + filename + "' %"}}}{quote})'
        
    body_content = re.sub(r'url\((\s*[\'"]?)(.*?\.([a-zA-Z0-9]+))([\'"]?\s*)\)', replace_url, body_content)
    
    # Do the same for extra_css styles
    new_extra_css = []
    for css in extra_css:
        css = re.sub(r'url\((\s*[\'"]?)(.*?\.([a-zA-Z0-9]+))([\'"]?\s*)\)', replace_url, css)
        new_extra_css.append(css)
    extra_css = new_extra_css

    # Assemble Final Content
    final_content = "{% extends 'base.html' %}\n{% load static %}\n\n"
    
    if extra_css:
        final_content += "{% block extra_css %}\n"
        final_content += "\n".join(extra_css)
        final_content += "\n{% endblock %}\n\n"
        
    final_content += "{% block content %}\n"
    final_content += body_content.strip()
    final_content += "\n{% endblock %}\n\n"
    
    if extra_js:
        final_content += "{% block extra_js %}\n"
        final_content += "\n".join(extra_js)
        final_content += "\n{% endblock %}\n"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(final_content)

pages = [
    'home.html', 'about_us.html', 'become_partner.html', 'contact_us.html', 
    'credit_card.html', 'personal_loan.html'
]

for p in pages:
    path = os.path.join('apps', 'core', 'templates', 'core', p)
    if os.path.exists(path):
        refactor_template(path)
        print(f"Refactored {p}")
    else:
        print(f"Skipped {p} (not found)")

print("Refactoring complete.")
