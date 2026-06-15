import json
import re
import sys
from pathlib import Path

PH_RE = re.compile(r'<[A-Z]+(?:_[A-Z]+)?_\d+>')

def restore_text(text, entries):
    def replace_match(m):
        return entries.get(m.group(0), m.group(0))
    return PH_RE.sub(replace_match, text)

translations_dir = Path('.literature_translator_tmp/translations')
output_dir = Path('.literature_translator_tmp/translations_restored')
map_path = Path('.literature_translator_tmp/protected/placeholder_map.json')

placeholder_map = json.loads(map_path.read_text(encoding='utf-8'))
entries = placeholder_map.get('entries', {})

output_dir.mkdir(parents=True, exist_ok=True)

ok = 0
bad = 0
for tf in sorted(translations_dir.glob('*_translated.json')):
    try:
        raw = tf.read_text(encoding='utf-8')
        data = json.loads(raw)
        for block_id, block_data in data.get('blocks', {}).items():
            sentences = block_data.get('sentences', [])
            restored = []
            for item in sentences:
                if isinstance(item, (list, tuple)):
                    restored.append([item[0], restore_text(item[1], entries)])
                else:
                    restored.append(restore_text(item, entries))
            data['blocks'][block_id]['sentences'] = restored
        out_path = output_dir / tf.name
        out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        ok += 1
    except Exception as e:
        bad += 1
        print(f'ERROR on {tf.name}: {e}', flush=True)
        # Try to write untranslated version as fallback
        try:
            raw = tf.read_bytes()
            # Try utf-8-sig (BOM)
            text = raw.decode('utf-8-sig')
            data = json.loads(text)
            out_path = output_dir / tf.name
            out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
            print(f'  Recovered with utf-8-sig', flush=True)
            ok += 1
            bad -= 1
        except Exception as e2:
            print(f'  Recovery failed: {e2}', flush=True)

print(f'Restored: {ok}, Failed: {bad}', flush=True)
print(f'Output files: {len(list(output_dir.glob("*_translated.json")))}', flush=True)
