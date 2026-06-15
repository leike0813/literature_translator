import json
import os

batch_path = os.path.join(os.path.dirname(__file__), 'batches', 'batch_0089.json')
out_path = os.path.join(os.path.dirname(__file__), 'translations', 'batch_0089_translated.json')

with open(batch_path, 'r', encoding='utf-8') as f:
    batch = json.load(f)

result = {
    'batch_id': batch['batch_id'],
    'original_batch': batch['batch_id'],
    'blocks': {}
}

for bid, bdata in batch['blocks'].items():
    # bib_item blocks: keep sentences unchanged
    result['blocks'][bid] = {
        'type': bdata['type'],
        'sentences': [s[1] for s in bdata['sentences']]
    }

with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f'Written: {out_path}')
print(f'Size: {os.path.getsize(out_path)} bytes')
