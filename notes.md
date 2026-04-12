# Green Metrics Tool — Notes

## Commandes de base
```bash
# Voir toutes les images et containers (être dans le dossier green-metrics-tool)
docker ps

# Activer le venv
source venv/bin/activate

# Lancer un test (être dans le dossier green-metrics-tool)
python3 runner.py --uri ~/gmt --name "testUblock"
```

## Débeugage

> **Rem :** si erreur `"connection to port … failed"` => Docker n'est pas lancé → ouvrir l'app Docker

### Réinitialiser Docker
```bash
# Restart les containers
docker restart green-coding-gunicorn-container
docker restart green-coding-nginx-container

# Rebuild complet
docker compose down -v
docker compose up --build

# OU simple restart
docker compose restart
```

### Redémarrer l'ordi
```bash
sudo reboot
```

### Options de lancement pour déboguer
```bash
# Avec sudo (éviter les problèmes d'autorisation)
sudo python3 runner.py --uri ~/gmt --name "debug"

# Flags utiles
python3 runner.py --uri ~/gmt --name "debug" --verbose
python3 runner.py --uri ~/gmt --name "debug" --docker-prune
python3 runner.py --uri ~/gmt --name "debug" --dev-no-system-checks
```

### Erreur "il y a déjà des mesures en cours"
```bash
# Voir les processus en cours
ps aux | grep powermetrics

# Tuer un process spécifique
sudo kill -9 <le_numero_de_pid>

# Tuer tous les process GMT qui traînent
sudo pkill -f "metric_providers"
sudo pkill -f powermetrics
sudo pkill -f metric_providers
```

## Conventions choisies
### Vidéos youtube : 

https://youtu.be/Y4J_NYAQQEQ?si=BLcMRRYQMqy0-23l

### Noms à donner pour les mesures :
```
ytb-Ublock
ytb-AdGuard
ytb-AdBlockPlus
ytb-noAddBlock
ytb-premium

# nouvelles vidéos
ytb-Ublock-v2
ytb-AdGuard-v2
ytb-AdBlockPlus-v2
ytb-noAddBlock-v2
ytb-premium-v2

#avec un flow PlayVideo qui mesure uniquement pendant que les vidéos jouent
ytb-Ublock-v3
ytb-AdGuard-v3
ytb-AdBlockPlus-v3
ytb-noAddBlock-v3
ytb-premium-v3

```
