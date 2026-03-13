---
description: Deploy latest master to production server for fernando_aragon_project
---

# Deploy fernando_aragon_project to Production

Run these steps on the production server at `/home/ryzepeck/webapps/fernando_aragon_project` to deploy the latest `master` branch.

## Pre-Deploy

// turbo
1. Quick status snapshot before deploy:
```bash
bash ~/scripts/quick-status.sh
```

## Deploy Steps

// turbo
2. Pull the latest code from master:
```bash
cd /home/ryzepeck/webapps/fernando_aragon_project && git pull origin master
```

3. Install backend dependencies and run migrations:
```bash
cd /home/ryzepeck/webapps/fernando_aragon_project/backend && source venv/bin/activate && pip install -r requirements.txt && DJANGO_SETTINGS_MODULE=base_feature_project.settings_prod python manage.py migrate
```

4. Build the frontend (Vite SPA):
```bash
cd /home/ryzepeck/webapps/fernando_aragon_project/frontend && npm ci && npm run build
```

5. Collect static files:
```bash
cd /home/ryzepeck/webapps/fernando_aragon_project/backend && source venv/bin/activate && DJANGO_SETTINGS_MODULE=base_feature_project.settings_prod python manage.py collectstatic --noinput
```

6. Restart services:
```bash
sudo systemctl restart fernando_aragon_project && sudo systemctl restart fernando-aragon-huey
```

## Post-Deploy Verification

// turbo
7. Run post-deploy check for fernando_aragon_project:
```bash
bash ~/scripts/post-deploy-check.sh fernando_aragon_project
```
Expected: PASS on all checks, FAIL=0.

8. If something fails, check the logs:
```bash
sudo journalctl -u fernando_aragon_project --no-pager -n 30
sudo journalctl -u fernando-aragon-huey --no-pager -n 30
sudo tail -20 /var/log/nginx/error.log
```

9. (Optional) Full server diagnostic with score:
```bash
bash ~/scripts/full-diagnostic.sh
```

## Verification Scripts Reference

| Script | Purpose | When to use |
|--------|---------|-------------|
| `bash ~/scripts/quick-status.sh` | Snapshot rápido: RAM, disco, servicios, SSL | Pre-deploy, sanity check |
| `bash ~/scripts/full-diagnostic.sh` | Diagnóstico completo con score | Auditorías, debugging profundo |
| `bash ~/scripts/post-deploy-check.sh fernando_aragon_project` | Verificación post-deploy | Después de cada deploy |

## Architecture Reference

- **Domain**: `fernandodearagon.projectapp.co`
- **Backend**: Django (`base_feature_project` module), `DJANGO_SETTINGS_MODULE=base_feature_project.settings_prod`
- **Frontend**: Vite + React SPA → `frontend/dist/` served by nginx
- **Services**: `fernando_aragon_project.service` (Gunicorn via socket), `fernando-aragon-huey.service`
- **Nginx**: `/etc/nginx/sites-available/fernando_aragon_project`
- **Socket**: `/home/ryzepeck/webapps/fernando_aragon_project/fernando_aragon_project.sock`
- **Static**: `/home/ryzepeck/webapps/fernando_aragon_project/backend/staticfiles/`
- **Media**: `/home/ryzepeck/webapps/fernando_aragon_project/backend/media/`
- **Resource limits**: MemoryMax=250MB, CPUQuota=40%, OOMScoreAdjust=300

## Notes

- `~/scripts` is a symlink to `/home/ryzepeck/webapps/ops/vps/`.
- Frontend `npm ci` may take a few minutes; the backend stays up during build.
- If MemoryMax is hit during deploy, the service will be killed and restarted automatically.
