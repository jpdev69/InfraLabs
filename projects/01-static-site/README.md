# Static site, one container

> Goal: Run your first container and make it survive restarts.

## Success criteria

- [ ] `http://localhost:8080` loads the site
- [ ] Editing `index.html` on your machine is reflected after a browser refresh — no container restart
- [ ] `docker stop` then `docker start` brings the identical site back — nothing reconfigured
- [ ] `docker ps` shows the container running with the restart policy you chose
- [ ] `docs/notes.md` explains, in your own words: image vs container vs the host folder you mounted
- [ ] You can show the container's logs with one command

## Architecture

- containers/services:
- ports:
- volumes:
- networks:

## Run

- scripts/up.ps1 brings it up
- scripts/destroy.ps1 tears it down
