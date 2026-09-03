from pathlib import Path

path = Path('calculadora/index.html')
text = path.read_text(encoding='utf-8')

head_marker = '<meta name="theme-color" content="#a51016">'
head_block = '''<meta name="theme-color" content="#a51016">\n<link rel="manifest" href="./manifest.webmanifest">\n<link rel="icon" href="./icon-192.png" sizes="192x192" type="image/png">\n<link rel="apple-touch-icon" href="./icon-192.png">\n<meta name="mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n<meta name="apple-mobile-web-app-title" content="Calculadora">'''

if 'manifest.webmanifest' not in text:
    if head_marker not in text:
        raise SystemExit('theme-color marker not found')
    text = text.replace(head_marker, head_block, 1)

script_tag = '<script src="./pwa-register.js" defer></script>'
if 'pwa-register.js' not in text:
    if '</body>' not in text:
        raise SystemExit('body close marker not found')
    text = text.replace('</body>', script_tag + '\n</body>', 1)

path.write_text(text, encoding='utf-8')
