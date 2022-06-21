# Experimental NixOS Security Tracker

The **Arch Linux Security Tracker** is a lightweight flask based panel
for tracking vulnerabilities in Arch Linux packages, displaying
vulnerability details and generating security advisories.

This is a hacked-up version of said tracker, currently being evaluated
for coordinating NixOS's security team.

## Features

* Issue tracking
* Issue grouping
* Todo lists
* Advisory scheduling
* Advisory generation
* SSO or local users

## Command line interface

The ```trackerctl``` script provides access to the command line interface
that controls and operates different parts of the tracker. All commands
and subcommands provide a ```--help``` option that describes the operation
and all its available options.

## Configuration

Defaults can be seen in `config/00-default.conf`. Further values will be
loaded from the directory specified by the `TRACKER_CONFIG_DIR`
environment variable, or `/etc/security-tracker` if this is not set.

## SSO setup

A simple test environment for SSO can be configured using Keycloak:

1. Run a local Keycloak installation via docker as [described
   upstream](https://www.keycloak.org/getting-started/getting-started-docker).

2. Create an ```arch-security-tracker``` client in Keycloak like in
   [test/data/openid-client.json](test/data/openid-client.json).
   Make sure the client contains a mapper for the group memberships called
   ```groups``` which is included as a claim.

3. Create a local tracker config file with enabled SSO and configure OIDC
   secrets, groups and metadata url accordingly.

## Contribution

Help is appreciated, for some guidelines and recommendations check our
[Contribution](CONTRIBUTING.md) file.
