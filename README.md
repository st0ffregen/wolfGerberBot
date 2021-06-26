# Build
```
docker build -t wolf-gerber-bot ./bot
```

# Live
```
docker run -it -it -v "$(pwd)/bot:/usr/src/app" --rm --env-file .env --name wolf-gerber-bot-running wolf-gerber-bot
```