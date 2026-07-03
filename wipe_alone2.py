import os

root_dir = r'c:\Users\hujai\OneDrive\Desktop\Projects\TELLEGRAM MUSIC BOT\telegram-music-CHIKOO\telegram-music-CHIKOO'

replacements = {
    'noxarix/ChikooXmusic': 'noxarix/ChikooXmusic',
    'noxarix': 'noxarix',
    'ChikooXmusic': 'ChikooXmusic',
    'ChikooMusic_bot': 'ChikooMusic_bot',
    'Music_Brigade_Chatting_zone': 'Music_Brigade_Chatting_zone',
    'BrokenXworld': 'BrokenXworld',
    'Chikoo_family': 'Chikoo_family',
    'Chikoo music': 'Chikoo music',
    'noxarix': 'noxarix',
    'nox_shadowx': 'nox_shadowx',
    'Chikoo': 'Chikoo',
    'CHIKOO': 'CHIKOO',
    'chikoo': 'chikoo',
    'https://files.catbox.moe/6notyf.jpg': 'https://files.catbox.moe/6notyf.jpg',
    'https://files.catbox.moe/6notyf.jpg': 'https://files.catbox.moe/6notyf.jpg',
    'https://files.catbox.moe/6notyf.jpg': 'https://files.catbox.moe/6notyf.jpg'
}

skip_dirs = {'.git', '__pycache__'}
skip_files = {'.env', 'chikoo.session', 'chikoo.session-journal', '.gitignore'}

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original = content
        for k, v in replacements.items():
            content = content.replace(k, v)
            
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {filepath}")
    except UnicodeDecodeError:
        pass

for root, dirs, files in os.walk(root_dir):
    dirs[:] = [d for d in dirs if d not in skip_dirs]
    for file in files:
        if file in skip_files or file.endswith('.pyc') or file.endswith('.jpg') or file.endswith('.png') or file.endswith('.zip'):
            continue
        filepath = os.path.join(root, file)
        process_file(filepath)

print("Done wiping Chikoo references!")
