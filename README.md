# Charon Webhook CLI
This project is part of [Charon](https://github.com/wireapp/charon) CLI for registering new bots that are using
 [Charon Web Hook API](https://github.com/wireapp/charon#webhook-api).
 
## Existing bots
List of service codes for the webhook bots that are deployed to the production.
* Github Actions bot - used for sending results of Github Actions to Wire.
```bash
1ca877b4-2e1a-42ef-b47d-c5ceda8b2fec:295e4e93-d347-4fe8-9f83-7a10c7c0a4c3
```

## Usage
What does this CLI do:
1) Creates new [Roman](https://github.com/dkovacevic/roman) account (if does not exist yet)
1) Creates new service in [Roman](https://github.com/dkovacevic/roman) (if does not exist yet)
1) Registers new webhook only bot in [Charon](https://github.com/wireapp/charon)

Two possible ways how to configure the CLI.

### File configuration
Please create `config.json` and fill all necessary values:
```json
{
  "email": "your@mail.com",
  "password": "your-super-strong-password"
}
```
It is also possible to specify advanced configuration:
```json
{
  "email": "your@mail.com",
  "password": "your-super-strong-password",
  "service_name": "Name of the created service",
  "bot_summary": "Summary displayed in the Wire UI",
  "roman_url": "http://your.roman.com",
  "charon_url": "http://your.charon.instance.com"
}
```

### Pass arguments to CLI

```
usage: cli.py [-h] [--file FILE] [--email EMAIL] [--password PASSWORD]
              [--service-name SERVICE_NAME] [--summary SUMMARY]
              [--env {prod,staging,local}] [--roman-url ROMAN_URL]
              [--charon-url CHARON_URL]

Register web hook bot in the Wire environment.

optional arguments:
  -h, --help            show this help message and exit
  --file FILE           Path to configuration JSON.
  --email EMAIL         Email for the Roman account.
  --password PASSWORD   Password for the account.
  --service-name SERVICE_NAME
                        Name of the service, if the account does not exist
                        yet.
  --summary SUMMARY     Summary of the service.
  --env {prod,staging,local}
                        Default configuration that is used for the missing
                        values.
  --roman-url ROMAN_URL
                        Roman URL
  --charon-url CHARON_URL
                        Charon URL
```
 
### Requirements
* python >= 3.6
* pip
* pip dependencies installed - to do that execute
```bash
make pip-install
```
 
