# n8n Conversation

[![My Home Assistant](https://img.shields.io/badge/Home%20Assistant-%2341BDF5.svg?style=flat&logo=home-assistant&label=My)](https://my.home-assistant.io/redirect/hacs_repository/?owner=EuleMitKeule&repository=n8n-conversation&category=integration)

![GitHub License](https://img.shields.io/github/license/eulemitkeule/n8n-conversation)
![GitHub Sponsors](https://img.shields.io/github/sponsors/eulemitkeule?logo=GitHub-Sponsors)

> [!NOTE]
> This integration requires Home Assistant `2025.8`.

_Integration to connect Home Assistant with n8n workflows through conversation agents._

**This integration allows you to use n8n workflows as conversation agents in Home Assistant, enabling powerful automation and AI-driven interactions with your smart home.**

## Features

- 🤖 Use n8n workflows as conversation agents in Home Assistant
- 📡 Send conversation context and exposed entities to n8n webhooks
- 🏠 Seamless integration with Home Assistant's voice assistant system
- 🔧 Configurable webhook URLs and output fields

## Installation

### HACS (Recommended)

> [!NOTE]
> **Quick Install**: Click the "My Home Assistant" badge at the top of this README for one-click installation via HACS.

1. Make sure [HACS](https://hacs.xyz/) is installed
2. Add this repository as a custom repository in HACS:
   - Go to HACS → Integrations → ⋮ → Custom repositories
   - Add `https://github.com/eulemitkeule/n8n-conversation` as an Integration
3. Search for "n8n Conversation" in HACS and install it
4. Restart Home Assistant

### Manual Installation

1. Download the latest release from the [releases page](https://github.com/eulemitkeule/n8n-conversation/releases)
2. Extract the `custom_components/n8n_conversation` folder to your `custom_components` directory
3. Restart Home Assistant

## Configuration

### Home Assistant Setup

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration** and search for "n8n Conversation"
3. Configure the integration with:
   - **Name**: A friendly name for your n8n agent
   - **Webhook URL**: The URL of your n8n webhook endpoint (remember to activate the workflow in n8n and to use the production webhook URL)
   - **Output Field**: The field name in the n8n response containing the reply (default: "output")

### n8n Workflow Setup

Create an n8n workflow with the following structure:

1. **Webhook Trigger**: Set up a webhook trigger to receive POST requests from Home Assistant
2. **Process the payload**: The webhook will receive:

   ```json
   {
     "user_id": "user_id_from_ha",
     "messages": [
       {
         "role": "user|assistant|system",
         "content": "message_content"
       }
     ],
     "query": "latest_user_message",
     "exposed_entities": [
       {
         "entity_id": "light.living_room",
         "name": "Living Room Light",
         "state": "on",
         "aliases": ["main light"],
         "area_id": "living_room",
         "area_name": "Living Room"
       }
     ]
   }
   ```

3. **Your AI/Processing Logic**: Process the conversation and entity data
4. **Return Response**: Return a JSON response with your configured output field:

   ```json
   {
     "output": "Your AI assistant response here"
   }
   ```

## Usage

### Voice Assistant Pipeline Setup

To use the n8n conversation agent with voice assistants, you need to create a voice assistant pipeline:

1. Go to **Settings** → **Voice assistants**
2. Click **Add Assistant**
3. Configure your pipeline:
   - **Name**: Give your pipeline a descriptive name (e.g., "n8n Assistant")
   - **Language**: Select your preferred language
   - **Speech-to-text**: Choose your preferred STT engine (e.g., Whisper, Google Cloud)
   - **Conversation agent**: Select your n8n conversation agent from the dropdown
   - **Text-to-speech**: Choose your preferred TTS engine (e.g., Google Translate, Piper)
   - **Wake word**: Optionally configure a wake word engine
4. Click **Create** to save your pipeline
5. Set this pipeline as the default for voice assistants or assign it to specific devices

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

- 🐛 [Report issues](https://github.com/eulemitkeule/n8n-conversation/issues)
- 💬 [GitHub Discussions](https://github.com/eulemitkeule/n8n-conversation/discussions)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
