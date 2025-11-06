# Browser Agent - Greenhouse ATS Automation 🤖

This demo showcases an **autonomous browser agent** that can log into Greenhouse ATS (Applicant Tracking System) and navigate to job applications using **LangGraph** and **Azure OpenAI**.

## 🎯 What This Demo Shows

This example demonstrates:
- **Autonomous Browser Agent**: Agent that can navigate websites and interact with UI
- **Multi-step Task Execution**: Login → Navigate → Search → Open Job → Access Applications
- **Vision-based Understanding**: Agent uses screenshots to understand web pages
- **ReAct Pattern**: Agent reasons about what it sees and decides actions
- **Tool-based Interaction**: Agent uses browser tools (click, type, navigate, etc.)

## 📋 Demo Task

**Mission**: Navigate to the applications page for a specific job posting.

The agent is given:
- ✅ High-level goal (access job applications)
- ✅ Login credentials
- ✅ Target job name
- ❌ **NO** step-by-step instructions

The agent **autonomously figures out**:
- How to login
- Where to find the Jobs section
- How to search for the job
- How to open the job
- How to access applications

This demonstrates true autonomous behavior - the agent reasons about the UI and decides its own actions!

### 🎯 Prompt Philosophy: Goal-Oriented vs Step-by-Step

**❌ Traditional Automation (Scripted)**:
```
Step 1: Click element with ID 'email_field'
Step 2: Type 'user@example.com'
Step 3: Click element with ID 'password_field'
...
```

**✅ Autonomous Agent (This Demo)**:
```
Mission: Navigate to applications page for [Job Name]
Workflow: Authenticate → Navigate → Search → Access

Agent figures out the "how" on its own!
```

This showcases the **power of LLM-based agents** - they understand context and adapt, rather than following rigid scripts.

## 🏗️ Architecture

### Agent Components

```
┌─────────────────────────────────────────────────────────┐
│                    LangGraph Agent                      │
│                                                         │
│  ┌─────────────┐    ┌──────────┐    ┌──────────────┐ │
│  │  Observe    │ -> │ Planning │ -> │    Action    │ │
│  │  Browser    │    │  (LLM)   │    │  Execution   │ │
│  └─────────────┘    └──────────┘    └──────────────┘ │
│         ↑                                    │          │
│         └────────────────────────────────────┘          │
│                  (Feedback Loop)                        │
└─────────────────────────────────────────────────────────┘
                           ↓
              ┌────────────────────────┐
              │   Chrome Browser       │
              │   (via CDP Protocol)   │
              └────────────────────────┘
```

### LangGraph Flow

```
Start → Observe Browser → Planning (LLM) → Action → Update History
          ↑                                    ↓
          └────────────────────────────────────┘
                      (Loop until done)
```

### Graph Nodes

1. **observe_browser**
   - Captures current page state (URL, title, elements, screenshot)
   - Extracts interactive elements with indexes
   - Highlights elements on page (visual feedback)
   - Sends screenshot to LLM for visual understanding

2. **planning**
   - LLM analyzes screenshot + element list
   - Decides which action to take next
   - Uses tool calling to specify action + parameters

3. **action**
   - Executes the chosen browser action
   - Returns feedback about what happened

4. **update_history**
   - Records what was done and what happened
   - Updates agent memory
   - Checks if task is complete

### Available Actions (Tools)

| Tool | Purpose | Example |
|------|---------|---------|
| `navigate(url)` | Go to a URL | `navigate("https://greenhouse.io")` |
| `click(index)` | Click an element | `click(5)` - clicks element [5] |
| `input_text(index, text)` | Type into field | `input_text(2, "engineer@example.com")` |
| `send_keys(keys)` | Press keyboard keys | `send_keys("Enter")` |
| `scroll(down, pages)` | Scroll page | `scroll(down=True, pages=1.0)` |
| `extract(query)` | Extract info with AI | `extract("what is the job title?")` |
| `screenshot()` | Take screenshot | `screenshot()` |
| `done(result)` | Complete task | `done("Job posted successfully")` |

## 🔧 How It Works

### Step-by-Step Execution

1. **Agent starts** with task description and empty state

2. **Observe phase**:
   - Browser captures current page screenshot
   - Extracts interactive elements (buttons, links, inputs)
   - Highlights elements with orange boxes and indexes
   - Creates visual + textual representation

3. **Planning phase**:
   - LLM receives:
     - Task description
     - Current URL and title
     - List of interactive elements (with indexes)
     - Screenshot of page
     - History of previous actions
   - LLM decides: "I need to click the Sign In button at index [12]"

4. **Action phase**:
   - Agent executes: `click(12)`
   - Browser clicks the element
   - Returns feedback: "✅ Clicked element 12 → Page navigated to dashboard"

5. **Update phase**:
   - Records action and result in history
   - Updates memory
   - Checks if done

6. **Loop** back to step 2 until task complete or max steps reached

## 🚀 Running the Demo

### Prerequisites

1. Python 3.8+
2. Chrome/Chromium browser installed
3. Azure OpenAI credentials in `.env` file
4. **Greenhouse ATS credentials in `.env` file** (see setup below)
5. All dependencies installed:
```bash
pip install -r requirements.txt
```

### Setup Credentials

Add these to your `.env` file:

