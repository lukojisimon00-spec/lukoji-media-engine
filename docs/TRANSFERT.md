# Transfert vers le dépôt GitHub `lukoji-media-engine`

Le travail de la phase 0 est un dépôt Git **local**, dans `/home/user/lukoji-media-engine`, sur la branche `main`.
Le dépôt GitHub n'existait pas, ou n'était pas accessible, au moment de l'exécution.

⚠️ Le conteneur de session est **éphémère**. Tant que le transfert n'est pas fait, le travail n'existe que
dans cette session. Il y a donc deux façons de le sécuriser.

## Option A — recommandée : pousser depuis la session

1. Sur GitHub, créer un dépôt **vide** et privé `lukojisimon00-spec/lukoji-media-engine`, sans README ni licence ni .gitignore.
2. Vérifier que l'application GitHub Claude a accès à ce dépôt.
3. Dans la session Claude Code, demander : « pousse lukoji-media-engine ». Claude attache le dépôt, puis :
   ```bash
   cd /home/user/lukoji-media-engine
   git remote add origin <url fournie par l'attachement>
   git push -u origin main
   ```

## Option B — archive Git autonome (bundle)

Un fichier `lukoji-media-engine.bundle` contient tout l'historique :

```bash
git clone lukoji-media-engine.bundle lukoji-media-engine
cd lukoji-media-engine
git remote set-url origin git@github.com:lukojisimon00-spec/lukoji-media-engine.git
git push -u origin main
```

## Après le transfert : vérification

```bash
./bin/lukoji brand-verify     # empreintes des originaux
./scripts/run_phase0.sh       # rejoue toute la validation (sources de test : variables SRC_VERTICAL / SRC_HORIZONTAL)
```

Sur une autre machine, il faut : FFmpeg avec libx264, Python ≥ 3.11 avec Pillow, numpy et pytest, et Node.js avec Playwright
(`npm i -D playwright && npx playwright install chromium`).
