import zipfile, re, glob, sys
pats = re.compile(sys.argv[1])
jars = glob.glob('../mods/*.jar') + glob.glob('../*.jar')
for j in jars:
    try:
        z = zipfile.ZipFile(j)
    except Exception: continue
    for n in z.namelist():
        if n.startswith('assets/') and '/textures/' in n and n.endswith('.png') and pats.search(n):
            ns = n.split('/')[1]; p = n.split('/textures/')[1][:-4]
            print(f"{ns}:{p}")
