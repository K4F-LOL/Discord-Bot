# Discord Community & Ticket Bot

A multipurpose Discord bot built with Python and `discord.py`. It combines support tickets, moderation, polls, anti-spam protection, welcome messages, utility commands, and server administration tools.

Most commands are hybrid commands, so they work with either the `!` prefix or Discord slash commands.

## Features

### Support tickets

- Posts an interactive **Open Ticket** button in the configured ticket channel.
- Creates a private `ticket-username` channel for the requester, the bot, and staff.
- Accepts an optional issue description when a ticket is opened with a command.
- Lets moderators close tickets and notifies the requester by direct message.
- Lets administrators assign tickets to staff members.
- Tracks created, assigned, open, and closed tickets in a local SQLite database.
- Displays ticket statistics for administrators.
- Automatically removes tickets after 24 hours if no staff member has responded.

| Command | Access | Description |
| --- | --- | --- |
| `!ticket_open [problem]` / `/ticket_open` | Everyone | Open a support ticket. |
| `!ticket_close` / `/ticket_close` | Moderator | Close the current ticket. |
| `!ticket_assign <member>` / `/ticket_assign` | Administrator | Assign a ticket to a staff member. |
| `!ticket_stats` / `/ticket_stats` | Administrator | Show total, open, and closed ticket counts. |
| `!post_ticket` / `/post_ticket` | Moderator | Repost the interactive ticket panel. |

### Polls

- Creates timed Yes/No polls or multiple-choice polls with up to eight options.
- Uses interactive Discord buttons for voting.
- Restricts each member to one active poll at a time.
- Allows poll owners to stop their own poll early.
- Allows administrators to stop another member's poll.
- Provides the bot owner with an overview of all active polls.

| Command | Access | Description |
| --- | --- | --- |
| `!poll <minutes> <title> [options...]` / `/poll` | Everyone | Create a timed poll. Omit options for Yes/No. |
| `!stoppoll [user_id]` / `/stoppoll` | Poll owner or administrator | Stop an active poll. |
| `!listpolls` / `/listpolls` | Bot owner | List all active polls. |

### Moderation

- Creates and deletes server roles.
- Kicks members from the server.
- Mutes, unmutes, deafens, undeafens, or disconnects members in voice channels.
- Purges a number of recent messages or messages sent after a specified date.

These commands require a role named `Moderator`.

| Command | Description |
| --- | --- |
| `!createrole <name>` / `/createrole` | Create a role. |
| `!deleterole <name>` / `/deleterole` | Delete a role. |
| `!kick <member> [reason]` / `/kick` | Kick a member. |
| `!mute <member>` / `/mute` | Server-mute a member in voice chat. |
| `!unmute <member>` / `/unmute` | Remove a server mute. |
| `!deafen <member>` / `/deafen` | Server-deafen a member. |
| `!undeafen <member>` / `/undeafen` | Remove server deafen. |
| `!voicekick <member>` / `/voicekick` | Disconnect a member from voice chat. |
| `!purge <amount>` / `/purge` | Delete a number of recent messages. |
| `!purge / <day> <month> [year]` | Delete messages sent after a date. |

### Anti-spam protection

- Detects rapid messages and repeated duplicate messages.
- Deletes detected spam and issues warnings.
- Times out a member after three warnings.
- Kicks a member after three spam timeouts.
- Sends moderation records to a channel named `spam-logs`, when present.
- Exempts bots, direct messages, and administrators.

### Welcome system

- Posts a welcome embed in the configured general channel.
- Sends new members a direct message containing the server rules.
- Replies when a member sends the exact message `Hello Bot`.

### Fun and utility commands

| Command | Description |
| --- | --- |
| `!ping` / `/ping` | Check whether the bot is responsive. |
| `!coinflip` / `/coinflip` | Flip a coin. |
| `!rps <hand>` / `/rps` | Play Rock, Paper, Scissors against the bot. |
| `!help` / `/help` | Display the built-in command guide. |
| `/embed_template` | Display an example Discord embed layout. |

### Owner and server administration

| Command | Access | Description |
| --- | --- | --- |
| `!servername <name>` / `/servername` | Bot owner | Change the server name. |
| `!region <region>` / `/region` | Bot owner | Change the server region. |
| `!ban <member> [reason]` / `/ban` | Bot owner | Ban a member. |
| `!unban <username>` / `/unban` | Bot owner | Unban a member by username. |
| `!createtextchannel <name>` / `/createtextchannel` | Manage Channels permission | Create a text channel. |
| `!createvoicechannel <name>` / `/createvoicechannel` | Manage Channels permission | Create a voice channel. |
| `!load <cog>` | Bot owner | Load an extension. |
| `!unload <cog>` | Bot owner | Unload an extension. |
| `!reload <cog>` | Bot owner | Reload an extension. |

## Requirements

- Python 3.10 or newer
- A Discord application and bot token
- The `discord.py` and `python-dotenv` packages

Install the dependencies:

```bash
pip install discord.py python-dotenv
```

## Setup

1. Clone the repository and enter its directory.
2. Copy `.env.example` to `.env`.
3. Add your Discord bot token to `.env`:

   ```env
   BOT_TOKEN=your_discord_bot_token_here
   ```

4. Replace the server-specific IDs in the source code:

   - General channel ID in `Cogs/welcome.py`
   - Ticket channel ID in `Cogs/tickets.py` and `Cogs/post_ticket.py`
   - Poll channel ID in `Cogs/poll.py`
   - Guild ID in `Cogs/tickets.py`
   - Bot owner user ID in `Utils/bot_util.py` and `main.py`

5. In the Discord Developer Portal, enable **Server Members Intent** and **Message Content Intent** for the bot.
6. Invite the bot with the permissions needed for the features you intend to use, including channel, role, message, moderation, voice, and member-management permissions.
7. Start the bot:

   ```bash
   python main.py
   ```

The bot creates `tickets.db` automatically when it starts. Both `.env` and database files are excluded from Git.

## Project structure

```text
.
|-- Cogs/                 # Bot features and commands
|-- Utils/                # Permission helper and ticket database
|-- .env.example          # Environment-variable template
|-- .gitignore            # Private and generated files excluded from Git
|-- main.py               # Bot entry point and extension loader
`-- README.md
```

## Security

Never commit your `.env` file or publish your Discord bot token. If a token is exposed, reset it immediately in the Discord Developer Portal.