```env
# Required for all demos
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o-mini

# Required for Greenhouse demo
GREENHOUSE_EMAIL=your-greenhouse-email@example.com
GREENHOUSE_PASSWORD=your-greenhouse-password
```

**Security Note**: Never commit your `.env` file to git. It's already in `.gitignore`.

### Run

```bash
cd greenhouse_agent
python greenhouse_demo.py
```

### What You'll See

1. **Chrome browser opens** (visible by default)
2. **Agent navigates** to Greenhouse login page
3. **Elements are highlighted** with orange boxes and numbers
4. **Agent types** credentials and clicks login
5. **Agent navigates** to Jobs page and searches for the job
6. **Agent clicks** on first job in search results
7. **Agent clicks** "Review applications"
8. **Agent reports** success - task complete!

### Expected Output

```
🚀 Starting LangGraph Browser Agent
Task: Login, search for a job, and navigate to applications
Model: gpt-4o-mini
Max Steps: 20

Step 1/20
🔍 Observing browser state...
📋 URL: https://app8.greenhouse.io/users/sign_in
📋 Elements found: 15 interactive elements
🤔 Agent deciding next action...
📌 Decision: input_text({'index': 2, 'text': 'your-email@example.com'})
✅ Typed 'your-email@example.com' into element 2

Step 2/20
...

✅ TASK COMPLETE
Result: Successfully navigated to applications for "Staff Engineer"
Steps taken: 12
```

## 🔑 Key Concepts for Presentation

### 1. **Autonomous Decision Making**
- Agent receives **goals**, not **instructions**
- Figures out the UI navigation on its own
- Adapts to what it sees on each page
- Demonstrates true AI autonomy (not scripted automation)

### 2. **Vision + Action**
- Agent can "see" the page via screenshots
- Combines visual understanding with element interaction
- LLM analyzes what it sees and decides what to do

### 3. **Element Highlighting**
- Interactive elements are highlighted with boxes
- Each element gets an index number
- Agent references indexes when taking actions

### 4. **State Management**
- Agent maintains:
  - Current browser state (URL, elements, screenshot)
  - Task description
  - Memory of what it's doing
  - History of actions taken
  - Step counter

### 5. **Feedback Loop**
- Agent sees result of each action
- Learns from what happened
- Adjusts next action based on feedback

### 6. **Chrome DevTools Protocol (CDP)**
- Low-level protocol for browser control
- More reliable than Selenium/Playwright for AI agents
- Direct communication with browser

## 🎓 Learning Path

1. **Browser Basics**: Understand how CDP connects to Chrome
2. **State Graph**: See how LangGraph manages agent flow
3. **Vision Integration**: How screenshots enable understanding
4. **Tool Calling**: How LLM decides which action to take
5. **Error Handling**: What happens when actions fail

## 🎯 Demo Characteristics

| Aspect | Details |
|--------|---------|
| **Task** | Automated job posting |
| **Complexity** | Login → Navigate → Multi-step form filling → Submit |
| **Context** | ATS/Recruitment automation |
| **Forms** | Complex multi-field job posting form |
| **Login** | Required with credentials |
| **Use Case** | RPA, HR automation, testing |

## 🔒 Security Note

**Important**: The demo uses hardcoded credentials for demonstration purposes only. In production:
- Store credentials securely (Azure Key Vault, environment variables)
- Use OAuth/SSO when available
- Implement proper access controls
- Audit all automated actions

## 🎯 Real-World Use Cases

This type of browser agent can automate:

1. **Recruitment**:
   - Post jobs across multiple platforms
   - Screen candidate profiles
   - Schedule interviews

2. **Testing**:
   - E2E testing of web applications
   - Regression testing
   - Visual testing

3. **Data Entry**:
   - Filling forms from structured data
   - Migrating data between systems
   - Invoice processing

4. **Monitoring**:
   - Check website functionality
   - Verify content updates
   - Price monitoring

## 🐛 Troubleshooting

### Agent gets stuck in a loop
- Check system prompt for guidance on breaking patterns
- Reduce max_steps to fail faster
- Review history to see repetitive actions

### Login fails
- Verify credentials are correct
- Check if Greenhouse has CAPTCHA (agent can't solve)
- Look for 2FA requirements

### Elements not clickable
- Element might be hidden or disabled
- Try different element index
- Check screenshot to verify element is visible

### Browser doesn't start
- Install Chrome/Chromium
- Check if port 9222 is available
- Run with `headless=False` to debug visually

## 📈 Extension Ideas

1. **Multi-site posting**: Post same job to multiple platforms
2. **Bulk operations**: Create multiple jobs from CSV
3. **Human-in-the-loop**: Ask for confirmation before submit
4. **Error recovery**: Retry on failures, alert on critical errors
5. **Candidate screening**: Parse resumes and score candidates

## 🤔 Discussion Questions for Session

1. How does the agent know which element to click?
2. What happens if page layout changes?
3. How to handle dynamic content (JavaScript-heavy sites)?
4. How to make agent more robust to website changes?
5. When should we use browser agents vs APIs?
6. How to test and validate agent behavior?

## 📖 References

- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Browser-use Library](https://github.com/browser-use/browser-use) (inspiration)
- [Greenhouse ATS API](https://developers.greenhouse.io/) (alternative to browser automation)

