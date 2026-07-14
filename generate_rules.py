import os
import re

def main():
    list_dir = 'list'
    packages = {}

    # Regular expression to robustly match both:
    # 1. - "package.name": "app name"
    # 2. "package.name": "app name"
    # and handle optional single/double quotes around package name and app name
    pattern = re.compile(r'^\s*(?:-\s*)?["\']?([a-zA-Z0-9._-]+)["\']?\s*:\s*["\']?([^"\']+)["\']?\s*$')

    if not os.path.isdir(list_dir):
        print(f"Error: Directory '{list_dir}' does not exist.")
        return

    # Process all YAML files in the list folder
    for filename in sorted(os.listdir(list_dir)):
        if not filename.endswith('.yaml'):
            continue
        
        filepath = os.path.join(list_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                # Remove trailing comments if any (unless they are part of the value)
                # But since our app names don't contain #, we can safely split or strip
                raw_line = line.split('#')[0].strip()
                if not raw_line or raw_line == 'app-list:':
                    continue
                
                m = pattern.match(raw_line)
                if m:
                    pkg = m.group(1).strip()
                    name = m.group(2).strip()
                    # Keep the record, if duplicate, we can prefer keeping the non-empty or newer one
                    packages[pkg] = name

    # Generate the Clash rule-set yaml file
    output_file = 'clash_android_rules.yaml'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 自动生成 Clash Rule-Set: Android Apps\n")
        f.write("payload:\n")
        for pkg in sorted(packages.keys()):
            app_name = packages[pkg]
            f.write(f"  - PROCESS-NAME,{pkg} #Android:{app_name}\n")

    print(f"Successfully generated Clash rule-set with {len(packages)} apps in '{output_file}'")

if __name__ == '__main__':
    main()
