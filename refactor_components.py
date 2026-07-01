import re

def process_component(file_path, is_navbar):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract styles
    style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    if style_match:
        styles = style_match.group(1)
        styles = re.sub(r'body\s*{[^}]*}', '', styles, flags=re.DOTALL)
        styles = '<style>\n' + styles.strip() + '\n</style>'
    else:
        styles = ''
    
    # Extract main HTML
    if is_navbar:
        body_content = re.search(r'<!-- Brand Blobs -->(.*?)<!-- Content Mockup -->', content, re.DOTALL)
    else:
        body_content = re.search(r'<!-- START FOOTER -->(.*?)<!-- END FOOTER -->', content, re.DOTALL)
        
    if body_content:
        html_content = body_content.group(1).strip()
    else:
        html_content = ''
        
    # Extract scripts
    script_match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
    if script_match:
        scripts = '<script>\n' + script_match.group(1).strip() + '\n</script>'
    else:
        scripts = ''
        
    final_html = '{% load static %}\n' + styles + '\n\n' + html_content + '\n\n' + scripts
    
    # Fix paths
    if is_navbar:
        final_html = final_html.replace('href="#" class="nav-link', 'href="{% url \'core:home\' %}" class="nav-link')
        final_html = final_html.replace('squared_efb_logo_copy-removebg-preview.png', '{% static \'images/squared_efb_logo_copy-removebg-preview.png\' %}')
    else:
        final_html = final_html.replace('EFB logo.jpg', '{% static \'images/EFB logo.jpg\' %}')
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

process_component('apps/core/templates/core/navbar.html', True)
process_component('apps/core/templates/core/footer.html', False)
print("Done")
