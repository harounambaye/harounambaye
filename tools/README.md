# Générateur des visuels du profil

Les images de `../assets/` sont des SVG générés par ces scripts. Le texte y est vectorisé
(mis en forme avec HarfBuzz) pour s'afficher à l'identique partout sur GitHub.

Pour modifier un texte (projet, parcours, compétences…), éditez `build.py`
(constantes `PROJECTS`, `VALUES`, `TIMELINE`, `STACK`, `HEADERS`), puis régénérez :

```bash
pip install -r requirements.txt
cd tools
python build.py ../assets    # versions bureau (1200 px) + boutons
python mobile.py ../assets   # versions mobiles (*-m.svg) + en-têtes de section
```

Les polices (Instrument Serif, Manrope, JetBrains Mono — licence OFL) sont téléchargées
dans `tools/fonts/` au premier lancement.
