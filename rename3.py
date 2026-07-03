import os

root_dir = 'c:\\Users\\hujai\\OneDrive\\Desktop\\Projects\\TELLEGRAM MUSIC BOT\\telegram-music-CHIKOO\\telegram-music-CHIKOO'

config_file = os.path.join(root_dir, 'config.py')
with open(config_file, 'r', encoding='utf-8') as f:
    config_content = f.read()

config_content = config_content.replace('https://t.me/chikooUpdates', 'https://t.me/BrokenXworld')
config_content = config_content.replace('https://t.me/chikooBotSupport', 'https://t.me/Music_Brigade_Chatting_zone')
config_content = config_content.replace("Owner I'd dalo", "8455806295")
config_content = config_content.replace("Apna Log Group Id Dalo", "-1003854544060")

with open(config_file, 'w', encoding='utf-8') as f:
    f.write(config_content)

replacements = {
    'noxarix': 'noxarix',
    'noxarix': 'noxarix',
    'noxarix': 'noxarix',
    'marine': 'marine',
    'nox_shadowx': 'nox_shadowx',
    'nox_shadowx': 'nox_shadowx',
    'ChikooXmusic': 'ChikooXmusic'
}

for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(('.py', '.json', '.md', '.txt', 'setup', 'Dockerfile', 'app.json')):
            filepath = os.path.join(subdir, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content
                for old, new in replacements.items():
                    new_content = new_content.replace(old, new)
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
            except Exception as e:
                pass

print("Replacements done.")
