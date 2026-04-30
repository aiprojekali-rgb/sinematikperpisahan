import os
import re

html_path = 'c:/xampp1/htdocs/CINEMATIC GRADUATION/graduation-slideshow.html'
output_dir = 'c:/xampp1/htdocs/CINEMATIC GRADUATION/output'

images = [f for f in os.listdir(output_dir) if f.endswith(('.png', '.jpg', '.JPG'))]

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

photo_pool_js = 'const PHOTO_POOL = [\n' + ',\n'.join([f'      "{img}"' for img in images]) + '\n    ];'

content = re.sub(r'const PHOTO_POOL = \[.*?\];', photo_pool_js, content, flags=re.DOTALL)

new_photo_assign = """const photoAssign = STUDENTS.map((s, i) => {
      // Find exact match first
      let match = PHOTO_POOL.find(p => p.toLowerCase() === s.nama.toLowerCase() + '_processed.jpg');
      
      // If no exact match, try partial match (e.g. for "alvin" instead of "ALVIN HAIDAR ABDILAH")
      if (!match) {
        // Split student name and try to find first name match
        const firstName = s.nama.split(' ')[0].toLowerCase();
        match = PHOTO_POOL.find(p => p.toLowerCase().includes(firstName));
      }

      if (match) {
        return `output/${match}`;
      }
      
      // Fallback
      return `output/${s.nama}_processed.jpg`;
    });"""

content = re.sub(r'const photoAssign = STUDENTS\.map\(\(_, i\) => PHOTO_POOL\[i % PHOTO_POOL\.length\]\);', new_photo_assign, content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Update successful.')
