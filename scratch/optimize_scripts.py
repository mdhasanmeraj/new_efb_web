import os
import re

def optimize_template_scripts():
    template_files = []
    for root, dirs, files in os.walk('.'):
        if 'node_modules' in root or '.git' in root or 'venv' in root or '.gemini' in root:
            continue
        for f in files:
            if f.endswith('.html'):
                template_files.append(os.path.join(root, f))

    unobserve_pattern = re.compile(
        r'if\s*\(\s*entry\.isIntersecting\s*\)\s*\{([^}]+)\}',
        re.DOTALL
    )

    for fpath in template_files:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = content
        
        # 1. Update IntersectionObserver entries to unobserve after triggering once if not already unobserved
        if 'IntersectionObserver' in content and 'unobserve' not in content and 'disconnect' not in content:
            # Add unobserve(entry.target) inside isIntersecting block
            def add_unobserve(match):
                body = match.group(1)
                return f"if (entry.isIntersecting) {{\n{body}\n                    observer.unobserve(entry.target);"
            new_content = re.sub(r'if\s*\(\s*entry\.isIntersecting\s*\)\s*\{([^}]+)\}', add_unobserve, new_content, count=1)

        # 2. Update Three.js initialization to check for mobile/reduced motion
        if 'function initGlobe' in content and 'window.innerWidth < 768' not in content:
            mobile_guard = """function initGlobe() {
        if (window.innerWidth < 768 || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            return;
        }"""
            new_content = new_content.replace('function initGlobe() {', mobile_guard)

        # 3. Add pause/play animation logic on tab visibility change or offscreen
        if 'requestAnimationFrame(animate)' in new_content and 'document.hidden' not in new_content:
            new_content = new_content.replace(
                'requestAnimationFrame(animate);',
                'if (!document.hidden) requestAnimationFrame(animate);'
            )

        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Optimized JS / Observers in: {fpath}")

if __name__ == '__main__':
    optimize_template_scripts()
