from pathlib import Path
from tempfile import TemporaryDirectory
import json
import os
import subprocess
import sys

script = Path(__file__).resolve().parents[1] / 'scripts' / 'srt_fast.py'
with TemporaryDirectory() as tmp:
    source = Path(tmp) / 'source.srt'
    snapshot = Path(tmp) / 'snapshot.json'
    source.write_text('1\n00:00:00,000 --> 00:00:02,000\nexample line\n', encoding='utf-8')
    result = subprocess.run([sys.executable, '-S', str(script), 'scan', str(source), '--snapshot', str(snapshot), '--summary'], capture_output=True, text=True, encoding='utf-8', env={**os.environ, 'PYTHONIOENCODING': 'utf-8'})
    assert result.returncode == 0, result.stderr
    assert 'CUES=1' in result.stdout and 'example line' not in result.stdout
    assert json.loads(snapshot.read_text(encoding='utf-8'))['rows'][0]['text'] == 'example line'
print('SRT summary PASS')
