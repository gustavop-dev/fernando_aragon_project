---
name: deploy-and-check
description: "Deploy latest master/main to the production server with pre-deploy checks, build, restart, and post-deploy verification."
disable-model-invocation: true
allowed-tools: Bash
---

> Ejecutar estos pasos conectado al servidor de producción vía SSH.
> Ruta base: `/home/ryzepeck/webapps/fernando_aragon_project`
> NO ejecutar en local.

# Deploy fernando_aragon_project to Production

Run these steps on the production server at `/home/ryzepeck/webapps/fernando_aragon_project` to deploy the latest `main` branch.

## Pre-Deploy

1. Quick status snapshot before deploy:
```bash
bash /home/ryzepeck/webapps/ops/vps/scripts/diagnostics/quick-status.sh
```

## Deploy Steps

2. Pull the latest code from main:
```bash
cd /home/ryzepeck/webapps/fernando_aragon_project && git pull origin master
```

3. Install backend dependencies and run migrations:
```bash
cd /home/ryzepeck/webapps/fernando_aragon_project/backend && source venv/bin/activate && pip install -r requirements.txt && DJANGO_SETTINGS_MODULE=base_feature_project.settings_prod python manage.py migrate
```

4. Build the frontend (Vite build + copy to Django static):
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

7. Run post-deploy check for fernando_aragon_project:
```bash
bash /home/ryzepeck/webapps/ops/vps/scripts/deployment/post-deploy-check.sh fernando_aragon_project
```
Expected: PASS on all checks, FAIL=0.

8. If something fails, check the logs:
```bash
sudo journalctl -u fernando_aragon_project.service --no-pager -n 30
sudo journalctl -u fernando-aragon-huey.service --no-pager -n 30
sudo tail -20 /var/log/nginx/error.log
```

## Architecture Reference

- **Domain**: `fernandodearagon.edu.co` / `www.fernandodearagon.edu.co`
- **Backend**: Django (`fernando_aragon_project` module), settings selected via `DJANGO_SETTINGS_MODULE=base_feature_project.settings_prod` in systemd unit
- **Frontend**: React 18.3 + Vite 7 SPA → `backend/static/frontend/`
- **Services**: `fernando_aragon_project.service` (Gunicorn via socket), `fernando_aragon_project.socket`, `fernando-aragon-huey.service`
- **Nginx**: `/etc/nginx/sites-available/fernando_aragon_project`
- **Socket**: `/home/ryzepeck/webapps/fernando_aragon_project/fernando_aragon_project.sock`
- **Static**: `/home/ryzepeck/webapps/fernando_aragon_project/backend/staticfiles/`
- **Media**: `/home/ryzepeck/webapps/fernando_aragon_project/backend/media/`
- **Resource limits**: MemoryMax=250M, CPUQuota=40%, OOMScoreAdjust=300

## Cleanup

9. Remove `node_modules` to save disk space (frontend already compiled):
```bash
rm -rf /home/ryzepeck/webapps/fernando_aragon_project/frontend/node_modules
```

## Notes

- VPS operations scripts live in `/home/ryzepeck/webapps/ops/vps/scripts/`.
- Frontend uses `npm run build` which runs the Vite build and copies output to `backend/static/frontend/`.
- `DJANGO_SETTINGS_MODULE=base_feature_project.settings_prod` must be set for migrate and collectstatic commands (manage.py defaults to settings_dev).
