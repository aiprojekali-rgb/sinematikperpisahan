import os
import re

html_path = 'c:/xampp1/htdocs/CINEMATIC GRADUATION/index.html'
output_dir = 'c:/xampp1/htdocs/CINEMATIC GRADUATION/output'

images = [f for f in os.listdir(output_dir) if f.endswith(('.png', '.jpg', '.JPG'))]

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

photo_pool_js = 'const PHOTO_POOL = [\n' + ',\n'.join([f'      "{img}"' for img in images]) + '\n    ];'

content = re.sub(r'const PHOTO_POOL = \[.*?\];', photo_pool_js, content, flags=re.DOTALL)

new_photo_assign = """const photoAssign = STUDENTS.map((s, i) => {
      // 1. Exact match
      let match = PHOTO_POOL.find(p => p.toLowerCase() === s.nama.toLowerCase() + '_processed.jpg');

      // 2. Try removing spaces and special characters for exact match
      if (!match) {
        const cleanName = s.nama.toLowerCase().replace(/[^a-z0-9]/g, '');
        match = PHOTO_POOL.find(p => p.toLowerCase().replace(/[^a-z0-9]/g, '').replace('processedjpg', '') === cleanName);
      }

      // 3. Try matching by longest unique word in the student's name (avoiding common names)
      if (!match) {
        // Find words longer than 3 chars, exclude common titles/names
        const words = s.nama.toLowerCase().split(/\\s+/).filter(w => 
          w.length > 3 && !['muhamad', 'muhammad', 'ahmad', 'siti', 'putri', 'putra', 'raden', 'tubagus'].includes(w)
        );
        
        for (const w of words) {
          const possibleMatches = PHOTO_POOL.filter(p => p.toLowerCase().includes(w));
          // Only assign if exactly ONE person in the photo pool matches this word
          if (possibleMatches.length === 1) {
            match = possibleMatches[0];
            break;
          }
        }
      }

      // 4. Try matching the first name if it's not common and unique in the pool
      if (!match) {
        const firstName = s.nama.split(' ')[0].toLowerCase();
        if (!['m', 'mohd', 'muhamad', 'muhammad', 'ahmad', 'siti'].includes(firstName)) {
          const possibleMatches = PHOTO_POOL.filter(p => p.toLowerCase().includes(firstName));
          if (possibleMatches.length === 1) {
             match = possibleMatches[0];
          }
        }
      }

      if (match) {
        return `output/${match}`;
      }

      // Fallback (akan menghasilkan 404 tapi mencegah salah foto muka orang)
      return `output/${s.nama}_processed.jpg`;
    });"""

content = re.sub(r'const photoAssign = STUDENTS\.map\(\(_, i\) => PHOTO_POOL\[i % PHOTO_POOL\.length\]\);', new_photo_assign, content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Update successful.')
