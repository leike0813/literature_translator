import json
from pathlib import Path

for fname in ['batch_0019_translated.json', 'batch_0062_translated.json']:
    f = Path('.literature_translator_tmp/translations') / fname
    raw = f.read_bytes()
    print(f'=== {fname} ===')
    print(f'Size: {len(raw)} bytes')
    try:
        text = raw.decode('utf-8')
        json.loads(text)
        print('OK')
    except json.JSONDecodeError as e:
        print(f'Error: {e}')
        pos = e.pos
        context = raw[max(0,pos-30):pos+30]
        print(f'Raw bytes around pos {pos}: {context}')
        print(f'Hex: {context.hex()}')
        # Show the problematic character
        print(f'Char at pos: {repr(raw[pos:pos+5])}')
    print()
