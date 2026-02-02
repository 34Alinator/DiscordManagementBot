# Documentation
## Introduction
Insert Description from Wilford
## Important abbreviations
### GBL:
Global Ban List, a cross-server JSON-file of banned user IDs
## Installation and Setup
### Invite link:
https://discord.com/oauth2/authorize?client_id=1467961972145258672&permissions=8&integration_type=0&scope=bot
### Permissions:
- Admin
- Presence Intent
- Server Members Intent
- Message Content Intent

Enable these in the Discord Developer Portal and when inviting the bot
### .env File:
````
DISCORD_TOKEN={API_TOKEN}
DISCORD_GUILD={SERVER_ID}
````

## Commands
### Ping:
/ping
Pings bot and responds with delay time in ms
### Global Ban:
/mglobal_ban {user}
Puts user on GBL, puts up an error if the user already is on the GBL
### Global Unban:
/mglobal_unban {user}
Removes user from GBL, puts up an error if the user is not on the GBL
### Uphold GBL:
/muphold_gbl
Sees if any user ID from the server Members list matches one from the GBL and kicks that one

## Files
### .gitignore
Specifies the ignored files for git
### Documentation.md
This Documentation
### global_ban_list.json
JSON which stores the GBL in form of an array
### main.py
Main Code for the bot
### README.md
The README

## Common Errors:
### Shard ID None is requesting privileged intents
Cause: Missing intent enablement in the Discord Developer Portal
Solution:
1. Navigate to your bot's page in the Discord Developer Portal
2. Under Bot go to Privileged Gateway intents
3. Enable Presence Intent, Server Members Intent and Message Content Intent
4. Restart the bot