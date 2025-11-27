# Mijn portaal - Frontend

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-started/get-docker/) installed on your system

### Running the Application

The frontend is part of the full Bureaublad application stack. To start the application:

1. **Configure environment** (from project root):

   ```bash
   cp backend/example.env backend/.env
   ```

2. **Start with Docker Compose** (from project root):

   ```bash
   docker compose build
   docker compose up
   ```

3. **Access the application**:
   - Frontend: [http://bureaublad.localhost](http://bureaublad.localhost)
   - Backend API: [http://bureaublad.localhost/api/](http://bureaublad.localhost/api/)

### Development (Frontend Only)

If you want to run the frontend in development mode separately:

1. **Install dependencies**:

   ```bash
   npm install
   # or
   bun install
   ```

2. **Run the development server**:

   ```bash
   npm run dev
   # or
   bun dev
   ```

3. **Open** [http://localhost:3000](http://localhost:3000) with your browser

**Note**: When running frontend separately, make sure the backend is running and accessible.

## Embedding External Applications

External applications can be embedded as iframes within the portal. The configuration is based on the `SIDEBAR_LINKS_JSON` setting in the backend `.env` file.

### Configuration

Each application in `SIDEBAR_LINKS_JSON` with `"iframe": true` will be embedded in the portal. The application's `id` field determines the route path.

#### Configuration Fields

- **`id`** (required): Unique identifier and route path (e.g., `"ocs"` creates `/ocs` route)
- **`icon`** (required): Icon name from [Ant Design Icons](https://ant.design/components/icon) (e.g., `"MailOutlined"`, `"FileTextOutlined"`, `"AppstoreOutlined"`)
- **`url`** (required): The external application URL to embed
- **`title`** (required): Display name in the navigation menu
- **`iframe`** (optional): Set to `true` to embed in iframe, `false` or omit to open in new tab

#### Example Configuration

```json
{
  "id": "ocs",
  "icon": "MailOutlined",
  "url": "https://nextcloud.example.com",
  "title": "Files",
  "iframe": true
}
```

This configuration creates:

- **Route**: `/ocs`
- **Menu Link**: "Files" in the navigation menu with a Mail icon
- **Embedded URL**: `https://nextcloud.example.com` loaded in an iframe

**Note**: The `icon` field should contain just the icon name from Ant Design Icons (without the `import` or component syntax). The `DynamicIcon` component automatically resolves the icon name.

### Adding a New Embedded Application

1. **Add to backend configuration** (`backend/.env`):

   ```json
   {
     "id": "myapp",
     "icon": "AppstoreOutlined",
     "url": "https://myapp.example.com",
     "title": "My App",
     "iframe": true
   }
   ```

2. **Create the route page** (`src/app/(EmbaddedApps)/myapp/page.jsx`):

   ```jsx
   import ExternalApp from "../../Common/ExternalApp";

   export default function MyAppPage() {
     return <ExternalApp />;
   }
   ```

3. The `ExternalApp` component automatically:
   - Matches the route path to the application `id`
   - Loads the configured `url` in an iframe
   - Displays the application `title`

### Route Structure

All embedded applications are organized under the `(EmbaddedApps)` route group:

```
src/app/(EmbaddedApps)/
  ├── ai/page.jsx          → /ai
  ├── calendar/page.jsx    → /calendar
  ├── docs/page.jsx        → /docs
  ├── drive/page.jsx       → /drive
  ├── grist/page.jsx       → /grist
  ├── ocs/page.jsx         → /ocs
  ├── meet/page.jsx        → /meet
  └── conversation/page.jsx → /conversation
```

The `(EmbaddedApps)` folder with parentheses is a Next.js Route Group - it organizes files without affecting the URL structure.
