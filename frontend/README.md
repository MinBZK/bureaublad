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

## Product Tiles

Applications are presented as product tiles on the homepage. Every product is
configured in the backend and opens in a new browser tab.

### Configuration Fields

- **`id`** (required): Unique identifier (e.g. `"ocs"`, `"docs"`, `"drive"`)
- **`icon`** (optional): Icon name
- **`url`** (required): External application URL
- **`title`** (required): Display name on the product tile
- **`enabled`** (required): Whether the product is shown

To add a product, add its service URL and title to `backend/.env` and enable
the matching `*_CARD` setting. The backend `/api/v1/config` endpoint returns the
enabled applications, which the frontend renders as tiles.

### Styling

The frontend follows the Rijkshuisstijl (Rijksoverheid) visual language. Brand
colours are CSS custom properties and can be adjusted at runtime with the
palette picker in the header, or through a `theme_css` file returned by the
backend.

The picker offers all official 100% Rijkshuisstijl colours (Lintblauw plus the
17 communication colours). Tints are only used as supporting surfaces together
with the 100% colour, and Cool Gray is reserved for neutral surfaces, charts and
tables. See [THEMING.md](THEMING.md) for details.
